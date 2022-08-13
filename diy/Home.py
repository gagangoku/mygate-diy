import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'diy/utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from util import metricFn, getLinkedinOauth, processLinkedinRedirect    # noqa


def run():
    st.set_page_config(layout="wide")
    st.title('Mygate DIY')

    print ('in Home.py')

    st.markdown(
        """
        Mygate DIY lets you play with analytics for your campaigns, and schedule new campaigns easily.

        You can:
        - <a href="/Market_Insights" target="_self">Get market insights</a>
        - <a href="/Campaign_Analytics" target="_self">Get insights into your campaigns</a>
        - <a href="/%EF%B8%8F_Run_a_campaign" target="_self">Run a campaign</a>
        - <a href="/Upcoming_Campaigns" target="_self">See your upcoming campaigns and actions associated with them</a>
        - <a href="/%EF%B8%8F_Settings" target="_self">Change settings like email alerts, adding team, leads webhooks etc.</a>
        ### Want to learn more?
        - Ask a question in our [community forums](https://discuss.streamlit.io)
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    run()