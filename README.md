# 🛒 E-Commerce Sales Analysis — Olist Dataset

> A complete end-to-end data analysis project covering data cleaning, SQL querying, visualization, and business insights — using the Brazilian E-Commerce (Olist) dataset from Kaggle.

---

## 📌 Project Overview

This project simulates a real-world **Data Analyst workflow** on a publicly available e-commerce dataset. It answers key business questions:

- What are the **top-selling product categories**?
- How has **revenue trended** month-over-month and quarter-over-quarter?
- Which **states** drive the most revenue?
- What does **customer segmentation** reveal about buying behavior?
- What are the **seasonal demand patterns**?

---

## 🗂️ Project Structure

```
ecommerce-sales-analysis/
│
├── data/                          ← Place Kaggle CSV files here
│   └── README.md                  ← Download instructions
│
├── sql/
│   └── queries.sql                ← All 12 SQL analysis queries
│
├── src/
│   ├── 01_data_cleaning.py        ← Load, clean & merge datasets
│   ├── 02_sql_analysis.py         ← Run SQL via SQLite, save results
│   ├── 03_visualizations.py       ← 8 charts with Matplotlib/Seaborn
│   └── 04_insights_report.py      ← Auto-generate business report
│
├── outputs/
│   ├── master_cleaned.csv         ← Cleaned master dataset
│   ├── sql_results/               ← CSV results for each SQL query
│   ├── charts/                    ← 8 saved chart images
│   └── reports/                   ← insights_report.txt / .md
│
├── requirements.txt
└── README.md
```

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Core language |
| **Pandas** | Data cleaning & manipulation |
| **SQLite (built-in)** | SQL queries — no DB setup required |
| **Matplotlib** | Chart rendering |
| **Seaborn** | Statistical visualizations |

> ✅ 100% free tools — no paid software or cloud services required.

---

## 📦 Dataset

**Brazilian E-Commerce Public Dataset by Olist**
- Source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Size: ~100,000 orders | 2016–2018
- Files: 8 relational CSV files (orders, products, customers, payments, reviews, etc.)

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the dataset
- Visit: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Download & unzip all CSV files into the `data/` folder

### 4. Run the pipeline (in order)
```bash
python src/01_data_cleaning.py      # Clean & merge data
python src/02_sql_analysis.py       # Run SQL queries
python src/03_visualizations.py     # Generate charts
python src/04_insights_report.py    # Generate report
```

All outputs are saved in the `outputs/` folder.

---

## 📊 Analysis Performed

| # | Analysis | File |
|---|----------|------|
| 1 | Overall KPIs (Revenue, Orders, AOV) | `sql/queries.sql` — Q1 |
| 2 | Monthly Revenue Trend | Q2 |
| 3 | Top 10 Product Categories | Q3 |
| 4 | Revenue by Customer State | Q4 |
| 5 | Customer Segmentation (RFM-lite) | Q5 |
| 6 | Payment Method Analysis | Q6 |
| 7 | Quarterly Growth Rate | Q7 |
| 8 | Review Score Distribution | Q8 |
| 9 | Top Sellers by Revenue | Q9 |
| 10 | Seasonal Demand Patterns | Q10 |
| 11 | High-Value Customer Identification | Q11 (Bonus) |
| 12 | Category Quadrant Analysis | Q12 (Bonus) |

---

## 📈 Sample Charts Generated

- Monthly Revenue & Order Volume (Dual-axis line + bar)
- Top 10 Product Categories (Horizontal bar)
- Revenue by State (Bar chart)
- Customer Segments (Donut + LTV bar)
- Payment Methods (Pie + installments bar)
- Quarterly Revenue Growth (Bar + QoQ line)
- Review Score Distribution (Colored bar)
- Seasonal Patterns by Month (Bar chart)

---

## 💡 Key Business Insights

1. **Revenue Concentration** — A single state drives a disproportionate share of revenue, indicating a geographic expansion opportunity.
2. **One-Time Buyer Problem** — The majority of customers purchase only once; retention programs could significantly improve LTV.
3. **Credit Card Dominance** — High installment usage signals price sensitivity and opportunity for flexible payment promotions.
4. **Strong Customer Satisfaction** — 5-star reviews dominate, validating product-market fit.
5. **Seasonal Spikes** — Revenue peaks align with Brazilian holidays and Black Friday, enabling proactive inventory planning.

---

## 🧠 Skills Demonstrated

- ✅ Data cleaning (nulls, duplicates, type casting, date parsing)
- ✅ Multi-table SQL joins & aggregations
- ✅ Window functions (`OVER`, `PARTITION BY`)
- ✅ CTEs (Common Table Expressions)
- ✅ Business metric calculation (AOV, LTV, QoQ growth)
- ✅ Data visualization best practices
- ✅ Business insight communication

---

## 👤 Author

**[Your Name]**
- LinkedIn: [linkedin.com/in/yourname](https://linkedin.com/in/yourname)
- GitHub: [github.com/yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
The Olist dataset is provided under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
