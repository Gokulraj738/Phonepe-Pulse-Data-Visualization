import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import mysql.connector
import pandas as pd
import json
import requests
import plotly.graph_objects as go




def TranCountAmount(df,Quarter):
    AggTan=df[df["Quarter"]==Quarter]
    AggTan.reset_index(drop=True, inplace=True)

    AggTanVis=AggTan.groupby('State')[['Transaction_count','Transaction_amount']].sum()
    AggTanVis.reset_index(inplace=True)


    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    fig_india_1 = px.choropleth(AggTanVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_amount", color_continuous_scale="Rainbow",
                            range_color=(AggTanVis["Transaction_amount"].min(), AggTanVis["Transaction_amount"].max()),
                            hover_name="State", title=f" TRANSACTION AMOUNT"
                            )
    fig_india_1.update_geos(visible=False, fitbounds="locations")

    st.plotly_chart(fig_india_1, use_container_width=True)

    fig_india_2 = px.choropleth(AggTanVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_count", color_continuous_scale="Rainbow",
                            range_color=(AggTanVis["Transaction_count"].min(), AggTanVis["Transaction_count"].max()),
                            hover_name="State", title=f" TRANSACTION COUNT"
                            )
    fig_india_2.update_geos(visible=False,fitbounds="locations")
    
    st.plotly_chart(fig_india_2, use_container_width=True)


def user(df,state):
    AggUsr=df[df["State"]==state]
    AggUsr.reset_index(drop=True, inplace=True)

    AggUsrVis=AggUsr.groupby('State')[['Count','Percentage']].sum()
    AggUsrVis.reset_index(inplace=True)
    
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    fig_india_2 = px.choropleth(AggUsrVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="Percentage", color_continuous_scale="Rainbow",
                            range_color=(AggUsrVis["Percentage"].min(), AggUsrVis["Percentage"].max()),
                            hover_name="State", title=f" Percentage"
                            )
    fig_india_2.update_geos(visible=False,fitbounds="locations")
    
    st.plotly_chart(fig_india_2, use_container_width=True)



def MapTransc(df, year):
    MapTan=df[df["Year"]==year]
    MapTan.reset_index(drop=True, inplace=True)

    MapTanVis=MapTan.groupby('State')[['Transaction_count','Transaction_amount']].sum()
    MapTanVis.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    fig_india_1 = px.choropleth(MapTanVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_amount", color_continuous_scale="Rainbow",
                            range_color=(MapTanVis["Transaction_amount"].min(), MapTanVis["Transaction_amount"].max()),
                            hover_name="State", title=f" TRANSACTION AMOUNT"
                            )
    fig_india_1.update_geos(visible=False, fitbounds="locations")

    st.plotly_chart(fig_india_1, use_container_width=True)

    fig_india_2 = px.choropleth(MapTanVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_count", color_continuous_scale="Rainbow",
                            range_color=(MapTanVis["Transaction_count"].min(), MapTanVis["Transaction_count"].max()),
                            hover_name="State", title=f" TRANSACTION COUNT"
                            )
    fig_india_2.update_geos(visible=False,fitbounds="locations")
    
    st.plotly_chart(fig_india_2, use_container_width=True)


def MapUsr(df, state):
    Mapusr=df[df["State"]==state]
    Mapusr.reset_index(drop=True, inplace=True)

    MapUsrVis=Mapusr.groupby('State')[['RegisteredUsers','AppOpens']].sum()
    MapUsrVis.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    fig_india_2 = px.choropleth(MapUsrVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="AppOpens", color_continuous_scale="Rainbow",
                            range_color=(MapUsrVis["AppOpens"].min(), MapUsrVis["AppOpens"].max()),
                            hover_name="State", title=f" AppOpens"
                            )
    fig_india_2.update_geos(visible=False,fitbounds="locations")
    
    st.plotly_chart(fig_india_2, use_container_width=True)


def TopTran(df,quarter):
    TopTran=df[df["Quarter"]==quarter]
    TopTran.reset_index(drop=True, inplace=True)

    TopTanVis=TopTran.groupby('State')[['Transaction_count','Transaction_amount']].sum()
    TopTanVis.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    fig_india_1 = px.choropleth(TopTanVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_amount", color_continuous_scale="Rainbow",
                            range_color=(TopTanVis["Transaction_amount"].min(), TopTanVis["Transaction_amount"].max()),
                            hover_name="State", title=f" TRANSACTION AMOUNT"
                            )
    fig_india_1.update_geos(visible=False, fitbounds="locations")

    st.plotly_chart(fig_india_1, use_container_width=True)

    fig_india_2 = px.choropleth(TopTanVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="Transaction_count", color_continuous_scale="Rainbow",
                            range_color=(TopTanVis["Transaction_count"].min(), TopTanVis["Transaction_count"].max()),
                            hover_name="State", title=f" TRANSACTION COUNT"
                            )
    fig_india_2.update_geos(visible=False,fitbounds="locations")
    
    st.plotly_chart(fig_india_2, use_container_width=True)


def TopUsr(df, quarter):
    Topusr=df[df["Quarter"]==quarter]
    Topusr.reset_index(drop=True, inplace=True)

    TopUsrVis=Topusr.groupby('State')['RegisteredUsers'].sum().reset_index()
    

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()

    fig_india_1 = px.choropleth(TopUsrVis, geojson=data1, locations="State", featureidkey="properties.ST_NM",
                            color="RegisteredUsers", color_continuous_scale="Rainbow",
                            range_color=(TopUsrVis["RegisteredUsers"].min(), TopUsrVis["RegisteredUsers"].max()),
                            hover_name="State", title=f" RegisteredUsers"
                            )
    fig_india_1.update_geos(visible=False, fitbounds="locations")

    st.plotly_chart(fig_india_1, use_container_width=True)




