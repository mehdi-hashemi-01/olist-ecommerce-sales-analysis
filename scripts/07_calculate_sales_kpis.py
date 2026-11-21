import pandas as pd

from paths import PROCESSED, TABLES

orders = pd.read_csv(PROCESSED / "order_totals.csv")
sales = orders.loc[orders.order_status.eq("delivered")].copy()
if sales.empty or sales.items_value.isna().any():
    raise ValueError("Delivered orders need item amounts for sales KPIs.")
sales.to_csv(PROCESSED / "delivered_sales.csv", index=False)
metrics = {
    "delivered_orders": len(sales), "items_sold": int(sales.item_count.sum()),
    "sales_brl": sales.items_value.sum(), "freight_brl": sales.freight_value.sum(),
    "average_order_value_brl": sales.items_value.mean(),
}
pd.DataFrame([metrics]).round(2).to_csv(TABLES / "07_sales_kpis.csv", index=False)
print("07 | Delivered order sales")
print(f"Orders: {len(sales):,}   |   Items: {metrics['items_sold']:,}")
print(f"Merchandise: R$ {metrics['sales_brl']:,.2f}   |   Freight: R$ {metrics['freight_brl']:,.2f}")
print(f"Average merchandise value per order: R$ {metrics['average_order_value_brl']:,.2f}")
