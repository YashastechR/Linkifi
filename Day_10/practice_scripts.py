"""
Practice Scripts
================
1. CSV → PostgreSQL pipeline
2. Database → pandas analysis
3. Multi-database queries

Install: pip install pandas sqlalchemy psycopg2-binary
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from io import StringIO

# ── CONFIG ────────────────────────────────────────────────────────────────────
PG_URL     = "postgresql+psycopg2://postgres:Yashas%40123@localhost:5433/mydb"
SQLITE_URL = "sqlite:///local_copy.db"   # no setup needed — file-based

pg_engine     = create_engine(PG_URL)
sqlite_engine = create_engine(SQLITE_URL)


# ─────────────────────────────────────────────────────────────────────────────
# PRACTICE 1 — CSV → PostgreSQL Pipeline
# ─────────────────────────────────────────────────────────────────────────────
def generate_sample_csv() -> str:
    """Create a CSV string in memory (simulates a real CSV file)."""
    return """name,department,salary,start_date,performance
Alice Johnson,Engineering,95000,2021-03-15,excellent
Bob Smith,Marketing,72000,2020-07-01,good
Carol White,Engineering,88000,2019-11-20,excellent
David Lee,HR,65000,2022-01-10,average
Eve Davis,Engineering,102000,2018-05-30,excellent
Frank Brown,Marketing,68000,2021-09-14,good
Grace Kim,HR,71000,2020-02-28,good
Henry Park,Engineering,85000,2023-06-01,average
"""


def csv_to_postgres_pipeline(csv_content: str = None, filepath: str = None):
    """
    Load a CSV file (or string) into PostgreSQL.
    Usage:
        csv_to_postgres_pipeline(filepath="employees.csv")
    """
    print("\n── CSV → PostgreSQL Pipeline ─────────────────────────────")

    # Read CSV
    if filepath:
        df = pd.read_csv(filepath)
    else:
        df = pd.read_csv(StringIO(csv_content or generate_sample_csv()))

    print(f"📄 Loaded {len(df)} rows from CSV")
    print(df.head())

    # Transform
    df["start_date"]   = pd.to_datetime(df["start_date"])
    df["salary"]       = pd.to_numeric(df["salary"], errors="coerce")
    df["years_tenure"] = (pd.Timestamp.now() - df["start_date"]).dt.days // 365
    df["performance"]  = df["performance"].str.upper()

    # Drop rows where salary is null (data quality check)
    before = len(df)
    df.dropna(subset=["salary"], inplace=True)
    print(f"🧹 Dropped {before - len(df)} rows with null salary")

    # Load to PostgreSQL
    df.to_sql("csv_employees", pg_engine, if_exists="replace", index=False)
    print("✅ Loaded to 'csv_employees' table in PostgreSQL")

    # Verify
    result = pd.read_sql_query("SELECT COUNT(*) as total FROM csv_employees;", pg_engine)
    print(f"✅ Verified: {result['total'][0]} rows in database")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# PRACTICE 2 — Database → Pandas Analysis
# ─────────────────────────────────────────────────────────────────────────────
def database_analysis():
    """Pull data from PostgreSQL and run pandas analysis."""
    print("\n── Database → Pandas Analysis ────────────────────────────")

    df = pd.read_sql_query(
        "SELECT department, salary, performance, years_tenure FROM csv_employees;",
        pg_engine
    )

    # ── Summary stats per department
    dept_summary = df.groupby("department").agg(
        headcount  =("salary", "count"),
        avg_salary =("salary", "mean"),
        max_salary =("salary", "max"),
        min_salary =("salary", "min"),
        avg_tenure =("years_tenure", "mean")
    ).round(2)
    print("\n📊 Department Summary:")
    print(dept_summary)

    # ── Performance distribution
    perf_counts = df["performance"].value_counts()
    print(f"\n🎯 Performance Distribution:\n{perf_counts}")

    # ── Salary bands
    df["salary_band"] = pd.cut(
        df["salary"],
        bins=[0, 70000, 85000, 100000, float("inf")],
        labels=["<70k", "70-85k", "85-100k", ">100k"]
    )
    print(f"\n💰 Salary Bands:\n{df['salary_band'].value_counts()}")

    # ── Correlation
    numeric = df[["salary", "years_tenure"]]
    corr = numeric.corr()
    print(f"\n🔗 Salary vs Tenure correlation: {corr.loc['salary', 'years_tenure']:.3f}")

    # Save analysis to DB
    dept_summary.reset_index().to_sql(
        "analysis_dept_summary", pg_engine, if_exists="replace", index=False
    )
    print("\n✅ Analysis saved to 'analysis_dept_summary' table")


# ─────────────────────────────────────────────────────────────────────────────
# PRACTICE 3 — Multi-Database Queries
# ─────────────────────────────────────────────────────────────────────────────
def multi_database_queries():
    """
    Demonstrates reading from two databases (PostgreSQL + SQLite)
    and joining/comparing in pandas memory.
    """
    print("\n── Multi-Database Queries ────────────────────────────────")

    # Seed SQLite with a small reference table
    ref_data = pd.DataFrame({
        "department": ["Engineering", "Marketing", "HR"],
        "budget":     [500000, 200000, 150000],
        "location":   ["NYC", "Chicago", "Austin"]
    })
    ref_data.to_sql("dept_reference", sqlite_engine, if_exists="replace", index=False)
    print("✅ Seeded SQLite 'dept_reference' table")

    # Read from PostgreSQL
    pg_df = pd.read_sql_query(
        "SELECT department, AVG(salary) as avg_salary, COUNT(*) as headcount "
        "FROM csv_employees GROUP BY department;",
        pg_engine
    )
    print(f"\n📋 PostgreSQL data:\n{pg_df}")

    # Read from SQLite
    sqlite_df = pd.read_sql_query(
        "SELECT * FROM dept_reference;",
        sqlite_engine
    )
    print(f"\n📋 SQLite data:\n{sqlite_df}")

    # JOIN in pandas memory (cross-database join!)
    merged = pd.merge(pg_df, sqlite_df, on="department", how="left")
    merged["salary_to_budget_ratio"] = (
        (merged["avg_salary"] * merged["headcount"]) / merged["budget"]
    ).round(3)

    print("\n🔗 Cross-database JOIN result:")
    print(merged[["department", "avg_salary", "headcount", "budget",
                  "location", "salary_to_budget_ratio"]])

    # Save merged result back to PostgreSQL
    merged.to_sql("cross_db_analysis", pg_engine, if_exists="replace", index=False)
    print("\n✅ Cross-DB analysis saved to PostgreSQL 'cross_db_analysis'")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = csv_to_postgres_pipeline()
    database_analysis()
    multi_database_queries()
