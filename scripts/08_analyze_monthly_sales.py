import pandas as pd

from paths import PROCESSED, TABLES

orders = pd.read_csv(PROCESSED / "delivered_sales.csv", parse_dates=["order_purchase_timestamp"])
if orders.order_purchase_timestamp.isna().any():
    raise ValueError("Monthly sales require a purchase date for each delivered order.")
orders["month"] = orders.order_purchase_timestamp.dt.to_period("M")
monthly = orders.groupby("month").agg(
    order_count=("order_id", "size"), items_sold=("item_count", "sum"),
    total_sales=("items_value", "sum"), total_freight=("freight_value", "sum"),
    average_order_value=("items_value", "mean"),
)
monthly = monthly.reindex(pd.period_range(monthly.index.min(), monthly.index.max(), freq="M"))
for name in ["order_count", "items_sold", "total_sales", "total_freight"]:
    monthly[name] = monthly[name].fillna(0)
monthly[["order_count", "items_sold"]] = monthly[["order_count", "items_sold"]].astype(int)
previous = monthly.total_sales.shift(1)
monthly["growth_pct"] = (monthly.total_sales - previous) / previous.where(previous > 0) * 100
if abs(monthly.total_sales.sum() - orders.items_value.sum()) > 0.01:
    raise ValueError("Monthly sales do not match overall sales.")
monthly.round(2).to_csv(TABLES / "08_monthly_sales.csv", index_label="month")
peak = monthly.total_sales.idxmax()
print(f"08 | Monthly sales  ({monthly.index.min()} to {monthly.index.max()})")
print(f"Highest observed month: {peak}   |   Merchandise: R$ {monthly.loc[peak, 'total_sales']:,.2f}")
