import os
import sys
import uuid

import streamlit as st
from streamlit_ws_localstorage import injectWebsocketCode
from streamlit_ws_localstorage.auth_redirect_server.auth_util import loginWithOAuthComponent
import streamlit.components.v1 as components

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)):
    sys.path.append(path2add)
from util import metricFn, getLinkedinOauth, getLoggedInUser, initMysqlConnection, runMysqlQuery, getLinkedinUserProfile    # noqa


USER_PROFILE_PIC_KEY = '_user.profilePic'
USER_EMAIL_ADDRESS_KEY = '_user.emailAddress'
AUTH_CODE_KEY = '_linkedin.authCode'


def logoutFn():
    conn = injectWebsocketCode(hostPort='linode.liquidco.in', uid=str(uuid.uuid1()))
    conn.setLocalStorageVal(key=USER_PROFILE_PIC_KEY, val='')
    conn.setLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY, val='')
    conn.setLocalStorageVal(key=AUTH_CODE_KEY, val='')
    st.write('Logged out, reloading the page')
    code = """<script>setTimeout(() => window.parent.location.reload(), 1000)</script>"""
    components.html(code, height=100)


def main():
    st.title('Login demo')

    uid = str(uuid.uuid1())
    conn = injectWebsocketCode(hostPort='linode.liquidco.in', uid=uid)
    print('conn: ', conn)

    emailAddress = conn.getLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY)
    authCode = conn.getLocalStorageVal(key=AUTH_CODE_KEY)
    if authCode and not emailAddress:
        (firstName, lastName, displayImage, id, profilePic, emailAddress) = getLinkedinUserProfile(authCode)
        conn.setLocalStorageVal(key=USER_PROFILE_PIC_KEY, val=profilePic)
        conn.setLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY, val=emailAddress)

    profilePic = conn.getLocalStorageVal(key=USER_PROFILE_PIC_KEY)
    emailAddress = conn.getLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY)
    if emailAddress:
        st.write('Welcome ' + emailAddress)
        st.image(profilePic, width=200)
        st.button('Logout', on_click=logoutFn)
    else:
        uid = str(uuid.uuid1())
        obj, authObj = getLinkedinOauth(uid)
        st.markdown('<a href="{}" target="_blank">Login with LinkedIn</a>'.format(authObj.authorization_url), unsafe_allow_html=True)
        loginWithOAuthComponent('linode.liquidco.in', uid, AUTH_CODE_KEY, reloadInSecs=6, height=40)

print ('In Login_Demo.py')
main()
