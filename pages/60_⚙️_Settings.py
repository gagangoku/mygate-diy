import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from utils import initStreamlitApp


def main():
    st.title('Settings')
    st.write('Controls like adding your team, email alerts, webhooks for leads etc can be configured here')


print ('In Settings.py')
initStreamlitApp()
main()
