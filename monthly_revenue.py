import pandas as pd

def get_monthly_revenue():
    """
    It takes the weekly sales data and multiplies it by the weekly prices to get the weekly revenue.
    Then it sums up the weekly revenue to get the monthly revenue
    """

    weekly_prices_df = pd.read_csv('files/weekly_price.csv')
    weekly_prices_df = weekly_prices_df.iloc[:,1:].T 

    all_sales_df = pd.read_csv('files/all_sales.csv')

    df_slice = all_sales_df.iloc[:,4:]

    all_sales_revenue = pd.DataFrame()

    for i in range(len(weekly_prices_df.T)):
        weekly_revenue = (df_slice[all_sales_df['week'] == i+1] * weekly_prices_df[i].values)
        all_sales_revenue = pd.concat([all_sales_revenue, weekly_revenue])

    monthly_revenue = pd.DataFrame()
    for i in all_sales_df['month'].unique():
        monthly_revenue[f'month {str(i)}'] = (all_sales_revenue[all_sales_df['month'] == i]).sum()

    monthly_revenue = round(monthly_revenue, 2)

    balance = [round(monthly_revenue[i].sum(),2) for i in monthly_revenue]
    monthly_revenue = monthly_revenue.T
    monthly_revenue['balance'] = balance

    monthly_revenue.to_csv('files/monthly_revenue.csv')






