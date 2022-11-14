import requests
import pandas as pd
import numpy as np
import os
from datetime import datetime

def request_data():
    response = requests.get('http://localhost:3000/api/ep1').json()
    df = pd.DataFrame(response)
    df = calculate_date(df)
    df = organize_db(df)
    return df

def calculate_date(df):
    df['date'] = df['date'].map(lambda x: datetime.fromtimestamp(x).strftime('%d-%m-%Y'))
    return df

def organize_db(df):
    df_slice = df.iloc[:,2:].fillna(0)
    df_slice = df_slice.sort_index(
        axis=1,
        key=lambda x: x.str.split("_").str[1]
        .astype(int)
    )
    df_slice[df_slice < 0] = 0
    df_slice.iloc[:,0:8] = df_slice.iloc[:,0:8].apply(np.int64)
    df_slice.iloc[:,8:] = df_slice.iloc[:,8:].round(2)
    df = df.iloc[:,0:2]
    df = pd.concat([df,df_slice], axis=1)
    df = df.sort_values(
        by=['date'],
        key=lambda x: x.str.split("-").str[1]
        .astype(int)
    )
    return df

def save_db(df):
    df.to_csv('all_sales.csv', index = False)

def weeklyfy(df, n_week):
    week = []
    [week.append(n_week) for _ in range(len(df))]
    return week

def monthlyfy(df):
    months = []
    dates_df = df['date'].str.split('-').str[1]
    month = 1
    cont = 0
    for i in dates_df:
        if cont == 0:
            months.append(month)
            previous_i = i
            cont = 1
        elif previous_i == i:
            months.append(month)
        else:
            month += 1
            months.append(month)
            previous_i = i
    return months

def show_db():
    return

df = pd.DataFrame()
n_week = 1

for _ in range(52):
    requested_df = request_data()
    requested_df.insert(loc=0, column='week', value=weeklyfy(requested_df, n_week))
    n_week += 1
    df = pd.concat([df,requested_df])

df.insert(loc=0, column='month', value=monthlyfy(df))
df = df.fillna(0)
save_db(df)