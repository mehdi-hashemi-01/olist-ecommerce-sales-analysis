from pathlib import Path

import pandas as pd


root = Path(__file__).resolve().parents[1]
raw_dir = root / "data" / "raw"
output_dir = root / "reports" / "tables"

files = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "categories": "product_category_name_translation.csv",
}

missing_files = [name for name in files.values() if not (raw_dir / name).is_file()]
if missing_files:
    raise SystemExit("Missing files in data/raw/:\n" + "\n".join(missing_files))

# Postal prefixes can start with zero.
postal_types = {
    "customer_zip_code_prefix": "string",
    "seller_zip_code_prefix": "string",
    "geolocation_zip_code_prefix": "string",
}

inventory = []
columns = []
for table, filename in files.items():
    frame = pd.read_csv(raw_dir / filename, dtype=postal_types)
    inventory.append({
        "table": table,
        "rows": len(frame),
        "columns": len(frame.columns),
        "full_row_duplicates": frame.duplicated().sum(),
    })
    for name in frame.columns:
        series = frame[name]
        columns.append({
            "table": table,
            "column": name,
            "loaded_dtype": str(series.dtype),
            "missing_count": series.isna().sum(),
            "missing_percent": round(100 * series.isna().mean(), 2),
        })

output_dir.mkdir(parents=True, exist_ok=True)
summary = pd.DataFrame(inventory)
summary.to_csv(output_dir / "table_inventory.csv", index=False)
pd.DataFrame(columns).to_csv(output_dir / "column_profile.csv", index=False)
print(summary.to_string(index=False))
print(f"Saved both reports to {output_dir}")
