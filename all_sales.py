import requests
import pandas as pd
import numpy as np
from datetime import datetime


def request_data():
    """
    It takes the data from the API, converts it to a dataframe, modifies the date format, and organizes the
    dataframe
    :return: A dataframe
    """
    response = requests.get('http://localhost:3000/api/ep1').json()
    df = pd.DataFrame(response)
    df = calculate_date(df)
    df = organize_db(df)
    return df

def calculate_date(df):
    """
    It takes a dataframe and converts the date column from a timestamp to a date
    
    :param df: the dataframe
    :return: A dataframe with the date column converted to a string.
    """
    df['date'] = df['date'].map(lambda x: datetime.fromtimestamp(x).strftime('%m-%d-%Y'))
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)
    df['date'] = df['date'].dt.strftime('%d-%m-%Y')
    return df

def organize_db(df):
    """
    It takes a dataframe, sorts the columns, rounds the last 8 columns
    to 2 decimal places, and sorts the rows by the month in the date column
    
    :param df: the dataframe to be organized
    :return: A dataframe with the columns sorted by the number in the column name.
    """
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
    '''
    df = df.sort_values(
        by=['date'],
        key=lambda x: x.str.split("-").str[1]
        .astype(int)
    )
    df = df.sort_values(
        by=['date'],
        key=lambda x: x.str.split("-").str[2]
        .astype(int)
    )
    '''
    return df

def weeklyfy(df, n_week):
    """
    It takes a dataframe and the number of the week and returns a list of that number repeated as many times as there
    are rows in the dataframe to be inserted as new column in the dataframe
    
    :param df: the dataframe
    :param n_week: the week number
    :return: A list of the same number of elements as the dataframe.
    """
    week = []
    [week.append(n_week) for _ in range(len(df))]
    return week

def monthlyfy(df):
    """
    It takes a dataframe with a column called 'date' and returns a list of integers that represent the
    month of each date in the dataframe.
    
    :param df: the dataframe
    :return: A list of integers.
    """
    months = []
    dates_df = df['date'].str.split('-').str[1]
    month = 1
    cont = 0
    for i in dates_df:
        if cont == 0:
            previous_i = i
            cont = 1
        elif previous_i != i:
            month += 1
            previous_i = i
        months.append(month)
    return months

def get_all_sales(weeks: int):
    """
    It takes the number of weeks you want to request data for, requests the data, adds a week column,
    adds a month column, fills in any missing values with 0, and saves the data to a csv
    
    :param weeks: int = number of weeks to pull data for
    :type weeks: int
    """

    df = pd.DataFrame()
    for n_week in range(weeks):
        requested_df = request_data()
        requested_df.insert(loc=0, column='week', value=weeklyfy(requested_df, n_week+1))
        df = pd.concat([df,requested_df])

    df.insert(loc=0, column='month', value=monthlyfy(df))
    df = df.fillna(0)
    df.to_csv('files/all_sales.csv', index = False)