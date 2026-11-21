import pandas as pd

from paths import PROCESSED, TABLES

dates = ["order_purchase_timestamp", "order_delivered_customer_date"]
orders = pd.read_csv(PROCESSED / "orders_clean.csv", parse_dates=dates)
actual = orders["order_delivered_customer_date"]
orders["missing_date"] = actual.isna()
status = orders.groupby("order_status", dropna=False).agg(
    orders=("order_id", "size"), missing_date=("missing_date", "sum")
)
status["has_date"] = status["orders"] - status["missing_date"]
status["missing_pct"] = (100 * status["missing_date"] / status["orders"]).round(2)
status = status.sort_values("orders", ascending=False)

orders["delivered_without_date"] = orders.order_status.eq("delivered") & actual.isna()
orders["canceled_with_date"] = orders.order_status.eq("canceled") & actual.notna()
orders["negative_duration"] = actual < orders["order_purchase_timestamp"]
flags = ["delivered_without_date", "canceled_with_date", "negative_duration"]
exceptions = orders.loc[orders[flags].any(axis=1), ["order_id", "order_status", *dates, *flags]]
exceptions.to_csv(TABLES / "03_delivery_exceptions.csv", index=False)
status.to_csv(TABLES / "03_dates_by_status.csv")
print("03 | Delivery date coverage by order status")
print(status.to_string())
print(f"Orders flagged for review: {len(exceptions):,}")
