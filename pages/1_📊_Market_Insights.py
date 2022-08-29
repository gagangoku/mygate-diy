import os
import sys

import streamlit as st
from streamlit.logger import get_logger

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from utils import metricFn, getLinkedinOauth

import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


LOGGER = get_logger(__name__)


SEGMENT_OVERALL = 'Overall'
SEGMENT_GENDER = 'Gender'
SEGMENT_MOBILE_DEVICE = 'Mobile device'
SEGMENT_AGE = 'Age'
SEGMENT_GEO_LOCATION = 'Geo location'
SEGMENT_ECOM_PURCHASE = 'Ecom purchase freq'
SEGMENT_FOOD_DELIVERY = 'Food delivery freq'
SEGMENT_COMMUTE = 'Commute freq'
SEGMENT_DAILY_HELP = 'Daily help freq'
SEGMENT_AUTOMOBILE = 'Automobile split'
SEGMENT_OWNER_TENANT = 'Owner / tenant'
SEGMENT_KIDS = 'Kids'
SEGMENT_PETS = 'Pet affinity'
SEGMENT_RENTAL_COST = 'Property - rental cost'
SEGMENT_BUY_SELL_COST = 'Property - buy sell cost'


# From https://streamlit.io/gallery
# From https://streamlit-demo-uber-nyc-pickups-streamlit-app-456wus.streamlitapp.com/
# https://github.com/streamlit/demo-uber-nyc-pickups/blob/main/streamlit_app.py
@st.experimental_singleton
def load_data():
    data = pd.read_csv(
        "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz",
        nrows=100000,  # approx. 10% of data
        names=[
            "date/time",
            "lat",
            "lon",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0, 1, 2],  # doesn't load last column, constant value "B02512"
        parse_dates=[
            "date/time"
        ],  # set as datetime instead of converting after the fact
    )
    return data

# FUNCTION FOR AIRPORT MAPS
def showMap(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )

# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.experimental_memo
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# FILTER DATA FOR A SPECIFIC HOUR, CACHE
@st.experimental_memo
def filterdata(df, hour_selected):
    return df[df["date/time"].dt.hour == hour_selected]


def pieChart(labels, sizes, caption="", figsize=(10, 5)):
    explode = [0.005 for x in range(len(labels))]
    fig1, ax1 = plt.subplots(figsize=figsize)
    ax1.pie(sizes,
            explode=explode,
            labels=labels,
            autopct='%1.1f%%',
            shadow=False,
            startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.markdown("<div style='text-align: center; font-size: 16px; font-weight: bold'>{}</div>".format(caption), unsafe_allow_html=True)
    st.pyplot(fig1)
    # st.markdown("<div style='text-align: center; font-size: 14px; font-weight: normal'>{}</div>".format(caption), unsafe_allow_html=True)
    st.markdown("""---""")


def overallSegment():
    col1, col2, col3 = st.columns(3)
    with col1:
        metricFn('3.5 Million', 'Homes on Mygate', (0, 250, 102))
    with col2:
        metricFn('2.5 Million', 'Active users on Mygate', (245, 138, 66))
    with col3:
        metricFn('25000+', 'Societies on Mygate', (252, 3, 252))

def genderSegment():
    pieChart(labels=['MALE', 'FEMALE', 'UNKNOWN'], sizes=[55, 40, 5], caption='Gender split')

def mobileDeviceSegment():
    pieChart(labels=['Android', 'IOS', 'Jio'], sizes=[55, 40, 5], caption='Operating System')
    pieChart(labels=['<5 inch', '>5 inch'], sizes=[55, 45], caption='Screen size')

def ageSegment():
    st.write('TBD')

def geoLocationSegment():
    print ('Geo location - calling load_data')
    data = load_data()
    hour_selected = 6
    midpoint = mpoint(data["lat"], data["lon"])
    st.write(
        f"""**Societies on Mygate**"""
    )
    showMap(filterdata(data, hour_selected), midpoint[0], midpoint[1], 10)

def ecomPurchaseSegment():
    st.write('TBD')

def foodDeliverySegment():
    st.write('TBD')

def commuteFreqSegment():
    st.write('TBD')

def dailyHelpSegment():
    st.write('TBD')

def automobileSegment():
    st.write('TBD')

def ownerTenantSegment():
    st.write('TBD')

def kidsSegment():
    st.write('TBD')

def petsSegment():
    st.write('TBD')

def rentalCostSegment():
    st.write('TBD')

def buySellCostSegment():
    st.write('TBD')


def pledgeSegment():
    st.write('TBD')
    data = pd.read_csv("/tmp/pledge.csv")
    print ('data: ', data)
    print('data number of rows: {}'.format(len(data)))
    print('data min: {}'.format(data.min()[0]))
    print('data max: {}'.format(data.max()[0]))
    print('data avg: {}'.format(data.sum()[0] / len(data)))
    frequency, bins = np.histogram(data, bins=20, range=[0, 100])

    binArray = []
    percentArray = []
    freqArray = []
    for b, f in zip(bins[1:], frequency):
        p = round(100*f/len(data), 1)
        binArray.append(b)
        freqArray.append(f)
        percentArray.append(p)

    obj = { 'bins': binArray, 'percents': percentArray, 'freq': freqArray }
    df = pd.DataFrame(obj)

    plt.margins(x=0, y=0)
    df.plot(kind='area', x='bins', y='percents', legend=None)
    plt.rc('grid', linestyle="dotted", color='#a0a0a0')
    plt.grid(True)
    plt.xlabel('% of shares pledged')
    plt.ylabel('% of companies')
    plt.xticks([10*x for x in range(10)])
    plt.yticks([10*x for x in range(8)])
    st.pyplot(fig=plt, clear_figure=True)

    plt.margins(x=0, y=0)
    df.plot(kind='area', x='bins', y='freq', legend=None)
    plt.rc('grid', linestyle="dotted", color='#a0a0a0')
    plt.grid(True)
    plt.xlabel('% of shares pledged')
    plt.ylabel('# of companies')
    plt.xticks([10*x for x in range(10)])
    st.pyplot(fig=plt, clear_figure=True)



def render():
    segment = st.radio(label="Select a segment to view",
                       options=[SEGMENT_OVERALL, SEGMENT_GENDER, SEGMENT_MOBILE_DEVICE, SEGMENT_AGE,
                                SEGMENT_GEO_LOCATION, SEGMENT_ECOM_PURCHASE, SEGMENT_FOOD_DELIVERY, SEGMENT_COMMUTE,
                                SEGMENT_DAILY_HELP, SEGMENT_AUTOMOBILE, SEGMENT_OWNER_TENANT, SEGMENT_KIDS, SEGMENT_PETS,
                                SEGMENT_RENTAL_COST, SEGMENT_BUY_SELL_COST
    ])

    st.header('Segment: ' + segment)

    if segment == SEGMENT_OVERALL:
        overallSegment()
    elif segment == SEGMENT_GENDER:
        genderSegment()
    elif segment == SEGMENT_MOBILE_DEVICE:
        mobileDeviceSegment()
    elif segment == SEGMENT_AGE:
        ageSegment()
    elif segment == SEGMENT_GEO_LOCATION:
        geoLocationSegment()
    elif segment == SEGMENT_ECOM_PURCHASE:
        ecomPurchaseSegment()
    elif segment == SEGMENT_FOOD_DELIVERY:
        foodDeliverySegment()
    elif segment == SEGMENT_COMMUTE:
        commuteFreqSegment()
    elif segment == SEGMENT_DAILY_HELP:
        dailyHelpSegment()
    elif segment == SEGMENT_AUTOMOBILE:
        automobileSegment()
    elif segment == SEGMENT_OWNER_TENANT:
        ownerTenantSegment()
    elif segment == SEGMENT_KIDS:
        kidsSegment()
    elif segment == SEGMENT_PETS:
        petsSegment()
    elif segment == SEGMENT_RENTAL_COST:
        rentalCostSegment()
    elif segment == SEGMENT_BUY_SELL_COST:
        buySellCostSegment()
    else:
        st.error('Unrecognized segment')

    st.markdown("""---""")
    st.markdown('Want access to detailed data reports - <a href="mailto:gagandeep@mygate.in?Subject=I want detailed reports">Signup here</a>', unsafe_allow_html=True)
    st.markdown('Want to run your own campaigns on a custom segment - <a href="mailto:gagandeep@mygate.in?Subject=I want to run my campaign on a custom segment">Run your campaign</a>', unsafe_allow_html=True)

st.title('Market Insights')
print ('In Market_Insights.py')
render()
