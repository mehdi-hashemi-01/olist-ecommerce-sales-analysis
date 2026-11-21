import pandas as pd

from paths import RAW, PROCESSED, TABLES

orders = pd.read_csv(PROCESSED / "delivered_sales.csv", parse_dates=["order_purchase_timestamp"])
customers = pd.read_csv(RAW / "olist_customers_dataset.csv", dtype={"customer_zip_code_prefix": "string"})
if customers[["customer_id", "customer_unique_id"]].isna().any().any():
    raise ValueError("Customer identifiers must be present.")
sales = orders.merge(customers, on="customer_id", how="left", validate="many_to_one")
if sales.customer_unique_id.isna().any() or len(sales) != len(orders):
    raise ValueError("Every delivered order must match one customer record.")
if abs(sales.items_value.sum() - orders.items_value.sum()) > 0.01:
    raise ValueError("Sales changed after joining customers.")
sales.to_csv(PROCESSED / "customer_orders.csv", index=False)

buyers = sales.groupby("customer_unique_id").agg(
    order_count=("order_id", "nunique"), total_spent=("items_value", "sum"),
    average_order_value=("items_value", "mean"), first_purchase=("order_purchase_timestamp", "min"),
    last_purchase=("order_purchase_timestamp", "max"),
)
buyers.nlargest(10, "total_spent").round(2).to_csv(TABLES / "10_top_customers.csv")
repeat = int(buyers.order_count.ge(2).sum())
rate = 100 * repeat / len(buyers)
pd.DataFrame([{
    "unique_buyers": len(buyers), "repeat_buyers": repeat, "repeat_pct": round(rate, 2),
}]).to_csv(TABLES / "10_customer_kpis.csv", index=False)
print("10 | Repeat purchases within the observed period")
print(f"Buyers: {len(buyers):,}   |   At least two delivered orders: {repeat:,} ({rate:.2f}%)")
