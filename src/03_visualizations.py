"""
Script 03: Visualizations
==========================
- Loads SQL query results from outputs/sql_results/
- Builds 8 publication-quality charts using Matplotlib & Seaborn
- Saves all charts to outputs/charts/
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
SQL_DIR    = os.path.join(os.path.dirname(__file__), "..", "outputs", "sql_results")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ── Global Style ──────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi":        150,
    "figure.facecolor":  "white",
    "axes.facecolor":    "#f9f9f9",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "DejaVu Sans",
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    10,
})

BRAND_COLORS = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED",
                "#0891B2", "#DB2777", "#65A30D", "#EA580C", "#6366F1"]


def save_chart(fig, filename):
    path = os.path.join(CHARTS_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔ Saved: outputs/charts/{filename}")


# ──────────────────────────────────────────────────────────────
# CHART 1: Monthly Revenue Trend (Line Chart)
# ──────────────────────────────────────────────────────────────
def chart_monthly_revenue():
    df = pd.read_csv(os.path.join(SQL_DIR, "02_monthly_revenue.csv"))

    fig, ax1 = plt.subplots(figsize=(14, 5))

    ax1.fill_between(df["order_yearmonth"], df["monthly_revenue"],
                     alpha=0.15, color=BRAND_COLORS[0])
    ax1.plot(df["order_yearmonth"], df["monthly_revenue"],
             color=BRAND_COLORS[0], linewidth=2.5, marker="o", markersize=4, label="Monthly Revenue")

    ax2 = ax1.twinx()
    ax2.bar(df["order_yearmonth"], df["num_orders"],
            alpha=0.25, color=BRAND_COLORS[1], label="# Orders")
    ax2.set_ylabel("Number of Orders", color=BRAND_COLORS[1])
    ax2.tick_params(axis="y", labelcolor=BRAND_COLORS[1])

    # Rotate x labels
    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df["order_yearmonth"], rotation=45, ha="right", fontsize=8)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))
    ax1.set_title("Monthly Revenue & Order Volume (2017–2018)")
    ax1.set_ylabel("Revenue (BRL)")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    fig.tight_layout()
    save_chart(fig, "01_monthly_revenue_trend.png")


# ──────────────────────────────────────────────────────────────
# CHART 2: Top 10 Product Categories (Horizontal Bar)
# ──────────────────────────────────────────────────────────────
def chart_top_categories():
    df = pd.read_csv(os.path.join(SQL_DIR, "03_top_categories.csv"))
    df = df.sort_values("total_revenue")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(df["category"], df["total_revenue"],
                   color=BRAND_COLORS[:len(df)], edgecolor="white", height=0.65)

    for bar, val in zip(bars, df["total_revenue"]):
        ax.text(bar.get_width() + 5000, bar.get_y() + bar.get_height() / 2,
                f"R${val:,.0f}", va="center", fontsize=8)

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.1f}M"))
    ax.set_title("Top 10 Product Categories by Revenue")
    ax.set_xlabel("Total Revenue (BRL)")
    fig.tight_layout()
    save_chart(fig, "02_top_categories.png")


# ──────────────────────────────────────────────────────────────
# CHART 3: Revenue by State (Bar Chart)
# ──────────────────────────────────────────────────────────────
def chart_revenue_by_state():
    df = pd.read_csv(os.path.join(SQL_DIR, "04_revenue_by_state.csv"))

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [BRAND_COLORS[0] if i == 0 else "#93C5FD" for i in range(len(df))]
    bars = ax.bar(df["state"], df["total_revenue"], color=colors, edgecolor="white")

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20000,
                f"R${bar.get_height()/1e6:.1f}M", ha="center", fontsize=7.5)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.0f}M"))
    ax.set_title("Top 10 States by Revenue")
    ax.set_xlabel("State")
    ax.set_ylabel("Total Revenue (BRL)")
    fig.tight_layout()
    save_chart(fig, "03_revenue_by_state.png")


# ──────────────────────────────────────────────────────────────
# CHART 4: Customer Segments (Donut Chart)
# ──────────────────────────────────────────────────────────────
def chart_customer_segments():
    df = pd.read_csv(os.path.join(SQL_DIR, "05_customer_segments.csv"))
    labels = [s.split(" - ")[1] for s in df["customer_segment"]]
    sizes  = df["num_customers"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Donut: customer count
    wedges, texts, autotexts = ax1.pie(
        sizes, labels=labels,
        colors=BRAND_COLORS[:len(df)],
        autopct="%1.1f%%", startangle=90,
        wedgeprops={"width": 0.55, "edgecolor": "white", "linewidth": 2},
        pctdistance=0.75
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax1.set_title("Customer Segments\n(by Count)")

    # Bar: avg lifetime value
    ax2.bar(labels, df["avg_lifetime_value"],
            color=BRAND_COLORS[:len(df)], edgecolor="white")
    for i, v in enumerate(df["avg_lifetime_value"]):
        ax2.text(i, v + 5, f"R${v:.0f}", ha="center", fontsize=9)
    ax2.set_title("Avg Lifetime Value by Segment")
    ax2.set_ylabel("Avg Spend (BRL)")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:.0f}"))

    fig.suptitle("Customer Segmentation Analysis", fontweight="bold", fontsize=13)
    fig.tight_layout()
    save_chart(fig, "04_customer_segments.png")


# ──────────────────────────────────────────────────────────────
# CHART 5: Payment Methods (Pie + Bar combo)
# ──────────────────────────────────────────────────────────────
def chart_payment_methods():
    df = pd.read_csv(os.path.join(SQL_DIR, "06_payment_methods.csv"))
    df = df.dropna(subset=["payment_type"])
    df["payment_type"] = df["payment_type"].astype(str)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Pie: share of orders
    ax1.pie(df["total_orders"], labels=df["payment_type"],
            colors=BRAND_COLORS[:len(df)],
            autopct="%1.1f%%", startangle=140,
            wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax1.set_title("Payment Method Share\n(by Orders)")

    # Bar: avg installments
    bars = ax2.bar(df["payment_type"], df["avg_installments"],
                   color=BRAND_COLORS[:len(df)], edgecolor="white")
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 f"{bar.get_height():.1f}x", ha="center", fontsize=9)
    ax2.set_title("Avg Installments by Payment Type")
    ax2.set_ylabel("Avg Installments")

    fig.suptitle("Payment Method Analysis", fontweight="bold", fontsize=13)
    fig.tight_layout()
    save_chart(fig, "05_payment_methods.png")


# ──────────────────────────────────────────────────────────────
# CHART 6: Quarterly Revenue Growth (Bar + Line)
# ──────────────────────────────────────────────────────────────
def chart_quarterly_growth():
    df = pd.read_csv(os.path.join(SQL_DIR, "07_quarterly_growth.csv"))
    df["pct_change"] = df["quarterly_revenue"].pct_change() * 100

    fig, ax1 = plt.subplots(figsize=(10, 5))

    colors = [BRAND_COLORS[0] if r >= 0 else BRAND_COLORS[2]
              for r in df["pct_change"].fillna(0)]
    bars = ax1.bar(df["period"], df["quarterly_revenue"],
                   color=BRAND_COLORS[0], alpha=0.8, edgecolor="white")

    ax2 = ax1.twinx()
    ax2.plot(df["period"], df["pct_change"], color=BRAND_COLORS[2],
             linewidth=2, marker="D", markersize=6, label="QoQ Growth %")
    ax2.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax2.set_ylabel("Quarter-over-Quarter Growth (%)", color=BRAND_COLORS[2])
    ax2.tick_params(axis="y", labelcolor=BRAND_COLORS[2])

    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.1f}M"))
    ax1.set_title("Quarterly Revenue & Growth Rate")
    ax1.set_ylabel("Revenue (BRL)")
    ax1.set_xlabel("Quarter")
    plt.xticks(rotation=30)
    ax2.legend()

    fig.tight_layout()
    save_chart(fig, "06_quarterly_growth.png")


# ──────────────────────────────────────────────────────────────
# CHART 7: Review Score Distribution (Bar)
# ──────────────────────────────────────────────────────────────
def chart_review_scores():
    df = pd.read_csv(os.path.join(SQL_DIR, "08_review_distribution.csv"))
    score_colors = ["#DC2626", "#F97316", "#EAB308", "#84CC16", "#16A34A"]
    score_colors_map = {5: "#16A34A", 4: "#84CC16", 3: "#EAB308", 2: "#F97316", 1: "#DC2626"}
    colors = [score_colors_map.get(s, "#93C5FD") for s in df["score"]]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df["score"].astype(str), df["num_reviews"],
                  color=colors, edgecolor="white", width=0.6)

    for bar, pct in zip(bars, df["percentage"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 300,
                f"{pct}%", ha="center", fontsize=10, fontweight="bold")

    ax.set_title("Customer Review Score Distribution")
    ax.set_xlabel("Review Score (1=Worst, 5=Best)")
    ax.set_ylabel("Number of Reviews")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    fig.tight_layout()
    save_chart(fig, "07_review_distribution.png")


# ──────────────────────────────────────────────────────────────
# CHART 8: Seasonal Patterns (Polar / Circular Bar)
# ──────────────────────────────────────────────────────────────
def chart_seasonal_patterns():
    df = pd.read_csv(os.path.join(SQL_DIR, "10_seasonal_patterns.csv"))
    df = df.sort_values("order_month")

    fig, ax = plt.subplots(figsize=(10, 5))

    colors = [BRAND_COLORS[i % len(BRAND_COLORS)] for i in range(len(df))]
    bars = ax.bar(df["order_month_name"], df["total_revenue"],
                  color=colors, edgecolor="white", width=0.6)

    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 10000,
                f"R${bar.get_height()/1e6:.1f}M",
                ha="center", fontsize=8)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1e6:.1f}M"))
    ax.set_title("Seasonal Revenue Patterns by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue (BRL)")
    plt.xticks(rotation=30)

    fig.tight_layout()
    save_chart(fig, "08_seasonal_patterns.png")


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  STEP 3: Building Visualizations")
    print("=" * 55)
    print()

    chart_monthly_revenue()
    chart_top_categories()
    chart_revenue_by_state()
    chart_customer_segments()
    chart_payment_methods()
    chart_quarterly_growth()
    chart_review_scores()
    chart_seasonal_patterns()

    print()
    print("=" * 55)
    print("  All 8 charts saved to outputs/charts/")
    print("  Run 04_insights_report.py next.")
    print("=" * 55)


if __name__ == "__main__":
    main()
