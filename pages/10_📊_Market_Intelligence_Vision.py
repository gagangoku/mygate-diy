import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add, __file__)
if (not (path2add in sys.path)):
    sys.path.append(path2add)
from utils import metricFn, getLinkedinOauth


print ('In Market_Intel_Thoughts')
# st.set_page_config(layout="wide")
st.title('Market intelligence - The vision')

st.markdown("""
    ### Mygate reach
    Mygate is the default gate security app for gated communities today and a well known brand.
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    metricFn('3.5 Million', 'Homes on Mygate', boxColor=(0, 250, 102), maxWidth=300)
with col2:
    metricFn('2.5 Million', 'Active users on Mygate', boxColor=(245, 138, 66), maxWidth=300)
with col3:
    metricFn('25000+', 'Societies on Mygate', boxColor=(252, 3, 252), maxWidth=300)


st.markdown("""
    ### Data captured
    - more than 10 Million e-com deliveries every month
    - more than 7 Million food deliveries every month
    - more than 30 Million daily help (maid / cook / nanny / driver / car washer) entries per month
    - ...

    We <b>don't extrapolate</b> from partial data to come up with a representative number, since we are the source of data.

    ### Imagine
    Some super interesting things we can do with this data:
    - Split of food delivery frequency by city, locality, society. Which areas are picking up, which areas are underserved
    - Split by owner / tenant - are tenants more likely to order food ?
    - Split by closeness to techparks - 
    - Split by daily help (maid / cook) - are users who employ a cook less (or more) likely to order food ? Are they more likely to order food when the cook doesnt come ?
    - Split by when they shifted in the society - are newcomers more likely to order food ?
    - ...

    ### Who can use it
    - Marketers & brands - growth stage, user acquisition
    - VC's - to see where the market is, and solidify their thesis
    - Incubators / accelerators - to recognize trends and advise their portfolio companies
    - Consultancies - to get the on ground reality and advise their customers on how to grow
    - Marketing agencies - to acquire lots of customers for your customers
    - Influencers - to understand market sentiments and what their audience might find interesting

    ### Data is the new oil
    The idea is to collect these kinds of super valuable insights, and eventually build the ability to target such segments on Mygate.

    Tell us what data is interesting to you.

""", unsafe_allow_html=True)

