import pandas as pd

from paths import RAW, PROCESSED, TABLES

orders = pd.read_csv(PROCESSED / "orders_clean.csv")
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
keys = ["order_id", "order_item_id"]
if items[keys + ["price", "freight_value"]].isna().any().any() or items.duplicated(keys).any():
    raise ValueError("Review missing item keys or amounts and duplicate item keys.")
if not items.order_id.isin(orders.order_id).all():
    raise ValueError("Some items refer to unknown orders.")

totals = items.groupby("order_id", as_index=False).agg(
    item_count=("order_item_id", "size"), product_count=("product_id", "nunique"),
    items_value=("price", "sum"), freight_value=("freight_value", "sum"),
)
totals["order_value_with_freight"] = totals.items_value + totals.freight_value
joined = orders.merge(totals, on="order_id", how="left", validate="one_to_one")
if abs(joined.items_value.sum() - items.price.sum()) > 0.01:
    raise ValueError("Item sales changed during aggregation.")
audit = pd.Series({
    "orders_before_join": len(orders), "orders_after_join": len(joined),
    "orders_with_items": len(totals), "orders_without_items": joined.item_count.isna().sum(),
    "negative_prices": items.price.lt(0).sum(), "negative_freight": items.freight_value.lt(0).sum(),
}, name="count")
audit.to_csv(TABLES / "06_item_join_checks.csv", index_label="check")
joined.to_csv(PROCESSED / "order_totals.csv", index=False)
print("06 | One row per order")
print(audit.to_string())
