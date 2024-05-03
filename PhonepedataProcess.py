# %%
import pandas as pd
import json
import os

# s!git clone https://github.com/PhonePe/pulse.git

# %% [markdown]
# ## Aggregate Transaction

# %%
path="C:/Users/Hp/Desktop/Phonepe/pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list


clm={'State':[], 'Year':[],'Quarter':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            A=json.load(Data)
            for z in A['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Transacion_type'].append(Name)
              clm['Transacion_count'].append(count)
              clm['Transacion_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quarter'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Transaction=pd.DataFrame(clm)

Agg_Transaction["State"] = Agg_Transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
Agg_Transaction["State"] = Agg_Transaction["State"].str.replace("-"," ")
Agg_Transaction["State"] = Agg_Transaction["State"].str.title()
Agg_Transaction['State'] = Agg_Transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

all_states = Agg_Transaction['State'].unique()



# %% [markdown]
# ## Aggregate user

# %%
path1="C:/Users/Hp/Desktop/Phonepe/pulse/data/aggregated/user/country/india/state/"
Agg_user_state_list=os.listdir(path1)
Agg_user_state_list

clm1={'State':[], 'Year':[],'Quarter':[],'Brands':[], 'Count':[], 'Percentage':[]}

for i in Agg_user_state_list:
    p_i=path1+i+"/"
    agg_user_yr=os.listdir(p_i)
    for j in agg_user_yr:
        p_j=p_i+j+"/"
        agg_us_yr_lst=os.listdir(p_j)
        for k in agg_us_yr_lst:
            p_k=p_j+k
            Data1=open(p_k,"r")
            B=json.load(Data1)
            try:
                for z in B['data']['usersByDevice']:
                  brand=z['brand']
                  count=z['count']
                  percentage=z['percentage']
                  clm1['Brands'].append(brand)
                  clm1['Count'].append(count)
                  clm1['Percentage'].append(percentage)
                  clm1['State'].append(i)
                  clm1['Year'].append(j)
                  clm1['Quarter'].append(int(k.strip('.json')))
            except:
                pass
#Succesfully created a dataframe
Agg_user=pd.DataFrame(clm1)

Agg_user["State"] = Agg_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
Agg_user["State"] = Agg_user["State"].str.replace("-"," ")
Agg_user["State"] = Agg_user["State"].str.title()
Agg_user['State'] = Agg_user['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

# %% [markdown]
# ## Map transaction

# %%
path2="C:/Users/Hp/Desktop/Phonepe/pulse/data/map/transaction/hover/country/india/state/"
map_tran_state=os.listdir(path2)
map_tran_state


clm2={'State':[], 'Year':[],'Quarter':[],'Districts':[], 'Transaction_count':[], 'Transaction_amount':[]}
for i in map_tran_state:
    p_i=path2+i+"/"
    map_tran_state_yr=os.listdir(p_i)
    for j in map_tran_state_yr:
        p_j=p_i+j+"/"
        map_tran_state_Lst=os.listdir(p_j)
        for k in map_tran_state_Lst:
            p_k=p_j+k
            Data2=open(p_k,'r')
            C=json.load(Data2)
            
            for z in C['data']['hoverDataList']:
                Name=z['name']
                count=z['metric'][0]['count']
                amount=z['metric'][0]['amount']
                clm2['Districts'].append(Name)
                clm2['Transaction_count'].append(count)
                clm2['Transaction_amount'].append(amount)
                clm2['State'].append(i)
                clm2['Year'].append(j)
                clm2['Quarter'].append(int(k.strip('.json')))
    
map_transaction=pd.DataFrame(clm2)


map_transaction["State"] = map_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
map_transaction["State"] = map_transaction["State"].str.replace("-"," ")
map_transaction["State"] = map_transaction["State"].str.title()
map_transaction['State'] = map_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

# %% [markdown]
# 
# 
# ## Map user

# %%
path3="C:/Users/Hp/Desktop/Phonepe/pulse/data/map/user/hover/country/india/state/"
map_usr_state=os.listdir(path3)
map_usr_state


clm3={'State':[], 'Year':[],'Quarter':[],'Districts':[],'RegisteredUsers':[], 'AppOpens':[]}
for i in map_usr_state:
    p_i=path3+i+"/"
    map_usr_state_yr=os.listdir(p_i)
    for j in map_usr_state_yr:
        p_j=p_i+j+"/"
        map_usr_state_Lst=os.listdir(p_j)
        for k in map_usr_state_Lst:
            p_k=p_j+k
            Data3=open(p_k,'r')
            D=json.load(Data3)
            for z in D['data']['hoverData'].items():
                district=z[0]
                registerUsers=z[1]['registeredUsers']
                appOpens=z[1]['appOpens']
                clm3['Districts'].append(district)
                clm3['RegisteredUsers'].append(registerUsers)
                clm3['AppOpens'].append(appOpens)
                clm3['State'].append(i)
                clm3['Year'].append(j)
                clm3['Quarter'].append(int(k.strip('.json')))

map_User=pd.DataFrame(clm3)


map_User["State"] = map_User["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
map_User["State"] = map_User["State"].str.replace("-"," ")
map_User["State"] = map_User["State"].str.title()
map_User['State'] = map_User['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

# %% [markdown]
# ## top transaction

# %%
path4="C:/Users/Hp/Desktop/Phonepe/pulse/data/top/transaction/country/india/state/"
top_tran=os.listdir(path4)
top_tran


clm4={'State':[], 'Year':[],'Quarter':[],'Pincodes':[], 'Transaction_count':[], 'Transaction_amount':[]}
for i in top_tran:
    p_i=path4+i+"/"
    top_tran_state_yr=os.listdir(p_i)
    for j in top_tran_state_yr:
        p_j=p_i+j+"/"
        top_tran_state_Lst=os.listdir(p_j)
        for k in top_tran_state_Lst:
            p_k=p_j+k
            Data4=open(p_k,'r')
            E=json.load(Data4)
        for z in E['data']['pincodes']:
            entityname=z['entityName']
            count=z['metric']['count']
            amount=z['metric']['amount']
            clm4['Pincodes'].append(entityname)
            clm4['Transaction_count'].append(count)
            clm4['Transaction_amount'].append(amount)
            clm4['State'].append(i)
            clm4['Year'].append(j)
            clm4['Quarter'].append(int(k.strip('.json')))
    
top_transaction=pd.DataFrame(clm4)


top_transaction["State"] = top_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_transaction["State"] = top_transaction["State"].str.replace("-"," ")
top_transaction["State"] = top_transaction["State"].str.title()
top_transaction['State'] = top_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


# %%
top_transaction


# %% [markdown]
# ## top user

# %%


# %%
path5="C:/Users/Hp/Desktop/Phonepe/pulse/data/top/user/country/india/state/"
top_usr=os.listdir(path5)
top_usr



clm5={'State':[], 'Year':[],'Quarter':[],'Pincodes':[],'RegisteredUsers':[]}
for i in top_tran:
    p_i=path5+i+"/"
    top_usr_state_yr=os.listdir(p_i)
    for j in top_usr_state_yr:
        p_j=p_i+j+"/"
        top_usr_state_Lst=os.listdir(p_j)
        for k in top_usr_state_Lst:
            p_k=p_j+k
            Data4=open(p_k,'r')
            E=json.load(Data4)
        for z in E['data']['pincodes']:
            entityname=z['name']
            registeredUsers=z['registeredUsers']
            clm5['Pincodes'].append(entityname)
            clm5['RegisteredUsers'].append(registeredUsers)
            clm5['State'].append(i)
            clm5['Year'].append(j)
            clm5['Quarter'].append(int(k.strip('.json')))
    
top_User=pd.DataFrame(clm5)


top_User["State"] = top_User["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
top_User["State"] = top_User["State"].str.replace("-"," ")
top_User["State"] = top_User["State"].str.title()
top_User['State'] = top_User['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

# %%
top_User

# %% [markdown]
# ## SQL Connection

# %%


# %% [markdown]
# ## SQL table AggregrateTransactions

# %%
import mysql.connector


conn=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="CSKtsk@738",
    database='PhonepeProject'
)
mycursor=conn.cursor()

mycursor.execute('''create table if not exists AggregrateTransactions (
    State varchar(255),
    year int,
    Quarter int,
    Transaction_type varchar(255),
    Transaction_count long,
    Transaction_amount double)''')


insert_query = '''INSERT INTO AggregrateTransactions (State, 
                                                     Year,
                                                     Quarter, 
                                                     Transaction_type,
                                                     Transaction_count, 
                                                     Transaction_amount) 
                                                     VALUES (%s, %s, %s, %s, %s, %s)'''
Values=Agg_Transaction.values.tolist()

for row in Values:
    mycursor.execute(insert_query, tuple(row))




conn.commit()

mycursor.close()
conn.close()

# %%


# %% [markdown]
# ## SQL table AggregrateUsers

# %%
conn=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="CSKtsk@738",
    database='PhonepeProject'
)
mycursor=conn.cursor()

mycursor.execute('''create table if not exists AggregrateUsers (
    State varchar(255),
    year int,
    Quarter int,
    Brand varchar(255),
    Count long,
    Percentage float)''')


insert_query = '''INSERT INTO AggregrateUsers (State, 
                                                     Year,
                                                     Quarter, 
                                                     Brand,
                                                     Count, 
                                                     Percentage) 
                                                     VALUES (%s, %s, %s, %s, %s, %s)'''
Values=Agg_user.values.tolist()

for row in Values:
    mycursor.execute(insert_query, tuple(row))




conn.commit()

mycursor.close()
conn.close()

# %% [markdown]
# ## SQL Table MapTranssactions

# %%
conn=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="CSKtsk@738",
    database='PhonepeProject'
)
mycursor=conn.cursor()

mycursor.execute('''create table if not exists MapTransactions (
    State varchar(255),
    year int,
    Quarter int,
    Districts varchar(255),
    Transaction_count long,
    Transaction_amount float)''')


insert_query = '''INSERT INTO MapTransactions (State, 
                                                     Year,
                                                     Quarter, 
                                                     Districts,
                                                     Transaction_count, 
                                                     Transaction_amount) 
                                                     VALUES (%s, %s, %s, %s, %s, %s)'''
Values=map_transaction.values.tolist()

for row in Values:
    mycursor.execute(insert_query, tuple(row))




conn.commit()

mycursor.close()
conn.close()

# %% [markdown]
# ## SQL Table MapUsers

# %%
conn=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="CSKtsk@738",
    database='PhonepeProject'
)
mycursor=conn.cursor()

mycursor.execute('''create table if not exists MapUsers (
    State varchar(255),
    year int,
    Quarter int,
    Districts varchar(255),
    RegisteredUsers long,
    AppOpens float)''')


insert_query = '''INSERT INTO MapUsers (State, 
                                                     Year,
                                                     Quarter, 
                                                     Districts,
                                                     RegisteredUsers, 
                                                     AppOpens) 
                                                     VALUES (%s, %s, %s, %s, %s, %s)'''
Values=map_User.values.tolist()

for row in Values:
    mycursor.execute(insert_query, tuple(row))

conn.commit()

mycursor.close()
conn.close()

# %% [markdown]
# ## SQL Table TopTransactions

# %%
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="CSKtsk@738",
    database='PhonepeProject'
)
mycursor = conn.cursor()

mycursor.execute('''create table if not exists TopTransactions (
    State varchar(255),
    Year int,
    Quarter int,
    Pincodes int,
    Transaction_count bigint,
    Transaction_amount float
    )''')

insert_query = '''INSERT INTO TopTransactions (State, Year, Quarter, Pincodes, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)'''

Values = top_transaction.values.tolist() 
for row in Values:
    mycursor.execute(insert_query, row) 
conn.commit()

mycursor.close()
conn.close()


# %% [markdown]
# ## SQL Table TopUsers

# %%
conn=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="CSKtsk@738",
    database='PhonepeProject'
)
mycursor=conn.cursor()

mycursor.execute('''create table if not exists TopUsers (
    State varchar(255),
    year int,
    Quarter int,
    Pincodes int,
    RegisteredUsers long
    )''')


insert_query = '''INSERT INTO TopUsers (State, 
                                                     Year,
                                                     Quarter, 
                                                     Pincodes,
                                                     RegisteredUsers
                                                     ) 
                                                     VALUES (%s, %s, %s, %s, %s)'''
Values=top_User.values.tolist()

for row in Values:
    mycursor.execute(insert_query, tuple(row))


conn.commit()

mycursor.close()
conn.close()

# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%



