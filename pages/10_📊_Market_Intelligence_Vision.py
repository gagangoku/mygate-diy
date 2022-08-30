import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add, __file__)
if (not (path2add in sys.path)):
    sys.path.append(path2add)
from utils import metricFn, highchartGraph


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

    Tell us what data is interesting to you - [EMAIL US](mailto:gagandeep@mygate.in?Subject=I%20find%20this%20interesting).

    <br/><br/>
    ### DEMO
""", unsafe_allow_html=True)


INDUSTRIES = ['Ecom', 'Food delivery', 'Housing', 'BFSI', 'Automotive', 'Fashion', 'F&B', 'Healthcare']
TIMES = ['last 7 days', 'last 30 days', 'last 3 months']
SEGMENTS = [
    ' ',

    # Industries
    'Food delivery freq - low',
    'Food delivery freq - medium',
    'Food delivery freq - high',

    # Geo
    'closeness to techparks / POI',

    # Owner / tenant
    'home owners',
    'tenants',

    # daily help
    'daily help',
    'maid',
    'cook',
    'nanny',
    'driver',
    'car washer',
    'dog walker',

    # Homes
    'rental cost',
    'buy / sell cost',

    # Location
    'city', 'locality', 'pincode',
]

col1, col2 = st.columns([2, 10])
with col1:
    st.markdown("""
    <div style="font-weight: bold; font-size: 20px; margin-top: 10px;">Industry:</div>
     """, unsafe_allow_html=True)
with col2:
    tabs = st.tabs(INDUSTRIES)


col1, col2, col3 = st.columns([2, 2, 1], gap="small")
with col1:
    seg1 = st.selectbox('Segment 1', SEGMENTS)
with col2:
    seg2 = st.selectbox('Segment 2', SEGMENTS)
with col3:
    seg3 = st.selectbox('Time range', TIMES, index=0)


mapTitle = seg1
obj = """
// Prepare random data
var data = [
    ['DE.SH', 728],
    ['DE.BE', 710],
    ['DE.MV', 963],
    ['DE.HB', 541],
    ['DE.HH', 622],
    ['DE.RP', 866],
    ['DE.SL', 398],
    ['DE.BY', 785],
    ['DE.SN', 223],
    ['DE.ST', 605],
    ['DE.NW', 237],
    ['DE.BW', 157],
    ['DE.HE', 134],
    ['DE.NI', 136],
    ['DE.TH', 704],
    ['DE.', 361]
];
Highcharts.getJSON('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/germany.geo.json', function (geojson) {
    // Initialize the chart
    Highcharts.mapChart('container', {
        chart: {
            map: geojson,
            height: __height__,
            borderWidth: 1,
            borderColor: 'rgba(200, 200, 200, 0.5)',
            marginRight: 20 // for the legend
        },
        title: {
            text: '__title__'
        },
        accessibility: {
            typeDescription: 'Map of Germany.'
        },
        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            floating: true,
            borderColor: 'rgba(255, 255, 255, 1)',
            backgroundColor: 'rgba(255, 255, 255, 1)',
            backgroundColor1: ( // theme
                Highcharts.defaultOptions &&
                Highcharts.defaultOptions.legend &&
                Highcharts.defaultOptions.legend.backgroundColor
            ) || 'rgba(255, 255, 255, 0.85)'
        },
        colorAxis: {
            min: 0,
            max: 1200,
            tickInterval: 400,
            stops: [[0, '#F1EEF6'], [0.65, '#900037'], [1, '#500007']],
            labels: {
                format: '{value}',
            }
        },
        series: [{
            data: data,
            keys: ['code_hasc', 'value'],
            joinBy: 'code_hasc',
            name: 'Random data',
            states: {
                hover: {
                    color: '#a4edba'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.properties.postal}'
            }
        }],
        exporting: {
            enabled: false
        },
    });
});
""".replace('__title__', mapTitle)

# code = """
# Highcharts.chart('container', {});
# """.format(obj)
highchartGraph(obj, theme="light")


st.write('')
colChart = """
Highcharts.chart('container', {
    chart: {
        type: 'bar',
        height: __height__,
        borderWidth: 1,
        borderColor: 'rgba(200, 200, 200, 0.5)',
    },
    title: {
        text: 'Segment split'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: [''],
        title: {
            text: '<b>Distribution</b>',
        },
    },
    yAxis: {
        min: 0,
        max: 200,
        title: {
            text: '<b>Value</b>',
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
    },
    plotOptions: {
        bar: {
            pointWidth: 15,
            dataLabels: {
                enabled: true
            }
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 80,
        floating: true,
        borderWidth: 1,
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
        shadow: true,
    },
    credits: {
        enabled: false
    },
    series: [{
        name: 'Seg 1',
        data: [43]
    }, {
        name: 'Seg 2',
        data: [57]
    }],
    exporting: {enabled: false},
});
"""
highchartGraph(colChart, theme="light", height=300)



colChart = """
Highcharts.chart('container', {
    chart: {
        type: 'column',
        height: __height__,
        borderWidth: 1,
        borderColor: 'rgba(200, 200, 200, 0.5)',
    },
    title: {
        text: 'Distribution by locality'
    },
    xAxis: {
        title: {
            text: '<b>Locality</b>'
        },
        categories: ['HSR', 'Indiranagar', 'Koramangala', 'Whitefield', 'Hebbal']
    },
    yAxis: {
        min: 0,
        title: {
            text: '<b>Distribution</b>'
        },
        stackLabels: {
            enabled: true,
            style: {
                fontWeight: 'bold',
                color: ( // theme
                    Highcharts.defaultOptions.title.style &&
                    Highcharts.defaultOptions.title.style.color
                ) || 'gray',
                textOutline: 'none'
            }
        }
    },
    legend: {
        backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || 'white',
        borderColor: '#CCC',
        borderWidth: 1,
        shadow: false
    },
    tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            dataLabels: {
                enabled: true
            }
        }
    },
    series: [{
        name: 'Seg 1',
        data: [5, 3, 4, 7, 2]
    }, {
        name: 'Seg 2',
        data: [2, 2, 3, 2, 1]
    }],
    exporting: {enabled: false},
});
"""
highchartGraph(colChart, theme="light")
