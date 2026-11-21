import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from paths import FIGURES


def chart(title, subtitle, height=4.8):
    fig, ax = plt.subplots(figsize=(9, height))
    fig.subplots_adjust(left=0.14, right=0.94, top=0.78, bottom=0.16)
    fig.text(0.06, 0.92, title, fontsize=20, weight="bold", color="#152F42")
    fig.text(0.06, 0.855, subtitle, fontsize=10, color="#465F70")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#ABC1CC")
    ax.tick_params(length=0, pad=6, colors="#304958")
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, stage, name):
    folder = FIGURES / stage
    folder.mkdir(exist_ok=True)
    fig.savefig(folder / name, dpi=150, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def sales_ranking(labels, values, title, subtitle, stage):
    fig, ax = chart(title, subtitle, height=5.6)
    fig.subplots_adjust(left=0.32)
    bars = ax.barh(labels, values, height=0.62, color="#317E83")
    bars[0].set_color("#163E58")
    ax.invert_yaxis()
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in values], padding=5, fontsize=9)
    ax.set_xlim(0, values.max() * 1.22)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    save(fig, stage, "top_sales.png")
