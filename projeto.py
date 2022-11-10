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
    df['date'] = df['date'].map(lambda x: datetime.fromtimestamp(x).strftime('%d/%m/%Y'))
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
    return df

def save_db(df):
    df.to_csv('bd.csv')

def show_db():
    return

#mask = ~np.isnan(df_slice)
#print(mask)
#print(df_slice[mask])

op = 's'
df = None

if (os.path.isfile('bd.csv')):
    df = pd.read_csv('bd.csv')
    df = df.set_index(df.iloc[:,0].name)

while (op == 's'):
    if df is not None:
        df = pd.concat([df,request_data()])
    else:
        df = request_data()

    print(df.to_string())

    op = input('Continuar? s/n ')

save_db(df)