import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from util import metricFn, getLinkedinOauth, processLinkedinRedirect, injectWebsocketCode, getOrCreateUID    # noqa

print ('In Upcoming_Campaign.py')



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
