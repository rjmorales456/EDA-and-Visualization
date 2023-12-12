import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
import holoviews as hv
import hvplot.pandas
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
warnings.filterwarnings('ignore')

with st.container():
    st.title("CSDATA06 Applied Data Science with Python: Midterm Project")
    st.write("by: Regolo Jerard L. Morales")
    st.write("Author of Dataset: PETRO")
    st.write("Link to Dataset: https://www.kaggle.com/datasets/piterfm/2022-ukraine-russian-war")
    st.write("Description: This dataset consist of the Equipment Loss and Death Toll, Military Wounded and Prisoners of War from the Russian and Ukraine War 2022.")

# Read datasets
personnel = pd.read_csv("russia_losses_personnel.csv")
equipment = pd.read_csv('russia_losses_equipment.csv')


merge = pd.merge(personnel,equipment,on=('date','day'))
merge.drop(['personnel*','POW'],axis=1,inplace=True)
merge.rename(columns = {'greatest losses direction':'Destroyed Cities'}, inplace = True)
merge['Total Fuel Consumption'] = merge['fuel tank'].combine_first(merge['vehicles and fuel tanks']).astype(float)

merge['date'] = pd.to_datetime(merge['date'])

# Get day week name
merge["Day_Week"] = merge['date'].dt.day_name()
#Get month
merge["Month"] = merge["date"].dt.strftime("%b")

with st.container():
    
    st.write("""
             # Loss of Personnel Over Time
            """)
   
    # st.markdown('### Metrics')
    fig1 = px.line(merge,x='date',y='personnel',width=850,height=400)
    
    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Personnel",
        font=dict(
            
            size=50
            
        )
    )
    st.plotly_chart(fig1)
    st.write("""
             The line graph shows the increase of Personnel loss of the Military as the War agaisnt Russia continues. The graph shows the increase from March 2022 until July 2023.
             """)
with st.container():
    
    st.write("""
             # Equipment Loss Overtime
             """)

    equipment_columns = ['aircraft', 'helicopter', 'tank', 'APC', 'field artillery',
                     'MRL', 'military auto', 'fuel tank', 'drone', 'naval ship',
                     'anti-aircraft warfare', 'special equipment', 'mobile SRBM system',
                     'vehicles and fuel tanks', 'cruise missiles']

    fig2 = px.line(merge,x='date',y=equipment_columns,width=950,height=650)

    fig2.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        legend_title="Equipment",
        font=dict(
            
            size=50
            
        )
    )
    st.plotly_chart(fig2)
    st.write("""
             The line graph shows the different equipment used during the war and the numnber of losses that were accumulated on March 2022 to July 2023. The most equipment that was lost during the war against Russia was the APC or Armored Personnel Carrier and the least equipment that was loss is the Military Auto.
             """)

with st.container():
    
    st.write("""
             # Total Equipment Loss
    """)
    # loss of land, air and water equipments
    aircraft = merge['aircraft'].sum()
    drone = merge['drone'].sum()
    helicopter = merge['helicopter'].sum()
    total_air_equipment = aircraft + drone + helicopter
    
    # Land Equipment
    tank = merge['tank'].sum()
    apc = merge['APC'].sum()
    field_artillery = merge['field artillery'].sum()
    mrl = merge['MRL'].sum()
    military_auto = merge['military auto'].sum()
    anti_aircraft_warfare = merge['anti-aircraft warfare'].sum()
    mobile_srbm_system = merge['mobile SRBM system'].sum()
    total_land_equipment = tank + apc + field_artillery + mrl + military_auto + anti_aircraft_warfare + mobile_srbm_system

    # # Water Equipment
    naval_ship = merge['naval ship'].sum()
    cruise_missiles = merge['cruise missiles'].sum()
    total_water_equipment = naval_ship + cruise_missiles


    # create a dataframe
    total_equipments = pd.DataFrame({
        "Equipments":['Air Equipment', 'Land Equipment', 'Water Equipment'],
        "Total": [total_air_equipment, total_land_equipment, total_water_equipment]
    })

    
    fig3 = px.pie(total_equipments,values='Total',names="Equipments",color_discrete_sequence=px.colors.sequential.haline_r,title="Total Equipment Loss",width=950,height=650)
    fig3.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        legend_title="Equipment",
        font=dict(
            
            size=25
            
        )
    )
    st.plotly_chart(fig3)
    st.write("""
             This pie chart represents the different equipment that was used during the war according to their uses on land, air and water.
             According to the pie chart, the most loss of equipment of the military was on Land Equipment that has a total of 80.6% and the least equipment loss was the Water Equipment that has 4.07%.
             """)
with st.container():
    #Destroyed Cities
    st.write("""
             # Top 10 Destroyed Cities during the war.
            """)
    destroyed_city = merge.groupby(['Destroyed Cities']).size().sort_values(ascending=False).head(10)
    city = pd.DataFrame(destroyed_city,columns=['Count']).reset_index()
    
    fig4 = px.bar(city,x="Destroyed Cities",y='Count',text_auto=True,width=950,height=650)
    fig4.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        legend_title="Top 10 Destroyed City",
        font=dict(
            
            size=25
            
        )
    )
    st.plotly_chart(fig4)
    st.write("""
             The Bar chart shoes the top 10 most citites that were affected and destroyed by the war against Russia. The City Donetsk is the highest affected city next to Bakhmut.
             """)

with st.container():
    # equipment loss per month
    st.write("""
             # Loss of Equipment Per Month
            """)
    equipment_data =  pd.DataFrame({
    "Aircraft":merge['aircraft'],
    "Helicopter":merge['helicopter'],
    "Tank":merge["tank"],
    "APC":merge['APC'],
    "Field Artillery": merge['field artillery'],
    "MRL":merge['MRL'],
    "Military Auto": merge['military auto'],
    "Drone": merge['drone'],
    "Naval Ship": merge['anti-aircraft warfare'],
    "Anti-Aircraft Warefare":merge['anti-aircraft warfare'],
    "Special Equipment": merge['special equipment'],
    "Mobile SRBM System": merge['mobile SRBM system'],
    "Cruise Missiles":merge['cruise missiles'],
    "Month":merge['Month']
})
combined_data = pd.DataFrame(equipment_data.groupby(['Month']).sum().reset_index())

combined_columns = ["Aircraft","Helicopter","Tank","APC","Field Artillery","MRL","Military Auto","Drone","Naval Ship",
                    "Anti-Aircraft Warefare","Special Equipment","Mobile SRBM System","Cruise Missiles"]
fig5 = px.bar(combined_data,x="Month",y=combined_columns,barmode="stack",width=950,height=650)

st.plotly_chart(fig5)
st.write("""
    This Stacked Bar Graph Shows the different equipment that were loss per month during the war against Russia. APC or Armored Personnel Carriers were the most lose equipment during the war.
""")