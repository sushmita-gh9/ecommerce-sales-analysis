"""
run_all.py — Master Pipeline Runner
=====================================
Run this ONE file to execute the entire project in order.

Usage (from the project root folder):
    python run_all.py

What it does:
  Step 1: Auto-downloads Olist dataset via kagglehub, cleans & merges data
  Step 2: Runs 10 SQL queries via SQLite
  Step 3: Generates 8 charts with Matplotlib/Seaborn
  Step 4: Generates a full business insights report
"""

import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("Step 1: Data Cleaning     (auto-downloads dataset)", os.path.join(ROOT, "src", "01_data_cleaning.py")),
    ("Step 2: SQL Analysis",                               os.path.join(ROOT, "src", "02_sql_analysis.py")),
    ("Step 3: Visualizations",                             os.path.join(ROOT, "src", "03_visualizations.py")),
    ("Step 4: Insights Report",                            os.path.join(ROOT, "src", "04_insights_report.py")),
]


def check_kagglehub():
    try:
        import kagglehub  # noqa
    except ImportError:
        print("\n  ERROR: kagglehub is not installed.")
        print("  Run:  pip install -r requirements.txt  then try again.\n")
        sys.exit(1)


def run_step(label, script_path):
    print("\n" + "=" * 60)
    print(f"  {label}")
    print("=" * 60 + "\n")
    result = subprocess.run([sys.executable, script_path], cwd=ROOT)
    if result.returncode != 0:
        print(f"\n  ERROR in '{label}'. Fix the error above and re-run.\n")
        sys.exit(result.returncode)


def main():
    print("""
+----------------------------------------------------------+
|       Olist E-Commerce Sales Analysis -- Full Run       |
+----------------------------------------------------------+
""")
    check_kagglehub()

    for label, path in STEPS:
        run_step(label, path)

    print("""
+----------------------------------------------------------+
|            All Steps Completed Successfully!            |
+----------------------------------------------------------+
  outputs/master_cleaned.csv    <- Cleaned dataset
  outputs/sql_results/          <- 10 query result CSVs
  outputs/charts/               <- 8 charts (.png)
  outputs/reports/              <- Insights report (.txt/.md)
+----------------------------------------------------------+
""")


if __name__ == "__main__":
    main()
