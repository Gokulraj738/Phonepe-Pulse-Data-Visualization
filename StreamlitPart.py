import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import mysql.connector
import pandas as pd
import json

import requests

from PIL import Image
import plotly.graph_objects as go


from GeoVisual import TranCountAmount
from GeoVisual import user
from GeoVisual import MapTransc
from GeoVisual import MapUsr
from GeoVisual import TopTran
from GeoVisual import TopUsr
from PhonepedataProcess import Agg_user
from PhonepedataProcess import map_transaction
from PhonepedataProcess import map_User
from PhonepedataProcess import top_transaction
from PhonepedataProcess import top_User

def execute_query(query):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="CSKtsk@738",
        database="PhonepeProject"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    conn.close()
    return df

conn=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="CSKtsk@738",
    database='PhonepeProject'
)
mycursor=conn.cursor()

mycursor.execute('select * from aggregratetransactions')
Aggregratetrantable=mycursor.fetchall()
conn.commit()
Aggre_Tran=pd.DataFrame(Aggregratetrantable, columns=('State','Year','Quarter','Transaction_type',
                                                  'Transaction_count','Transaction_amount'))
Aggre_Tran['Transaction_count'] = Aggre_Tran['Transaction_count'].astype(int)
Aggre_Tran7= Aggre_Tran.to_csv("output.csv", index=False)

mycursor.execute('select * from aggregrateusers')
Aggregrateusertable=mycursor.fetchall()
conn.commit()
Aggre_User=pd.DataFrame(Aggregrateusertable, columns=('State','Year','Quarter','Brand',
                                                  'Count','Percentage'))
Aggre_User['Count'] = Aggre_User['Count'].astype(int)

mycursor.execute('select * from maptransactions')
Maptrantable=mycursor.fetchall()
conn.commit()
Map_Tran=pd.DataFrame(Maptrantable, columns=('State','Year','Quarter','Districts',
                                                  'Transaction_count','Transaction_amount'))
Map_Tran['Transaction_count'] = Map_Tran['Transaction_count'].astype(int)

mycursor.execute('select * from mapusers')
Mapusertable=mycursor.fetchall()
conn.commit()
Map_User=pd.DataFrame(Mapusertable, columns=('State','Year','Quarter','Districts',
                                                  'RegisteredUsers','AppOpens'))



mycursor.execute('select * from toptransactions')
Toptrantable=mycursor.fetchall()
conn.commit()
Top_Tran=pd.DataFrame(Toptrantable, columns=('State','Year','Quarter','Pincodes',
                                                  'Transaction_count','Transaction_amount'))
Top_Tran['Transaction_count'] = Top_Tran['Transaction_count'].astype(int)

mycursor.execute('select * from topusers')
Topusertable=mycursor.fetchall()
conn.commit()
Top_User=pd.DataFrame(Topusertable, columns=('State','Year','Quarter','Pincodes',
                                                  'RegisteredUsers'))


def display_bar_chart(data, x, y, title):
    fig = px.bar(data, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)


def display_pie_chart(data, values, names, title):
    fig = px.pie(data, values=values, names=names, title=title)
    st.plotly_chart(fig, use_container_width=True)


def display_line_chart(data, x, y, title):
    fig = px.line(data, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)


def display_horizontal_bar_chart(data, x, y, title):
    fig = px.bar(data, x=x, y=y, orientation='h', title=title)
    st.plotly_chart(fig, use_container_width=True)


def display_area_chart(data, x, y, title):
    fig = px.area(data, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)

def main():
    icon = Image.open("C:/Users/Hp/Downloads/1587055421792.jpg")
    st.set_page_config(layout="wide")
    st.markdown(
        ''' 
        <style> 
        body {
            background-image: url("C:/Users/Hp/Downloads/1587055421792.jpg");
            background-size: cover;
            }
            </style>
            ''',
    unsafe_allow_html=True
    
    )


    st.markdown("<h1 style='color: violet;'>Phonepe Pulse Data Visualization and Exploration</h1>", unsafe_allow_html=True)

    st.write("")

    with st.sidebar:
       Select = option_menu("Main Menu",["Home", "Data Exploration Settings", 'Queries','Visualization'])

    if Select == 'Home':
        st.header('Welcome')
        
         
    elif Select == "Data Exploration Settings":
        tab1, tab2, tab3 = st.tabs(["Aggregrate Functions", "Map Functions", "Top Function"])

        with tab1:
                if tab1:
                    method = option_menu('Select the Function',['Aggregrate Transactions', 'Aggregrate Users'], key='aggregrate_function')

                    if method == 'Aggregrate Transactions':
                        with st.expander('States'):
                            state_method = option_menu('Select State Queries',['Sum Queries', 'Average Queries'], key='Sum Queries')

                            if state_method == 'Sum Queries':

                                Agg_Tran_state_Query1 = execute_query("SELECT State, SUM(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions GROUP BY State;")
                                Data1 = pd.DataFrame(Agg_Tran_state_Query1, columns=['State', "Transaction_count"])
                                st.write("Total No.of Sum ---- Transaction Count by State:")
                                st.write(Agg_Tran_state_Query1)
                                display_bar_chart(Agg_Tran_state_Query1, x='State', y='Total_Transaction_Count', title='Sum Transaction Count by State')

                                Agg_Tran_state_Query2 = execute_query("SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount FROM aggregratetransactions GROUP BY State;")
                                st.write("Total No.of Sum ---- Transaction Amount by State:")
                                st.write(Agg_Tran_state_Query2)
                                display_bar_chart(Agg_Tran_state_Query2, x='State', y='Total_Transaction_Amount', title='Sum Transaction Amount by State')

                            elif state_method == 'Average Queries':

                                Agg_Tran_state_Query3 = execute_query("SELECT State, avg(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions GROUP BY State;")
                                st.write("Total No.of avg ---- Transaction Count by State:")
                                st.write(Agg_Tran_state_Query3)
                                display_bar_chart(Agg_Tran_state_Query3, x='State', y='Total_Transaction_Count', title='Avg Transaction Count by State')

                                Agg_Tran_state_Query4 = execute_query("SELECT State, avg(Transaction_amount) AS Total_Transaction_Amount FROM aggregratetransactions GROUP BY State;")
                                st.write("Total No.of avg ---- Transaction Amount by State:")
                                st.write(Agg_Tran_state_Query4)
                                display_bar_chart(Agg_Tran_state_Query4, x='State', y='Total_Transaction_Amount', title='Avg Transaction Amount by State')

                            else:
                                pass

                        with st.expander('Years'):
                            year_method = option_menu('Select Years',['2018','2019','2020','2021','2022','2023'],key='Years')

                            if year_method == '2018':
                                Agg_Tran_year_Query1 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions where year = '2018' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(Agg_Tran_year_Query1)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query1['Year'], y=Agg_Tran_year_Query1['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                Agg_Tran_year_Query2 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM aggregratetransactions WHERE Year = '2018' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(Agg_Tran_year_Query2)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query2['Year'], y=Agg_Tran_year_Query2['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2019':
                                Agg_Tran_year_Query3 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions where year = '2019' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(Agg_Tran_year_Query3)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query3['Year'], y=Agg_Tran_year_Query3['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                Agg_Tran_year_Query4 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM aggregratetransactions WHERE Year = '2019' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(Agg_Tran_year_Query4)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query4['Year'], y=Agg_Tran_year_Query4['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2020':
                                Agg_Tran_year_Query5 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions where year = '2020' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(Agg_Tran_year_Query5)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query5['Year'], y=Agg_Tran_year_Query5['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                Agg_Tran_year_Query6 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM aggregratetransactions WHERE Year = '2020' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(Agg_Tran_year_Query6)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query6['Year'], y=Agg_Tran_year_Query6['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2021':
                                Agg_Tran_year_Query7 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions where year = '2021' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(Agg_Tran_year_Query7)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query7['Year'], y=Agg_Tran_year_Query7['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                Agg_Tran_year_Query8 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM aggregratetransactions WHERE Year = '2021' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(Agg_Tran_year_Query8)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query8['Year'], y=Agg_Tran_year_Query8['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2022':
                                Agg_Tran_year_Query9 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions where year = '2022' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(Agg_Tran_year_Query9)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query9['Year'], y=Agg_Tran_year_Query9['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                Agg_Tran_year_Query10 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM aggregratetransactions WHERE Year = '2022' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(Agg_Tran_year_Query10)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query10['Year'], y=Agg_Tran_year_Query10['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2023':
                                Agg_Tran_year_Query11 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM aggregratetransactions where year = '2023' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(Agg_Tran_year_Query11)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query11['Year'], y=Agg_Tran_year_Query11['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                Agg_Tran_year_Query12 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM aggregratetransactions WHERE Year = '2023' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(Agg_Tran_year_Query12)
                                fig = go.Figure(data=go.Scatter(x=Agg_Tran_year_Query12['Year'], y=Agg_Tran_year_Query12['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            else:
                                pass

                        with st.expander('Quarters'):
                            Quarter_method = option_menu('Select Quarter Queries',['Sum Queries', 'Average Queries'], key = 'Quarter Queries')

                            if Quarter_method == 'Sum Queries':
                                Agg_Tran_Quarter_Query1 = execute_query('select Quarter, sum(Transaction_count) as Total_Transaction_Count from aggregratetransactions group by Quarter')
                                st.write('Total No.of Sum ----  Transaction Count by Quarter')
                                st.write(Agg_Tran_Quarter_Query1)
                                display_bar_chart(Agg_Tran_Quarter_Query1, x='Quarter', y='Total_Transaction_Count', title='Sum Transaction Count by Quarter')

                                Agg_Tran_Quarter_Query2  = execute_query('select Quarter, sum(Transaction_amount) as Total_Transaction_Amount from aggregratetransactions group by Quarter')
                                st.write('Total No.of Sum ---- Transaction Amount by Quarter')
                                st.write(Agg_Tran_Quarter_Query2)
                                display_bar_chart(Agg_Tran_Quarter_Query2, x='Quarter', y='Total_Transaction_Amount', title='Sum Transaction Amount by Quarter')

                            elif Quarter_method == 'Average Queries':

                                Agg_Tran_Quarter_Query3 = execute_query('select Quarter, avg(Transaction_count) as Total_Transaction_Count from aggregratetransactions group by Quarter')
                                st.write('Total No.of avg ----  Transaction Count by Quarter')
                                st.write(Agg_Tran_Quarter_Query3)
                                display_bar_chart(Agg_Tran_Quarter_Query3, x='Quarter', y='Total_Transaction_Count', title='Avg Transaction Count by Quarter')
                                
                                Agg_Tran_Quarter_Query4  = execute_query('select Quarter, avg(Transaction_amount) as Total_Transaction_Amount from aggregratetransactions group by Quarter')
                                st.write('Total No.of avg ---- Transaction Amount by Quarter')
                                st.write(Agg_Tran_Quarter_Query4)
                                display_bar_chart(Agg_Tran_Quarter_Query4, x='Quarter', y='Total_Transaction_Amount', title='Avg Transaction Amount by Quarter')

                            else:
                                pass

                    elif method == 'Aggregrate Users':
                        with st.expander('Brands'):
                            brand_method = option_menu('Select Brand Queries',['Sum Queries', 'Average Queries'], key='Brand Queries')
                            if brand_method == 'Sum Queries':
                                Agg_User_Brabd_query1 = execute_query("SELECT Brand, sum(Transaction_count) AS Total_Transaction_Count FROM aggregrateusers  GROUP BY Brand;")
                                st.write("Sum Total Transaction Count by Brand:")
                                st.write(Agg_User_Brabd_query1)
                                display_pie_chart(Agg_User_Brabd_query1, values='Total_Transaction_Count', names='Brand', title='Sum Total Transaction Count by Brand')

                            elif brand_method == 'Average Queries':
                                Agg_User_Brabd_query2 = execute_query("SELECT Brand, AVG(Percentage) AS Average_Percentage_Users FROM aggregrateusers  GROUP BY Brand;")
                                st.write("Average Percentage of Users by Brand:")
                                st.write(Agg_User_Brabd_query2)
                                display_pie_chart(Agg_User_Brabd_query2, values='Average_Percentage_Users', names='Brand', title='Average Percentage of Users by Brand')

                            else:
                                pass

                        with st.expander('States'):
                                Agg_User_State_query1 = execute_query("SELECT State, Brand, SUM(Transaction_count) AS Total_Transaction_Count, avg(Transaction_count) as Avg_Transaction_Count FROM aggregrateusers GROUP BY State, Brand;")
                                st.write("State and Brand Analysis - Total Transaction Count:")
                                st.write(Agg_User_State_query1)
                                display_bar_chart(Agg_User_State_query1, x='State', y='Total_Transaction_Count', title='Total Transaction Count by State and Brand')
                                display_bar_chart(Agg_User_State_query1, x='Brand', y='Avg_Transaction_Count', title='Average Transaction Count by State and Brand')

                        with st.expander('Quarters'):
                            Agg_Useer_Quarter_Query1 = execute_query('select Quarter, Brand, sum(Transaction_count) as Total_Transaction_Count, avg(Transaction_count) as Avg_Transaction_Count from aggregrateusers group by Quarter, Brand')
                            st.write('Total No.of Sum and Average ----  Transaction Count by Quarter')
                            st.write(Agg_Useer_Quarter_Query1)
                            display_bar_chart(Agg_Useer_Quarter_Query1, x='Quarter', y='Total_Transaction_Count', title='Sum Transaction Count by Quarter and Brand')
                            display_bar_chart(Agg_Useer_Quarter_Query1, x='Brand', y='Avg_Transaction_Count', title='Average Transaction Count by Quarter and Brand')

        with tab2:
                if tab2:
                    method = option_menu('Select the Function',['Map Transactions', 'Map Users'])
                    if method == 'Map Transactions':
                        with st.expander('States'):
                            method = option_menu('Select State Queries',['Sum Queries', 'Average Queries'], key ='State Queries')
                            if method == 'Sum Queries':
                                map_tran_state_Query1 = execute_query("SELECT State,Year,Quarter,Districts, SUM(Transaction_count) AS Total_Transaction_Count FROM maptransactions GROUP BY State,Year,Quarter,Districts;")
                                st.write("Total No.of Sum and Average ---- Transaction Count, Amount by State,Year,Quarter,Districts:")
                                st.write(map_tran_state_Query1)
                                display_bar_chart(map_tran_state_Query1, x='State', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Districts')
                                display_bar_chart(map_tran_state_Query1, x='Quarter', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Districts')
                                display_bar_chart(map_tran_state_Query1, x='Year', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Districts')
                                display_bar_chart(map_tran_state_Query1, x='Districts', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Districts')
                            
                            elif method == 'Average Queries':
                                map_tran_state_Query2 = execute_query("SELECT State,Year,Quarter,Districts, avg(Transaction_amount) as Average_Transaction_Amount FROM maptransactions GROUP BY State,Year,Quarter,Districts;")
                                st.write("Total No.of Average ---- Transaction Count, Amount by State,Year,Quarter,Districts:")
                                st.write(map_tran_state_Query2)
                                display_bar_chart(map_tran_state_Query2, x='State', y='Average_Transaction_Amount', title='Average Transaction Count by State,Year,Quarter,Districts')
                                display_bar_chart(map_tran_state_Query2, x='Quarter', y='Average_Transaction_Amount', title='Avegare Transaction Count by State,Year,Quarter,Districts')
                                display_bar_chart(map_tran_state_Query2, x='Year', y='Average_Transaction_Amount', title='Average Transaction Count by State,Year,Quarter,Districts')
                                display_bar_chart(map_tran_state_Query2, x='Districts', y='Average_Transaction_Amount', title='Average Transaction Count by State,Year,Quarter,Districts')

                            else:
                                pass

                        with st.expander('Districts'):
                            map_tran_dis_query = execute_query("SELECT Districts, MAX(Transaction_count) AS Total_Transaction_Count FROM maptransactions GROUP BY Districts;")
                            st.write("Total Highest No.of ---- Transaction Count by Districts:")
                            st.write(map_tran_dis_query)
                            display_bar_chart(map_tran_dis_query, x='Districts', y='Total_Transaction_Count', title='Max Transaction Count by Districts')

                        with st.expander('Years'):
                            year_method = option_menu('Select Year Queries',['2018','2019','2020','2021','2022','2023'],key='Year Queries')
                            if year_method == '2018':
                                map_tran_year_Query1 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM maptransactions where year = '2018' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(map_tran_year_Query1)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query1['Year'], y=map_tran_year_Query1['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                map_tran_year_Query2 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM maptransactions WHERE Year = '2018' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(map_tran_year_Query2)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query2['Year'], y=map_tran_year_Query2['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2019':
                                map_tran_year_Query3 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM maptransactions where year = '2019' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(map_tran_year_Query3)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query3['Year'], y=map_tran_year_Query3['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                map_tran_year_Query4 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM maptransactions WHERE Year = '2019' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(map_tran_year_Query4)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query4['Year'], y=map_tran_year_Query4['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2020':
                                map_tran_year_Query5 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM maptransactions where year = '2020' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(map_tran_year_Query5)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query5['Year'], y=map_tran_year_Query5['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                map_tran_year_Query6 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM maptransactions WHERE Year = '2020' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(map_tran_year_Query6)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query6['Year'], y=map_tran_year_Query6['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2021':
                                map_tran_year_Query7 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM maptransactions where year = '2021' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(map_tran_year_Query7)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query7['Year'], y=map_tran_year_Query7['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                map_tran_year_Query8 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM maptransactions WHERE Year = '2021' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(map_tran_year_Query8)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query8['Year'], y=map_tran_year_Query8['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2022':
                                map_tran_year_Query9 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM maptransactions where year = '2022' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(map_tran_year_Query9)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query9['Year'], y=map_tran_year_Query9['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                map_tran_year_Query10 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM maptransactions WHERE Year = '2022' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(map_tran_year_Query10)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query10['Year'], y=map_tran_year_Query10['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2023':
                                map_tran_year_Query11 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM maptransactions where year = '2023' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(map_tran_year_Query11)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query11['Year'], y=map_tran_year_Query11['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                map_tran_year_Query12 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM maptransactions WHERE Year = '2023' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(map_tran_year_Query12)
                                fig = go.Figure(data=go.Scatter(x=map_tran_year_Query12['Year'], y=map_tran_year_Query12['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            else:
                                pass

                        with st.expander('Quarters'):
                            Quarter_method = option_menu('Select Quarter Queries',['Sum Queries', 'Average Queries'], key = 'map Quarter Queries')

                            if Quarter_method == 'Sum Queries':
                                map_tran_Quarter_Query1 = execute_query('select Quarter, sum(Transaction_count) as Total_Transaction_Count from maptransactions group by Quarter')
                                st.write('Total No.of Sum ----  Transaction Count by Quarter')
                                st.write(map_tran_Quarter_Query1)
                                display_bar_chart(map_tran_Quarter_Query1, x='Quarter', y='Total_Transaction_Count', title='Sum Transaction Count by Quarter')

                                map_tran_Quarter_Query2  = execute_query('select Quarter, sum(Transaction_amount) as Total_Transaction_Amount from maptransactions group by Quarter')
                                st.write('Total No.of Sum ---- Transaction Amount by Quarter')
                                st.write(map_tran_Quarter_Query2)
                                display_bar_chart(map_tran_Quarter_Query2, x='Quarter', y='Total_Transaction_Amount', title='Sum Transaction Amount by Quarter')

                            elif Quarter_method == 'Average Queries':

                                map_tran_Quarter_Query3 = execute_query('select Quarter, avg(Transaction_count) as Total_Transaction_Count from maptransactions group by Quarter')
                                st.write('Total No.of avg ----  Transaction Count by Quarter')
                                st.write(map_tran_Quarter_Query3)
                                display_bar_chart(map_tran_Quarter_Query3, x='Quarter', y='Total_Transaction_Count', title='Avg Transaction Count by Quarter')
                                
                                map_tran_Quarter_Query4  = execute_query('select Quarter, avg(Transaction_amount) as Total_Transaction_Amount from maptransactions group by Quarter')
                                st.write('Total No.of avg ---- Transaction Amount by Quarter')
                                st.write(map_tran_Quarter_Query4)
                                display_bar_chart(map_tran_Quarter_Query4, x='Quarter', y='Total_Transaction_Amount', title='Avg Transaction Amount by Quarter')

                            else:
                                pass
                    
                    elif method == 'Map Users':
                        with st.expander('States'):
                            map_user_State_query1 = execute_query("SELECT State, Quarter,Districts, SUM(RegisteredUsers) AS Total_Registered_Users, sum(AppOpens) as Total_AppOpens FROM mapusers GROUP BY State, Quarter, Districts;")
                            st.write("State, Quarter and Districts - Total RegisteredUsers and Total AppOpens:")
                            st.write(map_user_State_query1)
                            display_bar_chart(map_user_State_query1, x='State', y='Total_Registered_Users', title='Total Registered Users by State and Quarter')
                            display_bar_chart(map_user_State_query1, x='Quarter', y='Total_AppOpens', title='Total AppOpens by State and Districts')

                        with st.expander('Years'):
                            year_method = option_menu('Select Year Queries',['2018','2019','2020','2021','2022','2023'],key='map Year Queries')
                            if year_method == '2018':
                                map_user_year_Query1 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM mapusers where year = '2018' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(map_user_year_Query1)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query1['Year'], y=map_user_year_Query1['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                                map_user_year_Query2 = execute_query("SELECT Year, AVG(AppOpens) AS Average_App_Opens FROM mapusers WHERE Year = '2018' GROUP BY Year;")
                                st.write("Average App Opens by Year:")
                                st.write(map_user_year_Query2)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query2['Year'], y=map_user_year_Query2['Average_App_Opens'], mode='lines+markers'))
                                fig.update_layout(title='Average App Opens by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average App Opens')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2019':
                                map_user_year_Query3 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM mapusers where year = '2019' GROUP BY Year;")
                                st.write("Total No.of---- Total Registered Users by Year:")
                                st.write(map_user_year_Query3)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query3['Year'], y=map_user_year_Query3['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                                map_user_year_Query4 = execute_query("SELECT Year, AVG(AppOpens) AS Average_App_Opens FROM mapusers WHERE Year = '2019' GROUP BY Year;")
                                st.write("Average App Opens by Year:")
                                st.write(map_user_year_Query4)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query4['Year'], y=map_user_year_Query4['Average_App_Opens'], mode='lines+markers'))
                                fig.update_layout(title='Average App Opens by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average App Opens')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2020':
                                map_user_year_Query5 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM mapusers where year = '2020' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(map_user_year_Query5)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query5['Year'], y=map_user_year_Query5['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                                map_user_year_Query6 = execute_query("SELECT Year, AVG(AppOpens) AS Average_App_Opens FROM mapusers WHERE Year = '2020' GROUP BY Year;")
                                st.write("Average App Opens by Year:")
                                st.write(map_user_year_Query6)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query6['Year'], y=map_user_year_Query6['Average_App_Opens'], mode='lines+markers'))
                                fig.update_layout(title='Average App Opens by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average App Opens')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2021':
                                map_user_year_Query7 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM mapusers where year = '2021' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(map_user_year_Query7)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query7['Year'], y=map_user_year_Query7['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                                map_user_year_Query8 = execute_query("SELECT Year, AVG(AppOpens) AS Average_App_Opens FROM mapusers WHERE Year = '2021' GROUP BY Year;")
                                st.write("Average App Opens by Year:")
                                st.write(map_user_year_Query8)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query8['Year'], y=map_user_year_Query8['Average_App_Opens'], mode='lines+markers'))
                                fig.update_layout(title='Average App Opens by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average App Opens')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2022':
                                map_user_year_Query9 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM mapusers where year = '2022' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(map_user_year_Query9)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query9['Year'], y=map_user_year_Query9['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                                map_user_year_Query10 = execute_query("SELECT Year, AVG(AppOpens) AS Average_App_Opens FROM mapusers WHERE Year = '2022' GROUP BY Year;")
                                st.write("Average App Opens by Year:")
                                st.write(map_user_year_Query10)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query10['Year'], y=map_user_year_Query10['Average_App_Opens'], mode='lines+markers'))
                                fig.update_layout(title='Average App Opens by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average App Opens')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2023':
                                map_user_year_Query11 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM mapusers where year = '2023' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(map_user_year_Query11)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query11['Year'], y=map_user_year_Query11['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                                map_user_year_Query12 = execute_query("SELECT Year, AVG(AppOpens) AS Average_App_Opens FROM mapusers WHERE Year = '2023' GROUP BY Year;")
                                st.write("Average App Opens by Year:")
                                st.write(map_user_year_Query12)
                                fig = go.Figure(data=go.Scatter(x=map_user_year_Query12['Year'], y=map_user_year_Query12['Average_App_Opens'], mode='lines+markers'))
                                fig.update_layout(title='Averag eApp Opens by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average App Opens')
                                st.plotly_chart(fig, use_container_width=True)

                            else:
                                pass
        
        with tab3:
                if tab3:
                    method = option_menu('Select the Function',['Top Transactions', 'Top Users'])
                    if method == 'Top Transactions':
                        with st.expander('States'):
                            method = option_menu('Select State Queries',['Sum Queries', 'Average Queries'], key ='top State Queries')
                            if method == 'Sum Queries':
                                top_tran_state_Query1 = execute_query("SELECT State,Year,Quarter,Pincodes, SUM(Transaction_count) AS Total_Transaction_Count FROM toptransactions GROUP BY State,Year,Quarter,Pincodes;")
                                st.write("Total No.of Sum ---- Transaction Count, Amount by State,Year,Quarter,Pincodes:")
                                st.write(top_tran_state_Query1)
                                display_bar_chart(top_tran_state_Query1, x='State', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Pincodes')
                                display_bar_chart(top_tran_state_Query1, x='Quarter', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Pincodes')
                                display_bar_chart(top_tran_state_Query1, x='Year', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Pincodes')
                                display_bar_chart(top_tran_state_Query1, x='Pincodes', y='Total_Transaction_Count', title='Sum Transaction Count by State,Year,Quarter,Pincodes')
                            
                            elif method == 'Average Queries':
                                top_tran_state_Query2 = execute_query("SELECT State,Year,Quarter,Pincodes, avg(Transaction_amount) as Average_Transaction_Amount FROM toptransactions GROUP BY State,Year,Quarter,Pincodes;")
                                st.write("Total No.of Average ---- Transaction Count, Amount by State,Year,Quarter,Pincodes:")
                                st.write(top_tran_state_Query2)
                                display_bar_chart(top_tran_state_Query2, x='State', y='Average_Transaction_Amount', title='Average Transaction Count by State,Year,Quarter,Pincodes')
                                display_bar_chart(top_tran_state_Query2, x='Quarter', y='Average_Transaction_Amount', title='Avegare Transaction Count by State,Year,Quarter,Pincodes')
                                display_bar_chart(top_tran_state_Query2, x='Year', y='Average_Transaction_Amount', title='Average Transaction Count by State,Year,Quarter,Pincodes')
                                display_bar_chart(top_tran_state_Query2, x='Pincodes', y='Average_Transaction_Amount', title='Average Transaction Count by State,Year,Quarter,Pincodes')

                            else:
                                pass

                        with st.expander('Years'):
                            year_method = option_menu('Select Year Queries',['2018','2019','2020','2021','2022','2023'],key='top Year Queries')
                            if year_method == '2018':
                                top_tran_year_Query1 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM toptransactions where year = '2018' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(top_tran_year_Query1)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query1['Year'], y=top_tran_year_Query1['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                top_tran_year_Query2 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM toptransactions WHERE Year = '2018' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(top_tran_year_Query2)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query2['Year'], y=top_tran_year_Query2['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2019':
                                top_tran_year_Query3 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM toptransactions where year = '2019' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(top_tran_year_Query3)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query3['Year'], y=top_tran_year_Query3['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                top_tran_year_Query4 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM toptransactions WHERE Year = '2019' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(top_tran_year_Query4)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query4['Year'], y=top_tran_year_Query4['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2020':
                                top_tran_year_Query5 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM toptransactions where year = '2020' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(top_tran_year_Query5)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query5['Year'], y=top_tran_year_Query5['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                top_tran_year_Query6 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM toptransactions WHERE Year = '2020' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(top_tran_year_Query6)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query6['Year'], y=top_tran_year_Query6['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2021':
                                top_tran_year_Query7 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM toptransactions where year = '2021' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(top_tran_year_Query7)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query7['Year'], y=top_tran_year_Query7['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                top_tran_year_Query8 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM toptransactions WHERE Year = '2021' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(top_tran_year_Query8)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query8['Year'], y=top_tran_year_Query8['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2022':
                                top_tran_year_Query9 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM toptransactions where year = '2022' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(top_tran_year_Query9)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query9['Year'], y=top_tran_year_Query9['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                top_tran_year_Query10 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM toptransactions WHERE Year = '2022' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(top_tran_year_Query10)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query10['Year'], y=top_tran_year_Query10['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2023':
                                top_tran_year_Query11 = execute_query("SELECT Year, SUM(Transaction_count) AS Total_Transaction_Count FROM toptransactions where year = '2023' GROUP BY Year;")
                                st.write("Total No.of Sum ---- Transaction Count by Year:")
                                st.write(top_tran_year_Query11)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query11['Year'], y=top_tran_year_Query11['Total_Transaction_Count'], mode='lines+markers'))
                                fig.update_layout(title='Sum Transaction Count by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Transaction Count')
                                st.plotly_chart(fig, use_container_width=True)

                                top_tran_year_Query12 = execute_query("SELECT Year, AVG(Transaction_amount) AS Average_Transaction_Amount FROM toptransactions WHERE Year = '2023' GROUP BY Year;")
                                st.write("Average Transaction Amount by Year:")
                                st.write(top_tran_year_Query12)
                                fig = go.Figure(data=go.Scatter(x=top_tran_year_Query12['Year'], y=top_tran_year_Query12['Average_Transaction_Amount'], mode='lines+markers'))
                                fig.update_layout(title='Average Transaction Amount by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Average Transaction Amount')
                                st.plotly_chart(fig, use_container_width=True)

                            else:
                                pass
                    
                    elif method == 'Top Users':
                        with st.expander('States'):
                            top_user_state_query1 = execute_query("SELECT State, Quarter,Pincodes, SUM(RegisteredUsers) AS Total_Registered_Users FROM topusers GROUP BY State, Quarter, Pincodes;")
                            st.write("State, Quarter and Districts - Total RegisteredUsers:")
                            st.write(top_user_state_query1)
                            display_bar_chart(top_user_state_query1, x='State', y='Total_Registered_Users', title='Total Registered Users by State')
                            display_bar_chart(top_user_state_query1, x='Quarter', y='Total_Registered_Users', title='Total Registered Users by Quarter')

                        with st.expander('Years'):
                            year_method = option_menu('Select Year Queries',['2018','2019','2020','2021','2022','2023'],key='top Year Queries')
                            if year_method == '2018':
                                top_user_year_Query1 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM topusers where year = '2018' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(top_user_year_Query1)
                                fig = go.Figure(data=go.Scatter(x=top_user_year_Query1['Year'], y=top_user_year_Query1['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2019':
                                top_user_year_Query2 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM topusers where year = '2019' GROUP BY Year;")
                                st.write("Total No.of---- Total Registered Users by Year:")
                                st.write(top_user_year_Query2)
                                fig = go.Figure(data=go.Scatter(x=top_user_year_Query2['Year'], y=top_user_year_Query2['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2020':
                                top_user_year_Query3 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM topusers where year = '2020' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(top_user_year_Query3)
                                fig = go.Figure(data=go.Scatter(x=top_user_year_Query3['Year'], y=top_user_year_Query3['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2021':
                                top_user_year_Query4 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM topusers where year = '2021' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(top_user_year_Query4)
                                fig = go.Figure(data=go.Scatter(x=top_user_year_Query4['Year'], y=top_user_year_Query4['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2022':
                                top_user_year_Query5 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM topusers where year = '2022' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(top_user_year_Query5)
                                fig = go.Figure(data=go.Scatter(x=top_user_year_Query5['Year'], y=top_user_year_Query5['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users by Year',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                            elif year_method == '2023':
                                top_user_year_Query6 = execute_query("SELECT Year, SUM(RegisteredUsers) AS Total_Registered_user FROM topusers where year = '2023' GROUP BY Year;")
                                st.write("Total No.of ---- Total Registered Users by Year:")
                                st.write(top_user_year_Query6)
                                dftop=pd.DataFrame(top_user_year_Query6)
                                fig = go.Figure(data=go.Scatter(x=top_user_year_Query6['Year'], y=top_user_year_Query6['Total_Registered_user'], mode='lines+markers'))
                                fig.update_layout(title='Total Registered Users',
                                                xaxis_title='Year',
                                                yaxis_title='Total Registered Users')
                                st.plotly_chart(fig, use_container_width=True)

                            else:
                                pass
    elif Select == 'Visualization':
        st.header("Geo Visualization")
        tab1, tab2, tab3  = st.tabs(['Aggregrate Visuals', 'Map Visuals', 'Top Visuals'])
        with tab1:
            if tab1:
                method = option_menu('Select the visuals',['Aggregrate Transactions Visuals', 'Aggregrate Users Visuals'])
                if method == 'Aggregrate Transactions Visuals':
                    Quarter = st.sidebar.slider("Select Quarter", min_value=1, max_value=4, step=1)
                    TranCountAmount(Aggre_Tran, Quarter)
    
                elif method == 'Aggregrate Users Visuals':
                    all_states = Agg_user['State'].unique()
                    state = st.sidebar.selectbox("Select State", all_states)
                    user(Aggre_User, state)

                else:
                    pass
        with tab2:
            if tab2:
                method = option_menu('Select the visuals',['Map Transactions Visuals', 'Map Users Visuals'])
                if method == 'Map Transactions Visuals':
                    all_years = map_transaction['Year'].unique()
                    year = st.sidebar.selectbox('Select Years', all_years)
                    MapTransc(Map_Tran,year)

                elif method =='Map Users Visuals':
                    all_states = map_User['State'].unique()
                    state = st.sidebar.selectbox('Select state', all_states)
                    MapUsr(Map_User,state)
                else:
                    pass
        with tab3:
            if tab3:
                method = option_menu('Select the visuals',['Top Transactions Visuals', 'Top Users Visuals'])
                if method == 'Top Transactions Visuals':
                    all_quarter = top_transaction['Quarter'].unique()
                    quarter = st.sidebar.selectbox("Select Quarter", all_quarter)
                    TopTran(top_transaction,quarter)

                elif method == 'Top Users Visuals':
                    all_quarter = top_User['Quarter'].unique()
                    quarter = st.sidebar.selectbox("Select Quarter", all_quarter)                    
                    TopUsr(Top_User,quarter)
                else:
                    pass

    ques = None
    if Select == 'Queries':
        ques = st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Highest Transaction Count by Districts','Top 10 Districts With Lowest Transaction Count',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
        
    else:
        pass

    if ques == 'Top Brands Of Mobiles Used':
        Agg_User_Brabd_query1 = execute_query("SELECT Brand, COUNT(*) AS Total_Users FROM aggregrateusers GROUP BY Brand ORDER BY Total_Users DESC LIMIT 10;")
        st.write("Top 10 Brands of Mobiles Used:")
        AggUserDF = pd.DataFrame(Agg_User_Brabd_query1, columns=['Brand', 'Total_Users'])
        st.write(Agg_User_Brabd_query1)
        display_bar_chart(Agg_User_Brabd_query1, x='Brand', y='Total_Users', title='Top 10 Brands of Mobiles Used')

    elif ques == 'States With Lowest Transaction Amount':
        State_Transaction_Query = execute_query("SELECT State, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM aggregrateusers GROUP BY State ORDER BY Total_Transaction_Amount ASC LIMIT 10;")
        st.write("States with Lowest Transaction Amount:")
        st.write(State_Transaction_Query)
        display_bar_chart(State_Transaction_Query, x='State', y='Total_Transaction_Amount', title='States with Lowest Transaction Amount')

    elif ques == 'Highest Transaction Count by Districts':
        map_tran_dis_query = execute_query("SELECT Districts, MAX(Transaction_count) AS Total_Transaction_Count FROM maptransactions GROUP BY Districts;")
        MapTranDF = pd.DataFrame(map_tran_dis_query, columns=['Districts','Transaction_count'])
        st.write("Highest Transaction Count by Districts:")
        st.write(map_tran_dis_query)
        display_bar_chart(map_tran_dis_query, x='Districts', y='Total_Transaction_Count', title='Highest Transaction Count by Districts')

    elif ques == 'Top 10 Districts With Lowest Transaction Count':
        low_district_query = execute_query("SELECT Districts, MIN(Transaction_count) AS Total_Min_Transaction_Count FROM maptransactions GROUP BY Districts ORDER BY Total_Min_Transaction_Count ASC LIMIT 10;")
        st.write("Top 10 Districts With Lowest Transaction Count:")
        st.write(low_district_query)
        display_bar_chart(low_district_query, x='Districts', y='Total_Min_Transaction_Count', title='Top 10 Districts With Lowest Transaction Count')

    elif ques == 'Top 10 States With AppOpens':
        map_user_State_query1 = execute_query("SELECT State, COUNT(*) AS App_Opens FROM mapusers GROUP BY State ORDER BY App_Opens DESC LIMIT 10;")
        st.write("Top 10 States With Most App Opens:")
        st.write(map_user_State_query1)
        display_bar_chart(map_user_State_query1, x='State', y='App_Opens', title='Top 10 States With Most App Opens')

    elif ques == 'Least 10 States With AppOpens':
        least_app_opens_query = "SELECT State, COUNT(*) AS App_Opens FROM mapusers GROUP BY State ORDER BY App_Opens ASC LIMIT 10;"
        least_app_opens_data = execute_query(least_app_opens_query)
        st.write("Least 10 States With App Opens:")
        st.write(least_app_opens_data)
        display_bar_chart(least_app_opens_data, x='State', y='App_Opens', title='Least 10 States With App Opens')

    elif ques == 'States With Highest Trasaction Amount':
        state_trans_query = "SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount FROM toptransactions GROUP BY State ORDER BY Total_Transaction_Amount DESC;"
        state_trans_data = execute_query(state_trans_query)
        st.write("States With Highest Transaction Amount:")
        st.write(state_trans_data)
        display_bar_chart(state_trans_data, x='State', y='Total_Transaction_Amount', title='States With Highest Transaction Amount')

    elif ques == 'States With Highest Trasaction Count':
        state_trans_count_query = execute_query("SELECT State, COUNT(*) AS Total_Transactions FROM maptransactions GROUP BY State ORDER BY Total_Transactions DESC;")
        st.write("States With Highest Transaction Count:")
        st.write(state_trans_count_query)
        display_bar_chart(state_trans_count_query, x='State', y='Total_Transactions', title='States With Highest Transaction Count')

    elif ques == 'States With Lowest Trasaction Amount':
        low_state_trans_query = execute_query("SELECT State, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM aggregratetransactions GROUP BY State ORDER BY Total_Transaction_Amount ASC;")
        st.write("States With Lowest Transaction Amount:")
        st.write(low_state_trans_query)
        display_bar_chart(low_state_trans_query, x='State', y='Total_Transaction_Amount', title='States With Lowest Transaction Amount')

    elif ques == 'States With Lowest Trasaction Count':
         low_state_trans_count_query =execute_query( "SELECT State, COUNT(*) AS Total_Transactions FROM aggregrateusers GROUP BY State ORDER BY Total_Transactions ASC;")
         st.write("States With Lowest Transaction Count:")
         st.write(low_state_trans_count_query)
         display_bar_chart(low_state_trans_count_query)

    elif ques == 'Top 50 Districts With Lowest Transaction Amount':
        top_50_low_districts_query =execute_query( "SELECT Districts, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM maptransactions GROUP BY Districts ORDER BY Total_Transaction_Amount ASC LIMIT 50;")
        st.write("Top 50 Districts With Lowest Transaction Amount:")
        st.write(top_50_low_districts_query)
        display_bar_chart(top_50_low_districts_query, x='Districts', y='Total_Transaction_Amount', title='Top 50 Districts With Lowest Transaction Amount')

    else:
        pass

if __name__ == "__main__":
    main()
    
