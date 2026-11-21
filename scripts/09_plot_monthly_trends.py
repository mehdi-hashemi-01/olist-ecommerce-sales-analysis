import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter

from charts import chart, save
from paths import TABLES

monthly = pd.read_csv(TABLES / "08_monthly_sales.csv", parse_dates=["month"])
window = monthly.loc[monthly.month.between("2017-01-01", "2018-08-01")]
if window.empty:
    raise ValueError("No monthly data in the Jan 2017 to Aug 2018 chart window.")
series = [
    ("total_sales", "Monthly merchandise sales", "Sales (BRL)", "#217B78"),
    ("order_count", "Delivered orders by purchase month", "Orders", "#315D84"),
    ("average_order_value", "Average merchandise value per order", "BRL per order", "#AF6139"),
]
for column, title, unit, color in series:
    fig, ax = chart(title, "Jan 2017 to Aug 2018  |  Delivered orders grouped by purchase month")
    ax.plot(window.month, window[column], color=color, linewidth=2.3, marker="o", markersize=4)
    ax.set_ylim(bottom=0)
    ax.set_ylabel(unit)
    ax.grid(axis="y", color="#DDE6EA")
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    save(fig, "09_plot_monthly_trends", column + ".png")
print("09 | Saved three monthly charts to assets/figures/09_plot_monthly_trends/")
