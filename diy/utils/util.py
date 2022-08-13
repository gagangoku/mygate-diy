import json

import extra_streamlit_components as stx
import mysql.connector
import streamlit as st
from linkedin_v2 import linkedin

LINKEDIN_COOKIE_NAME = 'linkedin'

@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()


def metricFn(value, label, boxColor, fontColor=(0, 0, 0)):
    fontsize = 36
    valign = "left"
    iconname = "fas fa-asterisk"
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'

    htmlstr = f"""<p style='background-color: rgb({boxColor[0]}, 
                                                  {boxColor[1]}, 
                                                  {boxColor[2]}, 0.75); 
                            color: rgb({fontColor[0]}, 
                                       {fontColor[1]}, 
                                       {fontColor[2]}, 0.75); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 20px; 
                            padding-top: 20px; 
                            padding-bottom: 20px; 
                            line-height:25px;'>
                            <i class1='{iconname} fa-xs'></i> {value}
                            </style><BR><span style='font-size: 15px; 
                            margin-top: 0;'>{label}</style></span></p>"""
    st.markdown(lnk + htmlstr, unsafe_allow_html=True)


def getLinkedinOauth():
    # objStr = get_manager().get(cookie=LINKEDIN_COOKIE_NAME) or '{}'
    # obj = json.loads(objStr)
    obj = json.loads('{}')
    CLIENT_KEY = '86k87sfq7cd1s4'
    CLIENT_SECRET = '9HnaSDhz2Yv96Uk0'
    RETURN_URL = 'http://localhost:8501/%EF%B8%8F_Settings'
    authentication = linkedin.LinkedInAuthentication(CLIENT_KEY, CLIENT_SECRET, RETURN_URL,
                                                     ['r_liteprofile', 'r_emailaddress'])
    authentication.state = 'linkedin'
    return obj, authentication


# From https://github.com/HootsuiteLabs/python-linkedin-v2
# From https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin?context=linkedin%2Fconsumer%2Fcontext
def processLinkedinRedirect():
    d = st.experimental_get_query_params()
    code = d['code'][0]
    print ('code: ', code)

    obj, authObj = getLinkedinOauth()
    authObj.authorization_code = code
    authToken = authObj.get_access_token()

    application = linkedin.LinkedInApplication(token=authToken)
    profile = application.get_profile()
    print('profile: ', profile)
    firstName, lastName, displayImage, id = profile['localizedFirstName'], profile['localizedLastName'], profile['profilePicture']['displayImage'], profile['id']

    # Get profile picture
    response = application.make_request('GET', 'https://api.linkedin.com/v2/me?projection=(profilePicture(displayImage~:playableStreams))')
    json_response = response.json()
    print ('profile pic json_response: ', json_response)
    profilePic = json_response['profilePicture']['displayImage~']['elements'][2]['identifiers'][0]['identifier']

    # Get email
    response = application.make_request('GET', 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))')
    json_response = response.json()
    print ('email json_response: ', json_response)
    emailAddress = json_response['elements'][0]['handle~']['emailAddress']

    rsp = (firstName, lastName, displayImage, id, profilePic, emailAddress)
    print ('processLinkedinRedirect: ', rsp)
    return rsp


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def initMysqlConnection():
    return mysql.connector.connect(**st.secrets["mysql"])

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def runMysqlQuery(query, _conn):
    with _conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def getLoggedInUser():
    return st.experimental_user
