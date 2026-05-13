"""
Script 01: Data Cleaning & Preprocessing
=========================================
- Auto-downloads the Olist dataset via kagglehub (no manual steps!)
- Handles nulls, duplicates, and wrong formats
- Merges into a master analytical DataFrame
- Saves cleaned data for downstream scripts

First-time setup:
  pip install kagglehub
  Run this script — it will prompt you to log in to Kaggle (free account).
  After the first run, the dataset is cached locally.
"""

import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_data_dir():
    """Auto-download the Olist dataset using kagglehub and return the path."""
    try:
        import kagglehub
    except ImportError:
        print("\n  ERROR: kagglehub is not installed.")
        print("  Run:  pip install kagglehub  then try again.\n")
        raise SystemExit(1)

    print("  Downloading dataset via kagglehub...")
    print("  (First time only: you will be prompted to log in to Kaggle)\n")
    path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    print(f"\n  Dataset ready at: {path}\n")
    return path


def load_datasets():
    """Auto-download and load all Olist CSV files."""
    print("=" * 55)
    print("  STEP 1: Loading Raw Datasets")
    print("=" * 55)

    data_dir = get_data_dir()

    files = {
        "orders":       "olist_orders_dataset.csv",
        "order_items":  "olist_order_items_dataset.csv",
        "payments":     "olist_order_payments_dataset.csv",
        "customers":    "olist_customers_dataset.csv",
        "products":     "olist_products_dataset.csv",
        "sellers":      "olist_sellers_dataset.csv",
        "reviews":      "olist_order_reviews_dataset.csv",
        "translations": "product_category_name_translation.csv",
    }

    dfs = {}
    for name, filename in files.items():
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            print(f"  ERROR: Expected file not found: {path}")
            print("  The kagglehub download may be incomplete. Delete its cache folder and retry.")
            raise SystemExit(1)
        dfs[name] = pd.read_csv(path)
        print(f"  Loaded {name:15s} -> {dfs[name].shape[0]:>7,} rows, {dfs[name].shape[1]} cols")

    return dfs


def clean_orders(df):
    """Clean orders table: fix dates, drop bad statuses."""
    print("\n[orders] Cleaning...")

    before = len(df)
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df = df[df["order_status"] == "delivered"].copy()
    df.dropna(subset=["order_purchase_timestamp"], inplace=True)

    df["order_year"]      = df["order_purchase_timestamp"].dt.year
    df["order_month"]     = df["order_purchase_timestamp"].dt.month
    df["order_month_name"]= df["order_purchase_timestamp"].dt.strftime("%B")
    df["order_quarter"]   = df["order_purchase_timestamp"].dt.quarter
    df["order_yearmonth"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

    after = len(df)
    print(f"  Rows: {before:,} -> {after:,}  (removed {before - after:,} non-delivered/null rows)")
    return df


def clean_order_items(df):
    """Clean order items: remove negatives, fix types."""
    print("[order_items] Cleaning...")

    before = len(df)
    df.drop_duplicates(inplace=True)
    df = df[df["price"] > 0]
    df = df[df["freight_value"] >= 0]
    df["total_item_value"] = df["price"] + df["freight_value"]
    after = len(df)
    print(f"  Rows: {before:,} -> {after:,}  (removed {before - after:,} invalid rows)")
    return df


def clean_payments(df):
    """Aggregate payments per order."""
    print("[payments] Cleaning...")

    df.drop_duplicates(inplace=True)
    df = df[df["payment_value"] > 0]

    agg = df.groupby("order_id").agg(
        total_payment=("payment_value", "sum"),
        payment_installments=("payment_installments", "max"),
        payment_type=("payment_type", lambda x: x.value_counts().index[0]),
    ).reset_index()

    print(f"  Aggregated to {len(agg):,} unique orders")
    return agg


def clean_products(df, translations):
    """Clean products: translate category names to English."""
    print("[products] Cleaning...")

    df.drop_duplicates(subset=["product_id"], inplace=True)
    df = df.merge(translations, on="product_category_name", how="left")
    df["category_english"] = df["product_category_name_english"].fillna("unknown")
    df.drop(columns=["product_category_name", "product_category_name_english"], inplace=True)

    print(f"  Products cleaned: {len(df):,}")
    return df


def build_master_df(dfs):
    """Join all cleaned tables into one analytical master DataFrame."""
    print("\n[MERGE] Building master DataFrame...")

    orders    = clean_orders(dfs["orders"])
    items     = clean_order_items(dfs["order_items"])
    payments  = clean_payments(dfs["payments"])
    products  = clean_products(dfs["products"], dfs["translations"])
    customers = dfs["customers"].drop_duplicates(subset=["customer_id"])
    reviews   = dfs["reviews"][["order_id", "review_score"]].drop_duplicates(subset=["order_id"])

    df = orders.merge(items,     on="order_id",    how="inner")
    df = df.merge(payments,      on="order_id",    how="left")
    df = df.merge(customers,     on="customer_id", how="left")
    df = df.merge(products,      on="product_id",  how="left")
    df = df.merge(reviews,       on="order_id",    how="left")

    df.rename(columns={"customer_state": "state"}, inplace=True)

    print(f"\n  Master DataFrame shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"  Date range: {df['order_purchase_timestamp'].min().date()} -> {df['order_purchase_timestamp'].max().date()}")
    print(f"  Nulls per key column:")
    for col in ["price", "total_payment", "category_english", "state", "review_score"]:
        pct = df[col].isna().mean() * 100
        print(f"       {col:25s}: {pct:.1f}% null")

    return df


def main():
    dfs = load_datasets()
    master = build_master_df(dfs)

    out_path = os.path.join(OUTPUT_DIR, "master_cleaned.csv")
    master.to_csv(out_path, index=False)
    print(f"\n  Saved cleaned master data -> {out_path}")
    print("\n" + "=" * 55)
    print("  Data Cleaning Complete! Run 02_sql_analysis.py next.")
    print("=" * 55)


if __name__ == "__main__":
    main()
