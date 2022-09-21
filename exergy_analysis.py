import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# HEADER
st.header('EXERGY ANALYSIS OF STEAM TURBINE')

st.subheader('Power Plant Components')

base_parameters = {}

# DEFINE COMPONENTS AND HARD CODE BASE VALUES OF EXERGY DESTRUCTION AND EFFICIENCY
component_tuple = ('Boiler Feed Pump', 'Economizer', 'Evaporator', 'Superheater', 
                    'Reheater', 'Condenser', 'High Pressure Turbine', 'Intermediate Pressure Turbine', 'Low Pressure Turbine')
base_values = [[8.632, 0.190], [5.79913, 1.24], [3.5291374, 10.38], [0.0325, 0.80], 
                [0.02705331, 1.122], [354.23, 0.059], [0.065252, 1.49], [0.0825386, 1.75], [69522.83, 1.85] ]

base_parameters = dict(zip(component_tuple, base_values))

component = st.selectbox('Power Plant Components: Select component to be analysed', component_tuple)

'You selected: ', component
"Base parameter for ", component , "is ", base_parameters[component]
 

left_column, right_column = st.columns(2)

# INPUT EXERGY DESTRUCTION AND EFFICIENCY DATA
with left_column:
    st.subheader('Input values for exergy destruction (GJ)')
    a = st.number_input('2015')
    b = st.number_input('2016')
    c = st.number_input('2017')
    d = st.number_input('2018')
    e = st.number_input('2019')

with right_column:
    st.subheader('Input values for exergetic efficiency (%)')
    a1 = st.number_input('2015', key='a1')
    b1 = st.number_input('2016', key='b1')
    c1 = st.number_input('2017', key='c1')
    d1 = st.number_input('2018', key='d1')
    e1 = st.number_input('2019', key='e1')


if not all([a,b,c,d,e,a1,b1,c1,d1,e1]):
    st.write('Please fill in all the necessary fields')


# column1, column2, column3, column4, column5 = st.columns(5)
# rand_number = f'{23} kW'

# column1.metric('My metric', 42, 2) 
# column2.metric('My metric', rand_number, 78)
# column3.metric('My metric', f'{42}kW', 2) 
# column4.metric('My metric', 42, -2) 
# column5.metric('My metric', 42, 2)  

st.text('\n')
    
# VALUES ARE CONSTANT ACROSS ALL COMPONENTS (THERM. EFF. & YEARS OBSERVED)
thermal_efficiency_values = [37.96, 39.77, 38.96, 39.08, 38.81, 38.58]
years = ['.Base', '2015', '2016', '2017', '2018', '2019']

graph_data = {"exergy_destruction":[a,b,c,d,e],
"exergy_efficiency":[a1,b1,c1,d1,e1],
"thermal_efficiency": thermal_efficiency_values
}

# INSERT VALUES OF BASE PARAMETERS
graph_data['exergy_destruction'].insert(0, base_parameters[component][0])
graph_data['exergy_efficiency'].insert(0, base_parameters[component][1])

df = pd.DataFrame(graph_data, index=years)
st.dataframe(df)

st.text('\n')

left_column, right_column = st.columns(2)


alt_df1 = pd.DataFrame({'years': years , 'exergy_destruction': graph_data['exergy_destruction']})
alt_df2 = pd.DataFrame({'years': years , 'exergy_efficiency': graph_data['exergy_efficiency']})


chart1 = alt.Chart(alt_df1).mark_bar().encode(
    x='years',
    y='exergy_destruction'
).properties(width=350)

chart2 = alt.Chart(alt_df2).mark_bar().encode(
    x='years',
    y='exergy_efficiency'
).properties(width=350)

left_column.altair_chart(chart1)
right_column.altair_chart(chart2)

st.line_chart(df)

# PRINT SUCCESS
if all([a,b,c,d,e,a1,b1,c1,d1,e1]):
    st.success('Computed successfully')


hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 