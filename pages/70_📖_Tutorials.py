import os
import sys

import streamlit as st

path2add = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'utils')))
print ('path2add: ', path2add)
if (not (path2add in sys.path)) :
    sys.path.append(path2add)
from utils import metricFn, getLinkedinOauth, highchartGraph


st.title('Tutorials')
st.write('Videos of how you to use the DIY tool')

print ('In Tutorials.py')

if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter():
    st.session_state.count += 1

st.button('Increment', on_click=increment_counter)
st.write('Count = ', st.session_state.count)


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
            text: 'GeoJSON in Highmaps'
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
        
        colorAxis1: {
            tickPixelInterval: 100,
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
"""

# code = """
# Highcharts.chart('container', {});
# """.format(obj)
highchartGraph(obj, theme="light")
