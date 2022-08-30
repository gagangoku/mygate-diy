import os
import sys

import streamlit as st
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from utils import initStreamlitApp


print ('In Upcoming_Campaign.py')
initStreamlitApp()
st.title('Upcoming campaigns')
st.write('TBD')

uid = getOrCreateUID()
st.write('uid: ' + uid)

conn = injectWebsocketCode(hostPort='linode.liquidco.in', uid=uid)
print ('conn: ', conn)

st.write('calling setLocalStorageVal')
ret = conn.setLocalStorageVal(key='k1', val='v1')
st.write('ret: ' + ret)

st.write('calling getLocalStorageVal')
ret = conn.getLocalStorageVal(key='k1')
st.write('ret: ' + ret)
