# ============================================================
# TASK 1: DataFrame Fundamentals
# Run: python 01_dataframe_fundamentals.py
# Works on Windows, Mac, and Linux
# ============================================================

import pandas as pd
import sqlite3
import os

# ── Cross-platform folder (works on Windows + Mac + Linux) ─
SAVE_DIR = os.path.join(os.path.expanduser("~"), "pandas_files")
os.makedirs(SAVE_DIR, exist_ok=True)   # creates folder if missing
print(f"📁 Files will be saved to: {SAVE_DIR}")

print("=" * 55)
print("  TASK 1: DataFrame Fundamentals")
print("=" * 55)

# ── 1. Creating DataFrames ────────────────────────────────
print("\n📌 1. Creating DataFrames")

# From a dictionary
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Charlie", "Diana"],
    "age":    [25, 30, 35, 28],
    "city":   ["Delhi", "Mumbai", "Bangalore", "Chennai"],
    "salary": [50000, 60000, 70000, 55000]
})
print(df)

# From a list of dicts
students = pd.DataFrame([
    {"name": "Raj",   "score": 85, "grade": "A"},
    {"name": "Priya", "score": 92, "grade": "A+"},
    {"name": "Sam",   "score": 78, "grade": "B"},
])
print("\nStudents DataFrame:")
print(students)

# ── 2. Read CSV / Excel / JSON / SQL ─────────────────────
print("\n📌 2. Reading Data Files")

# ---------- CSV ----------
csv_path = os.path.join(SAVE_DIR, "sample.csv")
df.to_csv(csv_path, index=False)          # CREATES the CSV file
print(f"✅ CSV saved  → {csv_path}")

df_csv = pd.read_csv(csv_path)            # READ it back
print("\nRead from CSV:")
print(df_csv)

# ---------- Excel ----------
xlsx_path = os.path.join(SAVE_DIR, "sample.xlsx")
df.to_excel(xlsx_path, index=False)       # CREATES the Excel file
print(f"\n✅ Excel saved → {xlsx_path}")

df_excel = pd.read_excel(xlsx_path)       # READ it back
print("\nRead from Excel:")
print(df_excel)

# ---------- JSON ----------
json_path = os.path.join(SAVE_DIR, "sample.json")
df.to_json(json_path, orient="records", indent=2)   # CREATES JSON
print(f"\n✅ JSON saved  → {json_path}")

df_json = pd.read_json(json_path)          # READ it back
print("\nRead from JSON:")
print(df_json)

# ---------- SQL (in-memory SQLite, no file needed) ----------
conn = sqlite3.connect(":memory:")
df.to_sql("employees", conn, if_exists="replace", index=False)
df_sql = pd.read_sql("SELECT * FROM employees", conn)
print("\nRead from SQL (SQLite in-memory):")
print(df_sql)

# ── 3. Viewing Data ───────────────────────────────────────
print("\n📌 3. Viewing Data")

big_df = pd.DataFrame({
    "id":    range(1, 11),
    "value": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    "label": ["A","B","C","D","E","F","G","H","I","J"]
})

print("head(3):"); print(big_df.head(3))
print("\ntail(3):"); print(big_df.tail(3))
print("\ninfo():");  big_df.info()
print("\ndescribe():"); print(big_df.describe())
print("\nshape   :", big_df.shape)
print("columns :", list(big_df.columns))
print("dtypes  :\n", big_df.dtypes)

# ── 4. Selecting Columns & Rows ──────────────────────────
print("\n📌 4. Selecting Columns & Rows")

print("Single column 'name':")
print(df["name"])

print("\nMultiple columns ['name','salary']:")
print(df[["name", "salary"]])

print("\nRow 0 by position (iloc):")
print(df.iloc[0])

print("\nRows 1 to 2 (iloc[1:3]):")
print(df.iloc[1:3])

df_idx = df.set_index("name")
print("\nRow 'Bob' by label (loc):")
print(df_idx.loc["Bob"])

# ── 5. Filtering with Conditions ─────────────────────────
print("\n📌 5. Filtering with Conditions")

print("age > 28:")
print(df[df["age"] > 28])

print("\nage > 25 AND salary >= 60000:")
print(df[(df["age"] > 25) & (df["salary"] >= 60000)])

print("\ncity in ['Delhi', 'Mumbai']:")
print(df[df["city"].isin(["Delhi", "Mumbai"])])

print("\nquery('salary > 55000'):")
print(df.query("salary > 55000"))

print("\n✅ Task 1 Complete!")
print(f"📁 Check your saved files at: {SAVE_DIR}\n")