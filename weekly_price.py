import pandas as pd
import random
import math

sales_df = pd.read_csv('files/all_sales.csv')

df_slice = sales_df.iloc[:,4:]

indexes = list(df_slice.columns.values)
df = pd.DataFrame(index=indexes)

for i in sales_df['week'].unique():
    if i == 1:
        prices = []
        for j in indexes:
            if int(j.split("_")[1]) < 8:
                prices.append(round(random.uniform(10,75),2))
            else:
                prices.append(round(random.uniform(50,115),2))
        df['week ' + str(i)] = prices

    elif i == 2:
        df['week ' + str(i)] = df['week ' + str(i-1)].copy()
        
    else:
        mean_sales_week_0 = df_slice[sales_df['week'] == i-2].mean()
        mean_sales_week_1 = df_slice[sales_df['week'] == i-1].mean()

        variation = (mean_sales_week_1 - mean_sales_week_0)/mean_sales_week_0

        variation_function = (0.5 + 1/(1 + (math.e ** (-variation)))).fillna(1)

        prices = df['week ' + str(i-1)].values.copy()
        prices *= variation_function
        df['week ' + str(i)] = prices

df = df.T
df.to_csv('files/weekly_price.csv')

