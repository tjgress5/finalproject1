"""
Name:       TJ Gress
CS230:      Section 5
Data:       Cannabis Registry
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:

This program uses information from an excel file regarding cannabis registry in boston. The goal of the program is to allow users to seek out information
regarding cannabis dispensaries. The user may choose from multiple different choices including license type, business type, and zip code. The program has
charts and maps to allow the user to find the businesses they may be seeking out.
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import numpy as np
from PIL import Image

st.title("Cannabis Registry Information")
st.header("Please use this information to help you find a dispensary that will suit your needs!")
st_image = Image.open("C:/Users/tjgre/PycharmProjects/finalproject/Cannabis_leaf.svg.png")
st.image(st_image, width = 250, caption= "Cannabis Symbol")

tab1, tab2, tab3 = st.tabs(['Businesses by License Type', 'Businesses by Business Type', 'Businesses by Zip Code'])
df_za = pd.read_csv('Cannabis_Registry.csv', index_col='id_full_name')

df_za.rename(columns={"latitude":"lat", "longitude": "lon"}, inplace= True)

df_za = df_za.dropna()

options = ['Active', 'Inactive', 'Both']

def zipcodeseek(zipcode):
    corresponding_values = df_za[df_za['facility_zip_code'] == zipcode]['app_dba_name'].tolist()
    return corresponding_values
def create_map(df, zoom_level=12):
    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=zoom_level,
        pitch=0
    )

    layer1 = pdk.Layer(
        type='ScatterplotLayer',
        data=df,
        get_position='[lon, lat]',
        get_radius=500,
        get_color=[106, 138, 87],
        pickable=True
    )

    layer2 = pdk.Layer(
        type='ScatterplotLayer',
        data=df,
        get_position='[lon, lat]',
        get_radius=100,
        get_color=[177, 35, 185],
        pickable=True
    )

    tool_tip = {
        "html": "Business Name:<br/> <b>{app_dba_name} <b/> ",
        "style": {"backgroundColor": "orange", "color": "white"}
    }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12',
        initial_view_state=view_state,
        layers=[layer1, layer2],
        tooltip=tool_tip
    )

    return map

selected_map = 'Scatter'
with tab1:
   statuses = ['Active', 'Inactive']
   lst = [df_za.loc[df_za['app_license_status'].isin([status])].shape[0] for status in statuses]
   statusdict = {'Active':lst[0],'Inactive':lst[1]}
   def generate_bar_chart(dict):
       plt.figure()
       x = dict.keys()
       y = dict.values()
       plt.bar(x, y)
       plt.xticks(rotation=45)
       plt.ylabel("Amount of Businesses")
       plt.xlabel("License Type")
       plt.title("Amount of Businesses by License Type")
       return plt

   st.pyplot(generate_bar_chart(statusdict))

   df_za_active = df_za[df_za.app_license_status == 'Active']
   st.header("What type of license are you looking for?")
   option = st.radio("", options)
   if option == options[0]:
    st.header('Businesses With Active Licenses Mapped')
    zoom_level = st.slider("Please select the zoom level", 9.0, 15.0, 12.0)
    map_use = create_map(df_za_active, zoom_level)
    st.pydeck_chart(map_use)
    st.header("All Businesses with Active Licenses sorted Alphabetically")
    df_za_new = df_za.set_index("app_business_name")
    df_za_new.sort_values(by='app_dba_name', inplace=True)
    df4 = df_za_new[df_za_new.app_license_status == "Active"][["app_dba_name", "facility_address", "facility_zip_code"]]
    st.write(df4)
   if option == options[1]:
       st.header("Businesses With Inactive Licenses Mapped")
       df_za_inactive = df_za[df_za.app_license_status == 'Inactive']
       if selected_map == "Scatter":
           st.title("Scatterplot map")
       zoom_level = st.slider("Please select the zoom level", 9.0, 15.0, 12.0)
       map_use1 = create_map(df_za_inactive)
       st.pydeck_chart(map_use1)
       st.header("All Businesses with Inactive Licenses sorted Alphabetically")
       df_za_new = df_za.set_index("app_business_name")
       df_za_new.sort_values(by='app_dba_name', inplace=True)
       df4 = df_za_new[df_za_new.app_license_status == "Inactive"][["app_dba_name", "facility_address", "facility_zip_code"]]
       st.write(df4)
   if option == options[2]:
       st.header("Both Businesses With Inactive And Active Licenses Mapped")
       if selected_map == "Scatter":
           st.title("Scatterplot map")
       zoom_level = st.slider("Please select the zoom level", 9.0, 15.0, 12.0)
       map_use2 = create_map(df_za)
       st.pydeck_chart(map_use2)
       st.header("All Businesses split between Active and Inactive Licenses")
       df_za_new = df_za.set_index("app_business_name")
       df_za_new.sort_values(by='app_license_status', inplace=True)
       df4 = df_za_new[["app_dba_name", "app_license_status", "facility_address", "facility_zip_code"]]
       st.write(df4)


with tab2:
   category_list = ['Retail', 'Co-Located', 'Cultivate', 'Operator', 'Manufact', 'Courier']
   catlst = [df_za.loc[df_za['app_license_category'].isin([category])].shape[0] for category in category_list]
   st.title("Proportion of Businesses by Category of License")
   fig, ax = plt.subplots()
   ax.pie(catlst, labels=category_list, autopct='%.2f%%')
   st.pyplot(fig)
   def filter_and_display_data(category, df='df_za'):
        df_za2 = df.set_index("app_business_name")
        df_za2.sort_values(by='app_dba_name', inplace=True)
        df6 = df_za2[df_za2.app_license_category == category][["app_dba_name", "facility_address", "facility_zip_code"]]
        st.write(df6)
   st.header("Category of License")
   catchoice = st.selectbox("What type of business are you looking for", category_list)
   filter_and_display_data(catchoice, df_za)

with tab3:
   st.title("Sort by Zip Code")
   unique = df_za['facility_zip_code'].unique().tolist()
   uniquelist = [str(x) for x in unique]
   uniquelist.sort()
   zip = st.selectbox("Please select a zipcode", uniquelist)
   zipcodedict = {value: zipcodeseek(int(value)) for value in uniquelist}
   business_name = zipcodedict.get(zip)
   bus = ", ".join(business_name)
   if len(business_name) == 1:
    st.header(f"The Zipcode {zip} has 1 store {bus}")
   else:
       st.header(f"The Zipcode {zip} has {len(business_name)} stores {bus}")
   df_za_zip = df_za.set_index("app_dba_name")
   dfzip = df_za_zip[df_za_zip.facility_zip_code == int(zip)][["facility_zip_code", "facility_address", 'app_license_category', 'app_license_status']]
   st.write(dfzip)
   ziplst = [df_za.loc[df_za['facility_zip_code'].isin([int(zippy)])].shape[0] for zippy in uniquelist]
   print(ziplst)
   st.title("Proportion of Businesses by Zipcode")
   fig1, ax1 = plt.subplots()
   ax1.pie(ziplst, labels=uniquelist, autopct='%.2f%%')
   st.pyplot(fig1)
   for i in range(len(uniquelist)):
       n = uniquelist[i]
       z = ziplst[i]
       if z == 1:
           st.write(f"Zipcode {n} contains {z} store")
       else:
           st.write(f"Zipcode {n} contains {z} stores")

