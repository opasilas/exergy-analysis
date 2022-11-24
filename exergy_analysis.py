import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# HEADER
st.header('EXERGY ANALYSIS OF STEAM TURBINE')

st.subheader('Power Plant Components')

active_years = ['2015', '2016', '2017', '2018', '2019']

base_parameters = {}

# DEFINE COMPONENTS AND HARD CODE BASE VALUES OF EXERGY DESTRUCTION AND EFFICIENCY
component_tuple = ('Boiler Feed Pump', 'Economizer', 'Evaporator', 'Superheater', 
                    'Reheater', 'Condenser', 'Turbine')
base_values = [[8.632, 0.190], [5.79913, 1.24], [3.5291374, 10.38], [0.0325, 0.80], 
                [0.02705331, 1.122], [354.23, 0.059], [0.065252, 1.49], [0.0825386, 1.75], [69522.83, 1.85] ]

base_parameters = dict(zip(component_tuple, base_values))

component = st.selectbox('Power Plant Components: Select component to be analysed', component_tuple)

'You selected: ', component
"Base parameter for ", component , "is: ", 'Exergy Destruction',  base_parameters[component][0], 'Exergetic Efficiency: ', base_parameters[component][1]
 
# '''
# HARDCODED DEFAULT VALUES
# Specific heat capacity of water (Cpw)= 4.2kJ/kgk
# Reference temperature of surrounding (To)= (30C+273=303K)
# Specific volume of water (Vw) = 0.0010044m3/kg
# Reference enthropy at surrounding temperature (So)= 0.436kJ/kgK
#  Reference enthalpy at surrounding temperature (ho)= 125.7kJ/kg
# Ratio of chemical exergy of the fuel (c)= 1.06
# Calorific value of natural gas (CV)= 46500kJ/kg
# '''

CPw= 4.2
To = 303
Vw = 0.0010044
So = 0.436
Ho = 125.7
c = 1.06
Cv = 46.5


if component == 'Boiler Feed Pump':
    with st.form("boiler-form"):
        year = st.selectbox('Select year', active_years)

        left, right = st.columns(2)
        with left:
            Twi = st.number_input('Twi')
            Two = st.number_input('Two')
            Pout = st.number_input('Pout')
        with right:
            Pin = st.number_input('Pin')
            Mw = st.number_input('Mw')

        exergy_input = (CPw * (Twi - To)) - (To * np.log(Twi / To))
        exergy_output = (CPw * (Two - To)) - (To * np.log(Two / To))
        pump_work = Mw * Vw * (Pout - Pin)

        bfp_exergy_destruction = (exergy_input - exergy_output) + pump_work
        bfp_exergetic_efficiency = 1 - (bfp_exergy_destruction / pump_work)

        submitted = st.form_submit_button("Calculate")
        if submitted:
            st.write('Year:', year)
            st.write("Boiler Exergy Destruction", round(bfp_exergy_destruction, 3), "Boiler Exergetic Efficiency", round(bfp_exergetic_efficiency, 2))

# def calc(year, bfp_exergy_destruction,bfp_exergetic_efficiency):
#     dic = {'year': [], 'ex_des': [], 'ex_eff': [], 'therm_eff': []}

#     dic['year'].append(year)
#     dic['ex_des'].append(bfp_exergy_destruction)
#     dic['ex_eff'].append(bfp_exergetic_efficiency)
#     return dic


if component == 'Economizer':
    # with st.form("econ-form"):
    year = st.selectbox('Select year', active_years)

    left, right = st.columns(2)
    with left:
        M = st.number_input('M')
        Hout = st.number_input('Hout')
        Hin = st.number_input('Hin')
    with right:
        Sin = st.number_input('Sin')
        Sout = st.number_input('Sout')
        Tin = st.number_input('Tin', value=0.01)

    Q = M * (Hout - Hin) 
    Win = M * ((Hin - Ho) - To * (Sin - So))
    Wout = M * ((Hout - Ho) - To * (Sout - So)) 
    ex_heat = (1 - (To / Tin)) * Q

    econ_exergy_destruction = ex_heat + Win + Wout
    try:
        econ_exergetic_efficiency = Wout / Win
    except ZeroDivisionError:
        econ_exergetic_efficiency = 0
    
    st.write('Year: ', year)
    st.write("Economizer Exergy Destruction", round(econ_exergy_destruction, 3),'GJ', " | Economizer Exergetic Efficiency", round(econ_exergetic_efficiency, 2),'%')

       
if component == 'Evaporator':
    year = st.selectbox('Select year', active_years)

    left, right = st.columns(2)
    with left:
        M = st.number_input('M')
        Hout = st.number_input('Hout')
        Hin = st.number_input('Hin')
    with right:
        Sin = st.number_input('Sin')
        Sout = st.number_input('Sout')
        Cvf = st.number_input('Cvf')

    fuel_exergy = c * Cvf
    Winev = M * ((Hin - Ho) - To * (Sin - So))
    Woutev = M * ((Hout - Ho) - To * (Sout - So)) 
    Q = M * (Hout - Hin) 

    evap_exergy_destruction = fuel_exergy + Winev - Woutev
    try:
        evap_exergetic_efficiency = Woutev / Winev
    except ZeroDivisionError:
        evap_exergetic_efficiency = 0

    st.write('Year: ', year)
    st.write('Evaporator Exergy Destruction', round(evap_exergy_destruction, 3), 'GJ', ' | Evaporator Exergetic Efficiency', round(evap_exergetic_efficiency, 2), '%')


if component == 'Superheater':
    year = st.selectbox('Select year', active_years)

    left, right = st.columns(2)
    with left:
        M = st.number_input('M')
        Hout = st.number_input('Hout')
        Hin = st.number_input('Hin')
    with right:
        Sin = st.number_input('Sin')
        Sout = st.number_input('Sout')
        Tout = st.number_input('Tout')

    Winsu = M * ((Hin - Ho) - To * (Sin - So))
    Woutsu = M * ((Hout - Ho) - To * (Sout - So))
    Q = M * (Hout - Hin)
    try:
        ex_heat_su = (1 - (To / Tout)) * Q
    except ZeroDivisionError:
        ex_heat_su = 0
    super_exergy_destruction = Winsu + ex_heat_su - Woutsu
    try: 
        super_exergetic_efficiency = Woutsu / Winsu
    except ZeroDivisionError:
        super_exergetic_efficiency = 0
    
    st.write('Year: ', year)
    st.write('Superheater Exergy Destruction', round(super_exergy_destruction,3), 'GJ', 'Superheater Exergetic Efficiency', round(super_exergetic_efficiency, 2), '%')


if component == 'Reheater':
    year = st.selectbox('Select year', active_years)

    left, right = st.columns(2)
    with left:
        M = st.number_input('M')
        Hout = st.number_input('Hout')
        Hin = st.number_input('Hin')
    with right:
        Sin = st.number_input('Sin')
        Sout = st.number_input('Sout')
        Tout = st.number_input('Tout')

    Winre = M * ((Hin - Ho) - To * (Sin - So))
    Woutre = M * ((Hout - Ho) - To * (Sout - So))
    Q = M * (Hout - Hin)
    try:
        ex_heat_re = (1 - (To / Tout)) * Q
    except ZeroDivisionError:
        ex_heat_re = 0

    re_exergy_destruction = Winre + ex_heat_re - Woutre
    try:
        re_exergetic_efficiency = 1 - (re_exergy_destruction / Winre)
    except ZeroDivisionError:
        re_exergetic_efficiency = 0
    
    st.write('Year: ', year)
    st.write('Reheater Exergy Destruction', round(re_exergy_destruction, 3), 'GJ', 'Reheater Exergetic Efficiency', round(re_exergetic_efficiency, 2), '%')

if component == 'Condenser':
    year = st.selectbox('Select year', active_years)

    left, right = st.columns(2)
    with left:
        M = st.number_input('M')
        Hout = st.number_input('Hout')
        Hin = st.number_input('Hin')
        Tin = st.number_input('Tin')

    with right:
        Sin = st.number_input('Sin')
        Sout = st.number_input('Sout')
        Tout = st.number_input('Tout')

    Winco = M * ((Hin - Ho) - To * (Sin - So))
    Woutco = M * ((Hout - Ho) - To * (Sout - So))
    Q = M * CPw * (Tin - Tout)
    try:
        ex_heat_co = (1 - (To / Tout)) * Q
    except ZeroDivisionError:
        ex_heat_co = 0

    co_exergy_destruction = Winco - Woutco - ex_heat_co
    try:
        co_exergetic_efficiency = Woutco / Winco
    except ZeroDivisionError:
        co_exergetic_efficiency = 0
    
    st.write('Year: ', year)
    st.write('Condenser Exergy Destruction', round(co_exergy_destruction, 3), 'GJ', 'Condenser Exergetic Efficiency', round(co_exergetic_efficiency, 3), '%')


if component == 'Turbine':
    year = st.selectbox('Select year', active_years)

    left, right = st.columns(2)
    with left:
        M = st.number_input('M')
        Hout = st.number_input('Hout')
        Hin = st.number_input('Hin')
    with right:
        Sin = st.number_input('Sin')
        Sout = st.number_input('Sout')

    Wintu = M * ((Hin - Ho) - To * (Sin - So))
    Wouttu = M * ((Hout - Ho) - To * (Sout - So))
    turbine_work = M * (Hout - Hin)

    tu_exergy_destruction = Wintu - Wouttu - turbine_work
    try:
        tu_exergetic_efficiency = tu_exergy_destruction / (Wintu - Hin)
    except ZeroDivisionError:
        tu_exergetic_efficiency = 0

    st.write('Year: ', year)
    st.write('Turbine Exergy Destruction', round(tu_exergy_destruction, 3), 'GJ', ' | Turbine Exergetic Efficiency', round(tu_exergetic_efficiency, 2), '%')

# CALCULATE THERMAL EFFICIENCY
# thermal_efficency = Wnet / Qin
# Wnet = Hin - Hout

st.subheader('Calculate Overall Thermal Efficiency')
th_year = st.selectbox('Select year', active_years, key='th_year')
M = st.number_input('Mass of steam (M)', key='M')
Hinth = st.number_input('Enthalpy at HP turbine inlet (Hin,hp)', key='Hin')
Houtth = st.number_input('Enthalpy at LP turbine outlet (Hout,lp)', key='Hout')

Wnet = Hinth - Houtth
Qin = M * Cv

try:
    thermal_efficiency = Wnet / Qin
except ZeroDivisionError:
    thermal_efficiency = 0
'Thermal Efficiency for ', th_year, 'is ', round(thermal_efficiency, 3), '%'


left_column, middle_column, right_column = st.columns(3)

# INPUT EXERGY DESTRUCTION AND EFFICIENCY DATA
with left_column:
    st.subheader('Input values for exergy destruction (GJ)')
    a = st.number_input('2015')
    b = st.number_input('2016')
    c = st.number_input('2017')
    d = st.number_input('2018')
    e = st.number_input('2019')

with middle_column:
    st.subheader('Input values for exergetic efficiency (%)')
    a1 = st.number_input('2015', key='a1')
    b1 = st.number_input('2016', key='b1')
    c1 = st.number_input('2017', key='c1')
    d1 = st.number_input('2018', key='d1')
    e1 = st.number_input('2019', key='e1')
    
with right_column:
    st.subheader('Input values for thermal efficiency (%)')
    a2 = st.number_input('2015', key='a')
    b2 = st.number_input('2016', key='b2')
    c2 = st.number_input('2017', key='c2')
    d2 = st.number_input('2018', key='d2')
    e2 = st.number_input('2019', key='e2')


if not all([a,b,c,d,e,a1,b1,c1,d1,e1]):
    st.write('Please fill in all the necessary fields') 

st.text('\n')
    
# VALUES ARE CONSTANT ACROSS ALL COMPONENTS (THERM. EFF. & YEARS OBSERVED)
# thermal_efficiency_values = [37.96, 39.77, 38.96, 39.08, 38.81, 38.58]
years = ['.Base', '2015', '2016', '2017', '2018', '2019']

graph_data = {"exergy_destruction":[a,b,c,d,e],
"exergy_efficiency":[a1,b1,c1,d1,e1],
"thermal_efficiency": [a2,b2,c2,d2,e2]
}

# INSERT VALUES OF BASE PARAMETERS
graph_data['exergy_destruction'].insert(0, base_parameters[component][0])
graph_data['exergy_efficiency'].insert(0, base_parameters[component][1])
graph_data['thermal_efficiency'].insert(0, 37.96)

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

