# Data Setup Instructions

This project uses the **Brazilian E-Commerce Public Dataset by Olist** from Kaggle.

## Steps to Download:

1. Go to: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Click **Download** (you need a free Kaggle account)
3. Unzip the downloaded file
4. Place ALL the CSV files directly inside this `data/` folder

## Required CSV Files:
- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv
- olist_customers_dataset.csv
- olist_products_dataset.csv
- olist_sellers_dataset.csv
- olist_order_reviews_dataset.csv
- product_category_name_translation.csv

## After placing the files, run:
```
cd ecommerce-sales-analysis
pip install -r requirements.txt
python src/01_data_cleaning.py
python src/02_sql_analysis.py
python src/03_visualizations.py
python src/04_insights_report.py
```
