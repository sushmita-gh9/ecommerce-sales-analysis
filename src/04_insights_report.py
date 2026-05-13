"""
Script 04: Automated Insights Report Generator
================================================
- Reads all SQL results
- Generates a structured business insights report
- Saves as outputs/reports/insights_report.txt and insights_report.md
"""

import pandas as pd
import os
from datetime import datetime

SQL_DIR     = os.path.join(os.path.dirname(__file__), "..", "outputs", "sql_results")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def load(filename):
    return pd.read_csv(os.path.join(SQL_DIR, filename))


def generate_report():
    print("=" * 55)
    print("  STEP 4: Generating Insights Report")
    print("=" * 55)

    kpis      = load("01_overall_kpis.csv").iloc[0]
    monthly   = load("02_monthly_revenue.csv")
    cats      = load("03_top_categories.csv")
    states    = load("04_revenue_by_state.csv")
    segments  = load("05_customer_segments.csv")
    payments  = load("06_payment_methods.csv")
    payments  = payments.dropna(subset=["payment_type"])
    payments["payment_type"] = payments["payment_type"].astype(str)
    quarterly = load("07_quarterly_growth.csv")
    reviews   = load("08_review_distribution.csv")
    seasonal  = load("10_seasonal_patterns.csv")

    # ── Derived Metrics ──────────────────────────────────────
    best_month  = monthly.loc[monthly["monthly_revenue"].idxmax()]
    worst_month = monthly.loc[monthly["monthly_revenue"].idxmin()]
    top_cat     = cats.iloc[0]
    top_state   = states.iloc[0]
    top_payment = payments.iloc[0]
    peak_season = seasonal.loc[seasonal["total_revenue"].idxmax()]
    low_season  = seasonal.loc[seasonal["total_revenue"].idxmin()]

    five_star_pct = reviews[reviews["score"] == 5]["percentage"].values[0] if len(reviews[reviews["score"] == 5]) > 0 else 0
    one_star_pct  = reviews[reviews["score"] == 1]["percentage"].values[0] if len(reviews[reviews["score"] == 1]) > 0 else 0

    loyal_seg  = segments[segments["customer_segment"].str.contains("Loyal")]
    onetime_seg = segments[segments["customer_segment"].str.contains("One-Time")]
    loyal_ltv  = loyal_seg["avg_lifetime_value"].values[0] if len(loyal_seg) > 0 else 0
    onetime_ltv = onetime_seg["avg_lifetime_value"].values[0] if len(onetime_seg) > 0 else 0

    # ── Quarterly best growth ─────────────────────────────────
    quarterly["pct_change"] = quarterly["quarterly_revenue"].pct_change() * 100
    best_qtr = quarterly.loc[quarterly["pct_change"].idxmax()] if not quarterly["pct_change"].isna().all() else None

    # ── Build Report Text ─────────────────────────────────────
    lines = []
    def h1(text): lines.append(f"\n{'='*60}\n  {text}\n{'='*60}")
    def h2(text): lines.append(f"\n{'─'*50}\n  {text}\n{'─'*50}")
    def li(text): lines.append(f"  • {text}")
    def blank(): lines.append("")

    lines.append(f"""
╔══════════════════════════════════════════════════════════╗
║     OLIST E-COMMERCE: BUSINESS INSIGHTS REPORT          ║
║     Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}                    ║
║     Dataset: Brazilian E-Commerce (Olist) — Kaggle      ║
╚══════════════════════════════════════════════════════════╝""")

    h1("1. EXECUTIVE SUMMARY — KEY PERFORMANCE INDICATORS")
    li(f"Total Delivered Orders     : {int(kpis['total_orders']):>10,}")
    li(f"Unique Customers           : {int(kpis['unique_customers']):>10,}")
    li(f"Total Revenue (BRL)        : R${float(kpis['total_revenue']):>12,.2f}")
    li(f"Average Order Value        : R${float(kpis['avg_order_value']):>12,.2f}")
    li(f"Average Review Score       : {float(kpis['avg_review_score']):>10.2f} / 5.0")
    blank()

    h1("2. REVENUE TRENDS")

    h2("2.1 Monthly Revenue")
    li(f"Best month   : {best_month['order_yearmonth']}  →  R${best_month['monthly_revenue']:,.2f}")
    li(f"Worst month  : {worst_month['order_yearmonth']}  →  R${worst_month['monthly_revenue']:,.2f}")
    li(f"Peak vs Trough ratio: {best_month['monthly_revenue'] / worst_month['monthly_revenue']:.1f}x")
    blank()

    h2("2.2 Quarterly Growth")
    for _, row in quarterly.iterrows():
        chg = f"{row['pct_change']:+.1f}%" if not pd.isna(row["pct_change"]) else "  —  "
        li(f"{row['period']}  Revenue: R${row['quarterly_revenue']:>12,.0f}   QoQ Growth: {chg}")
    blank()

    h1("3. PRODUCT CATEGORY ANALYSIS")
    li(f"Top revenue category : {top_cat['category'].title()} (R${top_cat['total_revenue']:,.0f})")
    li(f"Top category orders  : {int(top_cat['total_orders']):,}")
    li(f"Top category avg price: R${top_cat['avg_price']:,.2f}")
    blank()
    li("Top 5 Categories by Revenue:")
    for _, row in cats.head(5).iterrows():
        li(f"  {row['category'].title():<35} R${row['total_revenue']:>12,.0f}  |  Avg Rating: {row['avg_rating']:.1f}★")
    blank()

    h1("4. GEOGRAPHIC ANALYSIS")
    li(f"Top state by revenue : {top_state['state']}  →  R${top_state['total_revenue']:,.0f}")
    blank()
    li("Top 5 States:")
    for _, row in states.head(5).iterrows():
        li(f"  {row['state']:<8} Orders: {int(row['total_orders']):>6,}   Revenue: R${row['total_revenue']:>12,.0f}")
    blank()

    h1("5. CUSTOMER SEGMENTATION")
    for _, row in segments.iterrows():
        seg_name = row["customer_segment"].split(" - ")[1]
        li(f"{seg_name:<28} | Customers: {int(row['num_customers']):>7,} | Avg LTV: R${row['avg_lifetime_value']:>8,.2f} | Revenue: R${row['segment_revenue']:>12,.0f}")
    blank()
    li(f"Loyal customers spend {loyal_ltv / onetime_ltv:.1f}x more than one-time buyers on average.")
    blank()

    h1("6. PAYMENT BEHAVIOUR")
    li(f"Most used payment method : {top_payment['payment_type'].title()} ({top_payment['total_orders']:,} orders)")
    blank()
    for _, row in payments.iterrows():
        li(f"  {row['payment_type'].title():<20} | Orders: {int(row['total_orders']):>7,} | Revenue: R${row['total_revenue']:>12,.0f} | Avg Installments: {row['avg_installments']:.1f}x")
    blank()

    h1("7. CUSTOMER SATISFACTION")
    li(f"Average review score : {float(kpis['avg_review_score']):.2f} / 5.0")
    li(f"5-star reviews       : {five_star_pct}% of all reviews")
    li(f"1-star reviews       : {one_star_pct}% of all reviews")
    blank()
    li("Review Score Breakdown:")
    for _, row in reviews.iterrows():
        bar = "█" * int(row["percentage"] / 2)
        li(f"  {int(row['score'])}★  {bar:<30} {row['percentage']:>5}%  ({int(row['num_reviews']):,} reviews)")
    blank()

    h1("8. SEASONAL PATTERNS")
    li(f"Peak month    : {peak_season['order_month_name']}  →  R${peak_season['total_revenue']:,.0f}")
    li(f"Slowest month : {low_season['order_month_name']}  →  R${low_season['total_revenue']:,.0f}")
    blank()

    h1("9. KEY BUSINESS INSIGHTS & RECOMMENDATIONS")
    blank()
    lines.append("  INSIGHT 1 — Revenue Concentration")
    li(f"  The top state ({top_state['state']}) contributes disproportionately to revenue.")
    li("  → Opportunity: invest in marketing for underperforming states.")
    blank()
    lines.append("  INSIGHT 2 — One-Time Buyer Problem")
    onetime_pct = onetime_seg["num_customers"].values[0] / segments["num_customers"].sum() * 100 if len(onetime_seg) > 0 else 0
    li(f"  ~{onetime_pct:.0f}% of customers buy only once.")
    li("  → Opportunity: retention campaigns (email, loyalty programs) could significantly increase LTV.")
    blank()
    lines.append("  INSIGHT 3 — Credit Card Dominance")
    li(f"  {top_payment['payment_type'].title()} dominates payments but installment usage suggests price sensitivity.")
    li("  → Opportunity: offer flexible payment plans or EMI promotions for high-ticket categories.")
    blank()
    lines.append("  INSIGHT 4 — High Customer Satisfaction")
    li(f"  {five_star_pct}% of customers rate 5 stars → strong product-market fit.")
    li("  → Opportunity: leverage reviews in marketing; investigate 1-star reviews for churn signals.")
    blank()
    lines.append("  INSIGHT 5 — Seasonal Demand Spikes")
    li(f"  Revenue peaks in {peak_season['order_month_name']} — likely tied to Brazilian holidays/Black Friday.")
    li("  → Opportunity: pre-stock inventory and run promotions 2–4 weeks before peak months.")
    blank()

    h1("10. DATA SOURCES & METHODOLOGY")
    li("Dataset     : Brazilian E-Commerce Public Dataset by Olist (Kaggle)")
    li("Time Period  : 2016–2018 (2017–2018 used for trend analysis)")
    li("Tools Used  : Python (Pandas), SQLite (SQL), Matplotlib, Seaborn")
    li("Scope       : Delivered orders only (to reflect actual revenue)")
    blank()
    lines.append("=" * 60)
    lines.append("  End of Report")
    lines.append("=" * 60)

    report_text = "\n".join(lines)

    # ── Save .txt ─────────────────────────────────────────────
    txt_path = os.path.join(REPORTS_DIR, "insights_report.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    # ── Save .md ──────────────────────────────────────────────
    md_lines = []
    for line in lines:
        if "═══" in line or "╔" in line or "╚" in line or "╗" in line or "║" in line:
            md_lines.append(line.replace("═", "─"))
        elif line.startswith("\n  ") and "─" not in line:
            md_lines.append(f"\n## {line.strip()}\n")
        else:
            md_lines.append(line)

    md_path = os.path.join(REPORTS_DIR, "insights_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"\n  ✔ Saved: outputs/reports/insights_report.txt")
    print(f"  ✔ Saved: outputs/reports/insights_report.md")
    print()
    print(report_text)
    print()
    print("=" * 55)
    print("  Project Complete! All outputs in the outputs/ folder.")
    print("=" * 55)


if __name__ == "__main__":
    generate_report()
