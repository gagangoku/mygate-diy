import os
import sys
import uuid

import streamlit as st
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from util import metricFn, getLinkedinOauth, getLoggedInUser, initMysqlConnection, runMysqlQuery, loginWithLinkedInComponent, getLinkedinUserProfile    # noqa


def main():
    st.title('Settings')
    st.write('Controls like adding your team, email alerts, webhooks for leads etc can be configured here')

    uid = getOrCreateUID()
    conn = injectWebsocketCode(hostPort='linode.liquidco.in', uid=uid)
    print('conn: ', conn)

    emailAddress = conn.getLocalStorageVal(key='_user.emailAddress')
    authCode = conn.getLocalStorageVal(key='_linkedin.authCode')
    if authCode and not emailAddress:
        (firstName, lastName, displayImage, id, profilePic, emailAddress) = getLinkedinUserProfile(authCode)
        conn.setLocalStorageVal(key='_user.profilePic', val=profilePic)
        conn.setLocalStorageVal(key='_user.emailAddress', val=emailAddress)

    profilePic = conn.getLocalStorageVal(key='_user.profilePic')
    emailAddress = conn.getLocalStorageVal(key='_user.emailAddress')
    if emailAddress:
        st.write('Welcome ' + emailAddress)
        st.image(profilePic, width=200)
    else:
        uid = str(uuid.uuid1())
        obj, authObj = getLinkedinOauth(uid)
        st.markdown('<a href="{}" target="_blank">Login with LinkedIn</a>'.format(authObj.authorization_url), unsafe_allow_html=True)
        loginWithLinkedInComponent(uid)

        # userEmail = getLoggedInUser()['email']
        # st.write('User email: {}'.format(userEmail))
        # conn = initMysqlConnection()
        # rows = runMysqlQuery(query="select id,email,data from userTable where email='{}'".format(userEmail), _conn=conn)
        # print ('rows: ', rows)
        # for row in rows:
        #     (id, email, data) = row
        #     st.write('id: {}, email: {}, data: {}'.format(id, email, data))


print ('In Settings.py')
main()
