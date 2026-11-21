import pandas as pd

from paths import PROCESSED, TABLES

dates = ["order_purchase_timestamp", "order_delivered_customer_date"]
orders = pd.read_csv(PROCESSED / "orders_clean.csv", parse_dates=dates)
elapsed = orders.order_delivered_customer_date - orders.order_purchase_timestamp
orders["delivery_days"] = elapsed.dt.total_seconds() / 86400
valid = orders.order_status.eq("delivered") & orders.delivery_days.ge(0)
delivery = orders.loc[valid, ["order_id", *dates, "order_estimated_delivery_date", "delivery_days"]]
delivery.to_csv(PROCESSED / "valid_deliveries.csv", index=False)

stats = delivery.delivery_days.describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95])
stats.rename("value").to_csv(TABLES / "04_duration_stats.csv", index_label="statistic")
print(f"04 | Purchase to delivery  ({len(delivery):,} valid orders)")
print(f"Median: {stats['50%']:.1f} days   |   90th percentile: {stats['90%']:.1f} days")
