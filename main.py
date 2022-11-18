import all_sales
import monthly_sales
import weekly_price
import monthly_revenue
import pandas as pd

weeks = int(input("Insert number of weeks to retrieve: "))

all_sales.get_all_sales(weeks)
monthly_sales.get_monthly_sales()
weekly_price.get_weekly_price()
monthly_revenue.get_monthly_revenue()

all_sales_df = pd.read_csv('files/all_sales.csv')
monthly_sales_df = pd.read_csv('files/monthly_sales.csv')
weekly_price_df = pd.read_csv('files/weekly_price.csv')
monthly_revenue_df = pd.read_csv('files/monthly_revenue.csv')

op = 1

while (op >= 1 and op <= 4):
    print('\n [1] All Sales \n [2] Monthly Sales \n [3] Weekly Price \n [4] Monthly Revenue \n')
    op = int(input("Which dataframe do you wish to visualize: "))

    if op == 1:
        print(all_sales_df)
    elif op == 2:
        print(monthly_sales_df)
    elif op == 3:
        print(weekly_price_df)
    elif op == 4:
        print(monthly_revenue_df)

