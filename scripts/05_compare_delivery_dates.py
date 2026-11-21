import pandas as pd

from charts import chart, save
from paths import PROCESSED, TABLES

dates = ["order_delivered_customer_date", "order_estimated_delivery_date"]
delivery = pd.read_csv(PROCESSED / "valid_deliveries.csv", parse_dates=dates).dropna(subset=dates)
actual = delivery.order_delivered_customer_date.dt.normalize()
promise = delivery.order_estimated_delivery_date.dt.normalize()
delay = (actual - promise).dt.days
outcome = pd.Series("On promised day", index=delay.index)
outcome.loc[delay < 0] = "Early"
outcome.loc[delay > 0] = "Late"
counts = outcome.value_counts().reindex(["Early", "On promised day", "Late"], fill_value=0)
summary = counts.rename("orders").to_frame()
summary["share_pct"] = counts / len(delivery) * 100
summary.round(2).to_csv(TABLES / "05_delivery_outcomes.csv", index_label="outcome")
delay[delay > 0].describe().rename("days").to_csv(TABLES / "05_late_delay_stats.csv", index_label="statistic")

fig, ax = chart("Did orders arrive by the promised date?", f"{len(delivery):,} eligible deliveries  |  Share of orders by calendar-day outcome")
bars = ax.barh(counts.index, summary.share_pct, color=["#317E83", "#728EA2", "#C56B40"])
ax.invert_yaxis()
ax.bar_label(bars, labels=[f"{v:.1f}%" for v in summary.share_pct], padding=5)
ax.set_xlim(0, 105)
ax.set_xlabel("Share of evaluated orders (%)")
save(fig, "05_compare_delivery_dates", "delivery_outcomes.png")
print(f"05 | Promised vs. actual date  ({len(delivery):,} orders evaluated)")
print(summary.round(2).to_string())
