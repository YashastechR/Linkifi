"""
Pandas with SQL
===============
Install: pip install pandas sqlalchemy psycopg2-binary
"""

import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# ── CONNECTION (SQLAlchemy engine used by pandas) ─────────────────────────────
DB_URL = "postgresql+psycopg2://postgres:Yashas%40123@localhost:5433/mydb"
engine = create_engine(DB_URL)


# ── 1. read_sql_query() — run any SELECT, get a DataFrame ────────────────────
def demo_read_sql_query():
    print("\n── read_sql_query() ──────────────────────────────")

    # Basic query
    df = pd.read_sql_query("SELECT * FROM employees ORDER BY salary DESC;", engine)
    print(df)

    # Query with parameters (use %(name)s style with pandas)
    df_eng = pd.read_sql_query(
        "SELECT name, salary FROM employees WHERE dept = %(dept)s;",
        engine,
        params={"dept": "Engineering"}
    )
    print(f"\nEngineering team:\n{df_eng}")

    # Parse date columns automatically
    df_dated = pd.read_sql_query(
        "SELECT * FROM employees;",
        engine,
        parse_dates=["created_at"],
        index_col="id"
    )
    print(f"\nWith date parsing:\n{df_dated.dtypes}")
    return df


# ── 2. read_sql_table() — read entire table ───────────────────────────────────
def demo_read_sql_table():
    print("\n── read_sql_table() ──────────────────────────────")

    # Read full table
    df = pd.read_sql_table("employees", engine)
    print(f"Full table shape: {df.shape}")
    print(df.head())

    # Read specific columns only
    df_slim = pd.read_sql_table(
        "employees",
        engine,
        columns=["name", "dept", "salary"]
    )
    print(f"\nSelected columns:\n{df_slim}")
    return df


# ── 3. to_sql() — write DataFrame to database ────────────────────────────────
def demo_to_sql():
    print("\n── to_sql() ──────────────────────────────────────")

    # Create a sample DataFrame
    df = pd.DataFrame({
        "product": ["Laptop", "Phone", "Tablet", "Monitor"],
        "price":   [1200.00, 800.00, 450.00, 350.00],
        "stock":   [50, 120, 80, 40],
        "category": ["Electronics"] * 4
    })

    # if_exists options: 'fail' | 'replace' | 'append'
    df.to_sql(
        name="products",
        con=engine,
        if_exists="replace",   # drop & recreate each run
        index=False,           # don't write the DataFrame index as a column
        dtype=None             # let pandas infer types
    )
    print("✅ DataFrame written to 'products' table.")

    # Verify
    result = pd.read_sql_table("products", engine)
    print(result)


# ── 4. CHUNK PROCESSING — for large tables ────────────────────────────────────
def demo_chunk_processing():
    print("\n── Chunk Processing ──────────────────────────────")

    # Read in chunks of 2 rows (use larger values like 10_000 in production)
    total_salary = 0
    chunk_count  = 0

    for chunk in pd.read_sql_query(
        "SELECT * FROM employees;",
        engine,
        chunksize=2           # process 2 rows at a time
    ):
        chunk_salary  = chunk["salary"].sum()
        total_salary += chunk_salary
        chunk_count  += 1
        print(f"  Chunk {chunk_count}: {len(chunk)} rows, salary sum = {chunk_salary}")

    print(f"  ✅ Total salary across all chunks: ${total_salary:,.2f}")


# ── 5. PANDAS ANALYSIS on SQL data ───────────────────────────────────────────
def demo_analysis():
    print("\n── Analysis on SQL Data ──────────────────────────")

    df = pd.read_sql_query("SELECT dept, salary FROM employees;", engine)

    summary = df.groupby("dept")["salary"].agg(
        count="count",
        mean="mean",
        min="min",
        max="max"
    ).round(2)

    print("Department salary summary:")
    print(summary)

    # Write analysis result back to DB
    summary.reset_index().to_sql(
        "dept_salary_summary", engine, if_exists="replace", index=False
    )
    print("✅ Analysis saved to 'dept_salary_summary' table.")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo_read_sql_query()
    demo_read_sql_table()
    demo_to_sql()
    demo_chunk_processing()
    demo_analysis()
