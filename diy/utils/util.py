import json
import ssl
import time
import uuid

import extra_streamlit_components as stx
import mysql.connector
import rel
import streamlit as st
import streamlit.components.v1 as components
from linkedin_v2 import linkedin

import websocket

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
# Don't use st.experimental_singleton because connections can go bad, use st.cache with ttl of 5 mins
@st.cache(ttl=300, hash_funcs={ssl.SSLSocket: id}, allow_output_mutation=True)
def initMysqlConnection():
    return mysql.connector.connect(**st.secrets["mysql"])

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 5 min.
@st.experimental_memo(ttl=300)
def runMysqlQuery(query, _conn):
    with _conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def getLoggedInUser():
    return st.experimental_user


def getOrCreateUID():
    if 'uid' not in st.session_state:
        st.session_state['uid'] = ''
    st.session_state['uid'] = st.session_state['uid'] or str(uuid.uuid1())
    print ('getOrCreateUID: ', st.session_state['uid'])
    return st.session_state['uid']



# Generate a unique uid that gets embedded in components.html for frontend
# Both frontend and server connect to ws using the same uid
# server sends commands like localStorage_get_key, localStorage_set_key, localStorage_clear_key etc. to the WS server,
# which relays the commands to the other connected endpoint (the frontend), and back
def injectWebsocketCode(hostPort, uid):
    code = '<script>function connect() { console.log("in connect uid: ", "' + uid + '"); var ws = new WebSocket("ws://' + hostPort + '/?uid=' + uid + '");' + """
  ws.onopen = function() {
    // subscribe to some channels
    // ws.send(JSON.stringify({ status: 'connected' }));
    console.log("onopen");
  };

  ws.onmessage = function(e) {
    console.log('Message:', e.data);
    var obj = JSON.parse(e.data);
    if (obj.cmd == 'localStorage_get_key') {
        var val = localStorage[obj.key] || '';
        ws.send(JSON.stringify({ status: 'success', val }));
        console.log('returning: ', val);
    } else if (obj.cmd == 'localStorage_set_key') {
        localStorage[obj.key] = obj.val;
        ws.send(JSON.stringify({ status: 'success' }));
        console.log('set: ', obj.key, obj.val);
    }
  };

  ws.onclose = function(e) {
    console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    setTimeout(function() {
      connect();
    }, 1000);
  };

  ws.onerror = function(err) {
    console.error('Socket encountered error: ', err.message, 'Closing socket');
    ws.close();
  };
}

connect();
</script>
        """
    components.html(code, height=0)
    time.sleep(1)       # Without sleep there are problems
    return WebsocketClient(hostPort, uid)


class WebsocketClient:
    def __init__(self, hostPort, uid):
        self.hostPort = hostPort
        self.uid = uid

    def getLocalStorageVal(self, key):
        ws = websocket.create_connection("ws://" + self.hostPort + "/?uid=" + self.uid)
        ws.send(json.dumps({ 'cmd': 'localStorage_get_key', 'key': key }))
        result = ws.recv()
        print("Received:", result)
        ws.close()
        return json.loads(result)['val']

    def setLocalStorageVal(self, key, val):
        ws = websocket.create_connection("ws://" + self.hostPort + "/?uid=" + self.uid)
        ws.send(json.dumps({ 'cmd': 'localStorage_set_key', 'key': key, 'val': val }))
        result = ws.recv()
        print("Received:", result)
        ws.close()
        return result
