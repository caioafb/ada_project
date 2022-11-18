import pandas as pd

def get_monthly_sales():
    """
    It reads in the all_sales.csv file, groups the data by month, sums the sales for each month, and
    then writes the results to a new file called monthly_sales.csv
    """
    df = pd.read_csv('files/all_sales.csv')

    df = df.groupby('month').sum()
    df = df.reset_index().drop(['week'], axis=1)
    df = round(df,2)

    df.to_csv('files/monthly_sales.csv', index = False)