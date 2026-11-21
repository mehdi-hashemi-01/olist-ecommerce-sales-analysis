import pandas as pd

from charts import chart, save
from paths import RAW, TABLES

orders = pd.read_csv(RAW / "olist_orders_dataset.csv",
                     usecols=["order_id", "order_status", "order_purchase_timestamp"])
items = pd.read_csv(RAW / "olist_order_items_dataset.csv",
                    usecols=["order_id", "order_item_id", "product_id", "price"])
orders["month"] = orders.order_purchase_timestamp.str[:7]
selected = orders.order_status.eq("delivered") & orders.month.isin(["2017-10", "2017-11"])
sales = orders.loc[selected, ["order_id", "month"]].merge(items, on="order_id", validate="one_to_many", how="left")
if sales[["product_id", "order_item_id", "price"]].isna().any().any() or sales.duplicated(["order_id", "order_item_id"]).any():
    raise ValueError("Review missing or duplicated delivered items before comparing prices.")

monthly = sales.groupby(["month", "product_id"]).agg(units=("price", "size"), price=("price", "mean"))
products = monthly.loc["2017-10"].join(monthly.loc["2017-11"], how="outer", lsuffix="_oct", rsuffix="_nov")
for name in ["units_oct", "units_nov"]:
    products[name] = products[name].fillna(0).astype(int)
products["group"] = "Both months"
products.loc[products.units_nov.eq(0), "group"] = "October only"
products.loc[products.units_oct.eq(0), "group"] = "November only"
products["price_change_brl"] = products.price_nov - products.price_oct
common = products.loc[products.group.eq("Both months")].copy()
if common.empty:
    raise ValueError("At least one product must have sales in both months.")

# Weights are unit shares within the matched group in each month.
weight_oct = common.units_oct / common.units_oct.sum()
weight_nov = common.units_nov / common.units_nov.sum()
common_oct = (weight_oct * common.price_oct).sum()
common_nov = (weight_nov * common.price_nov).sum()
overall = sales.groupby("month").price.mean()

# Midpoint weights split the interaction equally between price and mix.
price_effect = (weight_oct + weight_nov) / 2 * common.price_change_brl
mix_effect = (common.price_oct + common.price_nov) / 2 * (weight_nov - weight_oct)
products["matched_price_effect_brl"] = price_effect
products["matched_mix_effect_brl"] = mix_effect
effects = pd.Series({
    "Remove October-only products": common_oct - overall["2017-10"],
    "Prices of matched products": price_effect.sum(),
    "Unit mix of matched products": mix_effect.sum(),
    "Include November-only products": overall["2017-11"] - common_nov,
}, name="change_brl_per_item")
if abs(effects.sum() - (overall["2017-11"] - overall["2017-10"])) > 0.000001:
    raise ValueError("Contributions do not reconcile to the overall price change.")
products.to_csv(TABLES / "13_product_price_comparison.csv", float_format="%.8f")
effects.to_csv(TABLES / "13_price_effects.csv", index_label="component", float_format="%.8f")

fig, ax = chart("Why did the average item price fall?", "October to November 2017  |  Delivered items  |  Contributions in BRL per item")
fig.subplots_adjust(left=0.37)
colors = ["#317E83" if value >= 0 else "#B36643" for value in effects]
bars = ax.barh(effects.index, effects, height=0.58, color=colors)
ax.invert_yaxis()
ax.axvline(0, color="#657B84", linewidth=0.9)
ax.bar_label(bars, labels=[f"{value:+.2f}" for value in effects], padding=4)
ax.margins(x=0.18)
ax.set_xlabel("Change in mean price per item (BRL)")
save(fig, "13_compare_product_prices", "price_change.png")
print(f"13 | Average item price: R$ {overall['2017-10']:.2f} to R$ {overall['2017-11']:.2f}")
print(effects.round(2).to_string())
