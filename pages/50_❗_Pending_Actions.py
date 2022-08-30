import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from utils import initStreamlitApp


print ('In Pending_Actions.py')
initStreamlitApp()
st.title('Pending actions')
st.write('TBD')
