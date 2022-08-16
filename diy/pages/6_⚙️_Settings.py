import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from util import metricFn, getLinkedinOauth, processLinkedinRedirect, getLoggedInUser, initMysqlConnection, runMysqlQuery, injectWebsocketCode, getOrCreateUID    # noqa


def main():
    st.title('Settings')
    st.write('Controls like adding your team, email alerts, webhooks for leads etc can be configured here')

    uid = getOrCreateUID()
    conn = injectWebsocketCode(hostPort='linode.liquidco.in', uid=uid)
    print('conn: ', conn)

    d = st.experimental_get_query_params()
    if 'code' in d and len(d['code']) == 1 and 'state' in d and len(d['state']) == 1 and d['state'][0] == 'linkedin':
        # First time linkedin redirect
        firstName, lastName, displayImage, id, profilePic, emailAddress = processLinkedinRedirect()
        st.write('Name: ' + firstName + ' ' + lastName)
        st.write('emailAddress: ' + emailAddress)
        st.image(profilePic, width=200)
        st.experimental_set_query_params()

        ret = conn.setLocalStorageVal(key='_user.emailAddress', val=emailAddress)
        ret = conn.setLocalStorageVal(key='_user.profilePic', val=profilePic)
        st.write('Saved locally')
        return

    profilePic = conn.getLocalStorageVal(key='_user.profilePic')
    emailAddress = conn.getLocalStorageVal(key='_user.emailAddress')
    if emailAddress:
        st.write('Welcome ' + emailAddress)
        st.image(profilePic, width=200)
    else:
        obj, authObj = getLinkedinOauth()
        st.markdown('<a href="{}" target="_self">Login with LinkedIn</a>'.format(authObj.authorization_url), unsafe_allow_html=True)
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
