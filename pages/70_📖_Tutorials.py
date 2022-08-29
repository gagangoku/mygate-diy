import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from utils import metricFn, getLinkedinOauth

st.title('Tutorials')
st.write('Videos of how you to use the DIY tool')

print ('In Tutorials.py')

if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter():
    st.session_state.count += 1

st.button('Increment', on_click=increment_counter)
st.write('Count = ', st.session_state.count)
