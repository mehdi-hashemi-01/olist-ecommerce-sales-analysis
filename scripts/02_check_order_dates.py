import pandas as pd

from paths import RAW, PROCESSED, TABLES

orders = pd.read_csv(RAW / "olist_orders_dataset.csv")
if orders.order_id.isna().any() or orders.order_id.duplicated().any():
    raise ValueError("Each order needs a unique, non-empty order_id.")

date_columns = [
    "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
    "order_delivered_customer_date", "order_estimated_delivery_date",
]
checks = []
for name in date_columns:
    original = orders[name]
    converted = pd.to_datetime(original, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    checks.append({
        "column": name,
        "missing_in_source": original.isna().sum(),
        "invalid_nonempty": (original.notna() & converted.isna()).sum(),
        "parsed": converted.notna().sum(),
    })
    orders[name] = converted

audit = pd.DataFrame(checks)
audit.to_csv(TABLES / "02_date_checks.csv", index=False)
orders.to_csv(PROCESSED / "orders_clean.csv", index=False)
print(f"02 | Order dates  ({len(orders):,} orders)")
print(audit.to_string(index=False))
