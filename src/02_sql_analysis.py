"""
Script 02: SQL Analysis with SQLite
=====================================
- Loads cleaned master data into an in-memory SQLite database
- Runs analytical SQL queries (no external DB setup needed)
- Saves all query results as CSV files in outputs/
"""

import sqlite3
import pandas as pd
import os

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
SQL_RESULTS_DIR = os.path.join(OUTPUT_DIR, "sql_results")
os.makedirs(SQL_RESULTS_DIR, exist_ok=True)


def load_to_sqlite(csv_path):
    """Load cleaned CSV into an in-memory SQLite database."""
    print("=" * 55)
    print("  STEP 2: SQL Analysis")
    print("=" * 55)
    print("\n  Loading data into SQLite...")

    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(":memory:")
    df.to_sql("orders", conn, index=False, if_exists="replace")
    print(f"  ✔ Loaded {len(df):,} rows into SQLite table 'orders'")
    return conn, df


def run_query(conn, label, sql):
    """Execute a SQL query and return result as DataFrame."""
    result = pd.read_sql_query(sql, conn)
    print(f"  ✔ {label} → {len(result)} rows")
    return result


def save(df, filename, label):
    path = os.path.join(SQL_RESULTS_DIR, filename)
    df.to_csv(path, index=False)
    print(f"     Saved: outputs/sql_results/{filename}")
    return df


def main():
    csv_path = os.path.join(OUTPUT_DIR, "master_cleaned.csv")
    conn, _ = load_to_sqlite(csv_path)

    print("\n  Running SQL queries...\n")

    # ── Q1: Total Revenue & Orders Overview ──────────────────
    q1 = run_query(conn, "Q1 Overall KPIs", """
        SELECT
            COUNT(DISTINCT order_id)            AS total_orders,
            COUNT(DISTINCT customer_unique_id)  AS unique_customers,
            ROUND(SUM(price), 2)                AS total_revenue,
            ROUND(AVG(total_payment), 2)        AS avg_order_value,
            ROUND(AVG(review_score), 2)         AS avg_review_score
        FROM orders
    """)
    save(q1, "01_overall_kpis.csv", "Overall KPIs")
    print(q1.to_string(index=False))

    # ── Q2: Monthly Revenue Trend ─────────────────────────────
    q2 = run_query(conn, "Q2 Monthly Revenue", """
        SELECT
            order_yearmonth,
            COUNT(DISTINCT order_id)   AS num_orders,
            ROUND(SUM(price), 2)       AS monthly_revenue,
            ROUND(AVG(total_payment), 2) AS avg_order_value
        FROM orders
        WHERE order_year IN (2017, 2018)
        GROUP BY order_yearmonth
        ORDER BY order_yearmonth
    """)
    save(q2, "02_monthly_revenue.csv", "Monthly Revenue")

    # ── Q3: Top 10 Product Categories by Revenue ─────────────
    q3 = run_query(conn, "Q3 Top Categories", """
        SELECT
            category_english                    AS category,
            COUNT(DISTINCT order_id)            AS total_orders,
            ROUND(SUM(price), 2)                AS total_revenue,
            ROUND(AVG(price), 2)                AS avg_price,
            ROUND(AVG(review_score), 2)         AS avg_rating
        FROM orders
        WHERE category_english != 'unknown'
        GROUP BY category_english
        ORDER BY total_revenue DESC
        LIMIT 10
    """)
    save(q3, "03_top_categories.csv", "Top Categories")

    # ── Q4: Revenue by Customer State ────────────────────────
    q4 = run_query(conn, "Q4 Revenue by State", """
        SELECT
            state,
            COUNT(DISTINCT order_id)   AS total_orders,
            ROUND(SUM(price), 2)       AS total_revenue,
            ROUND(AVG(total_payment), 2) AS avg_order_value
        FROM orders
        GROUP BY state
        ORDER BY total_revenue DESC
        LIMIT 10
    """)
    save(q4, "04_revenue_by_state.csv", "Revenue by State")

    # ── Q5: Customer Segmentation by Purchase Frequency ──────
    q5 = run_query(conn, "Q5 Customer Segments", """
        WITH customer_orders AS (
            SELECT
                customer_unique_id,
                COUNT(DISTINCT order_id) AS num_orders,
                ROUND(SUM(price), 2)     AS total_spent
            FROM orders
            GROUP BY customer_unique_id
        )
        SELECT
            CASE
                WHEN num_orders = 1 THEN '1 - One-Time Buyer'
                WHEN num_orders BETWEEN 2 AND 3 THEN '2 - Repeat Buyer (2-3x)'
                ELSE '3 - Loyal Customer (4+)'
            END AS customer_segment,
            COUNT(*)                        AS num_customers,
            ROUND(AVG(total_spent), 2)      AS avg_lifetime_value,
            ROUND(SUM(total_spent), 2)      AS segment_revenue
        FROM customer_orders
        GROUP BY customer_segment
        ORDER BY customer_segment
    """)
    save(q5, "05_customer_segments.csv", "Customer Segments")

    # ── Q6: Payment Method Analysis ──────────────────────────
    q6 = run_query(conn, "Q6 Payment Methods", """
        SELECT
            payment_type,
            COUNT(DISTINCT order_id)          AS total_orders,
            ROUND(SUM(price), 2)              AS total_revenue,
            ROUND(AVG(payment_installments), 1) AS avg_installments
        FROM orders
        GROUP BY payment_type
        ORDER BY total_orders DESC
    """)
    save(q6, "06_payment_methods.csv", "Payment Methods")

    # ── Q7: Quarterly Revenue Growth ─────────────────────────
    q7 = run_query(conn, "Q7 Quarterly Growth", """
        SELECT
            order_year,
            order_quarter,
            order_year || '-Q' || order_quarter AS period,
            COUNT(DISTINCT order_id)            AS total_orders,
            ROUND(SUM(price), 2)                AS quarterly_revenue
        FROM orders
        WHERE order_year IN (2017, 2018)
        GROUP BY order_year, order_quarter
        ORDER BY order_year, order_quarter
    """)
    save(q7, "07_quarterly_growth.csv", "Quarterly Growth")

    # ── Q8: Review Score Distribution ────────────────────────
    q8 = run_query(conn, "Q8 Review Distribution", """
        SELECT
            CAST(review_score AS INT)  AS score,
            COUNT(*)                   AS num_reviews,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS percentage
        FROM orders
        WHERE review_score IS NOT NULL
        GROUP BY score
        ORDER BY score DESC
    """)
    save(q8, "08_review_distribution.csv", "Review Distribution")

    # ── Q9: Top 10 Sellers by Revenue ────────────────────────
    q9 = run_query(conn, "Q9 Top Sellers", """
        SELECT
            seller_id,
            COUNT(DISTINCT order_id)   AS total_orders,
            ROUND(SUM(price), 2)       AS total_revenue,
            ROUND(AVG(review_score), 2) AS avg_rating
        FROM orders
        WHERE seller_id IS NOT NULL
        GROUP BY seller_id
        ORDER BY total_revenue DESC
        LIMIT 10
    """)
    save(q9, "09_top_sellers.csv", "Top Sellers")

    # ── Q10: Seasonal Patterns (Month-over-Month) ─────────────
    q10 = run_query(conn, "Q10 Seasonal Patterns", """
        SELECT
            order_month,
            order_month_name,
            COUNT(DISTINCT order_id)   AS total_orders,
            ROUND(SUM(price), 2)       AS total_revenue
        FROM orders
        GROUP BY order_month, order_month_name
        ORDER BY order_month
    """)
    save(q10, "10_seasonal_patterns.csv", "Seasonal Patterns")

    conn.close()
    print("\n" + "=" * 55)
    print("  SQL Analysis Complete! Run 03_visualizations.py next.")
    print("=" * 55)


if __name__ == "__main__":
    main()
