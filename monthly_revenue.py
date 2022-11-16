import pandas as pd


weekly_prices_df = pd.read_csv('files/weekly_price.csv')
# Removido a coluna das semanas para facilitar a multiplicação dos dataframes
weekly_prices_df = weekly_prices_df.iloc[:,1:].T 

all_sales_df = pd.read_csv('files/all_sales.csv')

# Fatiando o dataframe para manter somente as informações dos produtos
df_slice = all_sales_df.iloc[:,4:]

all_sales_revenue = pd.DataFrame()

for i in range(len(weekly_prices_df.T)):
    weekly_revenue = round((df_slice[all_sales_df['week'] == i+1] * weekly_prices_df[i].values),2)
    all_sales_revenue = pd.concat([all_sales_revenue, weekly_revenue])

monthly_revenue = pd.DataFrame()
for i in all_sales_df['month'].unique():
    monthly_revenue['Month ' + str(i)] = (all_sales_revenue[all_sales_df['month'] == i]).sum()

monthly_revenue.to_csv('files/monthly_revenue.csv')








