import pandas as pd

df = pd.read_csv('all_sales.csv')

df_slice = df.iloc[:,4:]
month1 = df_slice[df['month'] == 1].sum()
month2 = df_slice[df['month'] == 2].sum()
month_indexes = []
year = pd.DataFrame()

for i in range(12):
    month = df_slice[df['month'] == i+1].sum().round(2)
    year = pd.concat([year,month], axis=1)
    month_indexes.append('Month ' + str(i+1))

year = year.set_axis(month_indexes, axis=1)

year.to_csv('monthly_sales.csv')

