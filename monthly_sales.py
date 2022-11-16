import pandas as pd

df = pd.read_csv('files/all_sales.csv')

df_slice = df.iloc[:,4:]
month_indexes = []
year = pd.DataFrame()

for i in range(12):
    month = df_slice[df['month'] == i+1].sum().round(2)
    year = pd.concat([year,month], axis=1)
    month_indexes.append('Month ' + str(i+1))

year = year.set_axis(month_indexes, axis=1)
year = year.T
year.to_csv('files/monthly_sales.csv')