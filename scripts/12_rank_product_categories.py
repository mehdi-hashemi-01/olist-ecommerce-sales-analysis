import pandas as pd

from charts import sales_ranking
from paths import RAW, PROCESSED, TABLES

orders = pd.read_csv(PROCESSED / "delivered_sales.csv")
items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
products = pd.read_csv(RAW / "olist_products_dataset.csv", usecols=["product_id", "product_category_name"])
translations = pd.read_csv(RAW / "product_category_name_translation.csv")
if products.product_id.isna().any() or translations.product_category_name.isna().any():
    raise ValueError("Product IDs and translation keys must be present.")
delivered = items.loc[items.order_id.isin(orders.order_id)]
sales = delivered.merge(products, on="product_id", how="left", validate="many_to_one", indicator=True)
if sales["_merge"].ne("both").any():
    raise ValueError("Some delivered items have no matching product.")
sales = sales.merge(translations, on="product_category_name", how="left", validate="many_to_one")
original = sales.product_category_name
english = sales.product_category_name_english
sales["category"] = english.fillna(original).fillna("unknown")
print(f"12 | Product categories  ({original.isna().sum():,} items missing a category, "
      f"{(original.notna() & english.isna()).sum():,} items without translation)")

categories = sales.groupby("category").agg(
    items_sold=("order_item_id", "size"), order_count=("order_id", "nunique"),
    unique_products=("product_id", "nunique"), total_sales=("price", "sum"),
    average_item_price=("price", "mean"),
).sort_values("total_sales", ascending=False)
total = orders.items_value.sum()
if len(sales) != len(delivered) or abs(categories.total_sales.sum() - total) > 0.01:
    raise ValueError("Category totals do not match delivered sales.")
categories["sales_share_percent"] = 100 * categories.total_sales / total
categories.round(2).to_csv(TABLES / "12_category_sales.csv")
top = categories.head(10)
labels = top.index.str.replace("_", " ").str.title()
sales_ranking(labels, top.total_sales, "Categories with the highest merchandise sales",
              "Top 10 product categories  |  Delivered items  |  BRL, excluding freight", "12_rank_product_categories")
print(top[["items_sold", "total_sales"]].to_string())
