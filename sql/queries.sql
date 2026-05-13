-- ============================================================
-- Olist E-Commerce Sales Analysis — SQL Queries
-- Tool: SQLite (compatible with PostgreSQL/MySQL with minor edits)
-- Author: [Your Name]
-- ============================================================


-- ──────────────────────────────────────────────────────────────
-- Q1: Overall Business KPIs
-- ──────────────────────────────────────────────────────────────
SELECT
    COUNT(DISTINCT order_id)            AS total_orders,
    COUNT(DISTINCT customer_unique_id)  AS unique_customers,
    ROUND(SUM(price), 2)                AS total_revenue,
    ROUND(AVG(total_payment), 2)        AS avg_order_value,
    ROUND(AVG(review_score), 2)         AS avg_review_score
FROM orders;


-- ──────────────────────────────────────────────────────────────
-- Q2: Monthly Revenue Trend
-- ──────────────────────────────────────────────────────────────
SELECT
    order_yearmonth,
    COUNT(DISTINCT order_id)     AS num_orders,
    ROUND(SUM(price), 2)         AS monthly_revenue,
    ROUND(AVG(total_payment), 2) AS avg_order_value
FROM orders
WHERE order_year IN (2017, 2018)
GROUP BY order_yearmonth
ORDER BY order_yearmonth;


-- ──────────────────────────────────────────────────────────────
-- Q3: Top 10 Product Categories by Revenue
-- ──────────────────────────────────────────────────────────────
SELECT
    category_english                AS category,
    COUNT(DISTINCT order_id)        AS total_orders,
    ROUND(SUM(price), 2)            AS total_revenue,
    ROUND(AVG(price), 2)            AS avg_price,
    ROUND(AVG(review_score), 2)     AS avg_rating
FROM orders
WHERE category_english != 'unknown'
GROUP BY category_english
ORDER BY total_revenue DESC
LIMIT 10;


-- ──────────────────────────────────────────────────────────────
-- Q4: Revenue by Customer State (Top 10)
-- ──────────────────────────────────────────────────────────────
SELECT
    state,
    COUNT(DISTINCT order_id)     AS total_orders,
    ROUND(SUM(price), 2)         AS total_revenue,
    ROUND(AVG(total_payment), 2) AS avg_order_value
FROM orders
GROUP BY state
ORDER BY total_revenue DESC
LIMIT 10;


-- ──────────────────────────────────────────────────────────────
-- Q5: Customer Segmentation by Purchase Frequency
-- ──────────────────────────────────────────────────────────────
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
    COUNT(*)                   AS num_customers,
    ROUND(AVG(total_spent), 2) AS avg_lifetime_value,
    ROUND(SUM(total_spent), 2) AS segment_revenue
FROM customer_orders
GROUP BY customer_segment
ORDER BY customer_segment;


-- ──────────────────────────────────────────────────────────────
-- Q6: Payment Method Analysis
-- ──────────────────────────────────────────────────────────────
SELECT
    payment_type,
    COUNT(DISTINCT order_id)           AS total_orders,
    ROUND(SUM(price), 2)               AS total_revenue,
    ROUND(AVG(payment_installments), 1) AS avg_installments
FROM orders
GROUP BY payment_type
ORDER BY total_orders DESC;


-- ──────────────────────────────────────────────────────────────
-- Q7: Quarterly Revenue Growth
-- ──────────────────────────────────────────────────────────────
SELECT
    order_year,
    order_quarter,
    order_year || '-Q' || order_quarter AS period,
    COUNT(DISTINCT order_id)            AS total_orders,
    ROUND(SUM(price), 2)                AS quarterly_revenue
FROM orders
WHERE order_year IN (2017, 2018)
GROUP BY order_year, order_quarter
ORDER BY order_year, order_quarter;


-- ──────────────────────────────────────────────────────────────
-- Q8: Review Score Distribution
-- ──────────────────────────────────────────────────────────────
SELECT
    CAST(review_score AS INT) AS score,
    COUNT(*)                  AS num_reviews,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS percentage
FROM orders
WHERE review_score IS NOT NULL
GROUP BY score
ORDER BY score DESC;


-- ──────────────────────────────────────────────────────────────
-- Q9: Top 10 Sellers by Revenue
-- ──────────────────────────────────────────────────────────────
SELECT
    seller_id,
    COUNT(DISTINCT order_id)    AS total_orders,
    ROUND(SUM(price), 2)        AS total_revenue,
    ROUND(AVG(review_score), 2) AS avg_rating
FROM orders
WHERE seller_id IS NOT NULL
GROUP BY seller_id
ORDER BY total_revenue DESC
LIMIT 10;


-- ──────────────────────────────────────────────────────────────
-- Q10: Seasonal Patterns (Monthly Aggregation)
-- ──────────────────────────────────────────────────────────────
SELECT
    order_month,
    order_month_name,
    COUNT(DISTINCT order_id)  AS total_orders,
    ROUND(SUM(price), 2)      AS total_revenue
FROM orders
GROUP BY order_month, order_month_name
ORDER BY order_month;


-- ──────────────────────────────────────────────────────────────
-- BONUS Q11: High-Value Customers (Top 1% by Spend)
-- ──────────────────────────────────────────────────────────────
WITH customer_spend AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS num_orders,
        ROUND(SUM(price), 2)     AS total_spent
    FROM orders
    GROUP BY customer_unique_id
),
percentiles AS (
    SELECT PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY total_spent) AS p99
    FROM customer_spend
)
SELECT
    c.*
FROM customer_spend c, percentiles p
WHERE c.total_spent >= p.p99
ORDER BY c.total_spent DESC;


-- ──────────────────────────────────────────────────────────────
-- BONUS Q12: Category Performance vs Average (Z-Score view)
-- ──────────────────────────────────────────────────────────────
WITH cat_stats AS (
    SELECT
        category_english AS category,
        ROUND(AVG(price), 2) AS avg_price,
        ROUND(AVG(review_score), 2) AS avg_rating,
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    WHERE category_english != 'unknown'
    GROUP BY category_english
),
overall AS (
    SELECT
        AVG(avg_price)  AS mean_price,
        AVG(avg_rating) AS mean_rating
    FROM cat_stats
)
SELECT
    c.category,
    c.avg_price,
    c.avg_rating,
    c.total_orders,
    CASE
        WHEN c.avg_price > o.mean_price AND c.avg_rating > o.mean_rating THEN 'Premium Star'
        WHEN c.avg_price > o.mean_price AND c.avg_rating <= o.mean_rating THEN 'Expensive & Underperforming'
        WHEN c.avg_price <= o.mean_price AND c.avg_rating > o.mean_rating THEN 'Value Champion'
        ELSE 'Budget & Low Rated'
    END AS category_quadrant
FROM cat_stats c, overall o
ORDER BY total_orders DESC;
