import pandas as pd

from charts import sales_ranking
from paths import PROCESSED, TABLES

orders = pd.read_csv(PROCESSED / "customer_orders.csv")
cities = orders.groupby(["customer_state", "customer_city"], as_index=False, dropna=False).agg(
    order_count=("order_id", "size"), unique_customers=("customer_unique_id", "nunique"),
    total_sales=("items_value", "sum"), average_order_value=("items_value", "mean"),
).sort_values("total_sales", ascending=False)
cities["sales_share_percent"] = 100 * cities.total_sales / orders.items_value.sum()
cities.round(2).to_csv(TABLES / "11_city_sales.csv", index=False)
top = cities.head(10)
labels = top.customer_city.fillna("Unknown").str.title() + " / " + top.customer_state.fillna("?")
sales_ranking(labels, top.total_sales, "Cities with the highest merchandise sales",
              "Top 10 city and state pairs  |  Delivered orders  |  BRL, excluding freight", "11_rank_cities")
print("11 | City sales leaders (BRL, excluding freight)")
print(top[["customer_state", "customer_city", "total_sales"]].to_string(index=False))
