import os
import sys

import streamlit as st
from PIL import Image
from streamlit.logger import get_logger

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from utils import metricFn, initStreamlitApp


LOGGER = get_logger(__name__)

AdProp_Noticeboard = 'Noticeboard'
AdProp_PAC = 'Post Approval Card'
AdProp_PAS = 'Post Action Screen'
AdProp_Spotlight = 'Spotlight'
AdProp_Kiosk = 'Kiosk'
AdProp_Signage = 'Signage'
AdProp_D2D = 'Door to Door'
AdProp_RWA = 'Management committees'


AD_PROPERTIES = [AdProp_Noticeboard, AdProp_PAC, AdProp_PAS, AdProp_Spotlight, AdProp_Kiosk, AdProp_Signage, AdProp_D2D, AdProp_RWA]
TAGS = ['food_lover', 'pet_owner', 'gender_male', 'gender_female', 'car_owner', 'society_affluence_high', 'society_affluence_medium','society_affluence_low', 'society_active_units_gt_100', 'society_active_units_gt_500', 'society_active_units_gt_1000', 'kids_age_lt_5', 'kids_age_gt_5', 'kids_age_gt_10']
CITIES = ['Gandhinagar', 'Pune', 'Ahmedabad', 'Bengaluru', 'Navi', 'Mumbai', 'Pathanamthitta', 'Chennai', 'Lucknow', 'Mumbai', 'Noida', 'Agra', 'Kochi', 'Hyderabad', 'Thane', 'Nagpur', 'Gurugram', 'Patna', 'Sambalpur', 'Kolkata', 'Thiruvananthapuram', 'Kalyan', 'New', 'Delhi', 'Surat', 'Vadodara', 'Indore', 'Raipur', 'Zirakpur', 'Kanpur', 'Bhiwadi', 'Neemrana', 'Faridabad', 'Ghaziabad', 'Greater', 'Noida', 'Nashik', 'Vijayawada', 'Mohali', 'Sonipat', 'Mysuru', 'Mandsaur', 'Dehradun', 'Solapur', 'Hosur', 'Ludhiana', 'Bhopal', 'Jaipur', 'Coimbatore', 'Bhubaneswar', 'North', 'Dumdum', 'Kota', 'Haridwar', 'Panchkula', 'Panipat', 'Visakhapatnam', 'Ranchi', 'Gwalior', 'Asansol', 'Mgdev', 'City', 'Chandigarh', 'Thrissur', 'Guwahati', 'Durg', 'Meerut', 'Kolhapur', 'Jamshedpur', 'Jodhpur', 'Lonavala', 'Korba', 'Bharuch', 'North', 'Goa', 'Kalaburagi', 'Muzaffarpur', 'Dharuhera', 'Valsad', 'Dhamtari', 'Siliguri', 'Ujjain', 'Bilaspur', 'Jabalpur', 'Bhilai', 'Rajkot', 'Ambedkar', 'Nagar', 'Alwar', 'Boisar', 'Bahadurgarh', 'Rudrapur', 'Bishnupur', 'Birbhum', 'Sirhind', 'Fatehgarh', 'Sahib', 'Bhagalpur', 'Jalandhar', 'Guntur', 'Karnal', 'Sirohi', 'Neemuch', 'Kozhikode', 'Mathura', 'Dubai', 'Vapi', 'Chandrapur', 'Anantapur', 'Daman', 'Nairobi', 'Jagdalpur', 'Simga', 'Jharsuguda', 'Muzaffarnagar', 'Rewari', 'Kheda', 'Sidhi', 'Moradabad', 'Khammam', 'Kakinada', 'Rohtak', 'Jamnagar', 'Kutch', 'Aurangabad', 'Haldia', 'Latur', 'Rajnandgaon', 'Solan', 'Vizianagaram', 'Amritsar', 'Rewa', 'Kottayam', 'Mangaluru', 'Sonbhadra', 'Shillong', 'Kanpur', 'Jaggayyapet', 'South', 'Goa', 'Jammu', 'Auroville', 'Tiruppur', 'Tirupati', 'Salem', 'Ajmer', 'Adchini', 'Bharatpur', 'Satna', 'Udaipur', 'Chittorgarh', 'Dhanbad', 'Kasaragod', 'Ariyalur', 'Amreli', 'District', 'Durgapur', 'Murshidabad', 'Rishikesh']


def load_image(image_file):
    img = Image.open(image_file)
    return img


def renderSection1():
    st.header('Basic info')
    ad_properties = st.multiselect('Ad properties (required)', AD_PROPERTIES)

    c1, c2 = st.columns([1, 1])
    with c1:
        brand = st.text_input(label='Brand')
    with c2:
        brandCategory = st.text_input(label='Brand Category')
    userTags = st.multiselect('Users to target', TAGS)
    budget = st.slider(label='Your daily budget in Rupees (required)', value=10000, min_value=1000, max_value=50000, step=500)
    with st.expander("Advanced options"):
        st.caption('Finer location controls')
        st.caption('Integrated ads - Spotlight & PAC reminders for Notice')
    submit_button = st.button(label='Next')


    if submit_button:
        errmsg = []
        if not len(ad_properties):
            errmsg.append("\nSelect atleast one ad property")
        if not budget:
            errmsg.append("\nBudget is mandatory")

        for er in errmsg:
            st.error(er)
        if len(errmsg) > 0:
            return

        col1, col2 = st.columns(2)
        with col1:
            metricFn(budget / 10, 'Expected impressions (daily)', (0, 250, 102))
        with col2:
            metricFn(budget / 100, 'Expected clicks (daily)', (245, 138, 66))

        # st.write('**Expected impressions**: {}'.format(budget / 10))
        # st.write('**Expected clicks**: {}'.format(budget / 100))

        out = { 'ad_properties': ad_properties, 'brand': brand, 'brandCategory': brandCategory, 'userTags': userTags, 'budget': budget }
        print (out)
        return out
    return None


def renderSection2(out):
    st.header('CREATIVES')
    print (out)
    ad_properties = out['ad_properties'] if out else []
    if AdProp_Spotlight in ad_properties:
        st.subheader('Spotlight creative')
        # st.image(
        #     "https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif", # I prefer to load the GIFs using GIPHY
        #     width=200, # The actual size of most gifs on GIPHY are really small, and using the column-width parameter would make it weirdly big. So I would suggest adjusting the width manually!
        # )
        st.write('image dimension - 1000 px * 1000 px')
        image_file = st.file_uploader("Upload creative", type=["png", "jpg", "jpeg"], key='spotlight')
        if image_file is not None:
            file_details = { "filename": image_file.name, "filetype": image_file.type, "filesize": image_file.size }
            st.image(load_image(image_file), width=250)
    if AdProp_PAC in ad_properties:
        st.subheader('PAC creative')
        st.write('image dimension - 1000 px * 1000 px')
        image_file = st.file_uploader("Upload creative", type=["png", "jpg", "jpeg"], key='pac')
        if image_file is not None:
            file_details = { "filename": image_file.name, "filetype": image_file.type, "filesize": image_file.size }
            st.image(load_image(image_file), width=250)


print ('In Run_a_campaign.py')
initStreamlitApp()
st.title('Run a campaign')
st.write('Run your ad creatives directly from this dashboard')
out = renderSection1()
print ('out = ', out)
st.session_state.out = out or (st.session_state.out if 'out' in st.session_state else None)
if st.session_state.out:
    renderSection2(st.session_state.out)
