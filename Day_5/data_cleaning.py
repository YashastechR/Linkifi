# ============================================================
# TASK 2: Data Cleaning
# Run: python 02_data_cleaning.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 55)
print("  TASK 2: Data Cleaning")
print("=" * 55)

# Sample messy dataset
raw = pd.DataFrame({
    "Name":    ["Alice", "Bob", None, "Diana", "Bob", "Eve"],
    "Age":     [25, None, 35, 28, 30, "twenty"],
    "Salary":  [50000, 60000, None, 55000, 60000, 45000],
    "email":   ["alice@x.com","BOB@X.COM",None,"diana@x.com","bob@x.com","eve@x.com"],
    "dept":    ["HR","IT","IT",None,"IT","Finance"],
    "Joining": ["2020-01-01","2019-06-15","2021-03-01","2018-11-20","2019-06-15","2022-08-10"]
})

print("Raw (messy) data:")
print(raw)

# ── 1. Handle Missing Values ─────────────────────────────
print("\n📌 1. Missing Values")

print("Missing count per column:\n", raw.isnull().sum())

df = raw.copy()

# dropna – drop rows where Name is missing
df_dropped = df.dropna(subset=["Name"])
print("\nAfter dropna(subset=['Name']):", len(df_dropped), "rows")

# fillna – fill missing salary with median
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")  # fix bad types first
df["Salary"] = df["Salary"].fillna(df["Salary"].median())
print("\nSalary after fillna(median):\n", df["Salary"])

# fill missing dept with "Unknown"
df["dept"] = df["dept"].fillna("Unknown")

# forward-fill (useful for time series)
df["Name"] = df["Name"].ffill()   # carry previous value forward
print("\nName after ffill:\n", df["Name"])

# ── 2. Remove Duplicates ─────────────────────────────────
print("\n📌 2. Remove Duplicates")

print("Duplicates before:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicates after :", df.duplicated().sum())
print("Rows after dedup  :", len(df))

# ── 3. Data Type Conversion ──────────────────────────────
print("\n📌 3. Data Type Conversion")

df["Age"] = pd.to_numeric(df["Age"], errors="coerce")   # "twenty" → NaN
df["Age"] = df["Age"].fillna(df["Age"].median()).astype(int)
df["Joining"] = pd.to_datetime(df["Joining"])
df["Salary"] = df["Salary"].astype(int)

print("Dtypes after conversion:\n", df.dtypes)

# ── 4. String Operations ──────────────────────────────────
print("\n📌 4. String Operations")

df["Name"]  = df["Name"].str.strip().str.title()       # fix casing + spaces
df["email"] = df["email"].str.lower().str.strip()      # lowercase emails

# Extract domain from email
df["email_domain"] = df["email"].str.split("@").str[1]

# Check if email contains a keyword
df["is_x_email"] = df["email"].str.contains("x.com", na=False)

print(df[["Name", "email", "email_domain", "is_x_email"]])

# Replace partial string
df["dept"] = df["dept"].str.replace("IT", "Information Technology", regex=False)

# ── 5. Rename Columns ─────────────────────────────────────
print("\n📌 5. Rename Columns")

df = df.rename(columns={
    "Name":    "full_name",
    "Age":     "age",
    "Salary":  "salary",
    "Joining": "joining_date"
})
# Make ALL column names lowercase at once
df.columns = df.columns.str.lower()
print("Columns after rename:", list(df.columns))

# ── 6. Reset & Set Index ──────────────────────────────────
print("\n📌 6. Reset & Set Index")

df = df.reset_index(drop=True)        # clean 0-based index after dedup
print("After reset_index:\n", df.index.tolist())

df_indexed = df.set_index("full_name")    # use name as index
print("\nWith full_name as index:\n", df_indexed[["age", "salary"]])

df_indexed = df_indexed.reset_index()    # back to default
print("\nReset back to default index — done!")

print("\n✅ Task 2 Complete!\n")
print("Final clean DataFrame:")
print(df[["full_name","age","salary","dept","joining_date"]].to_string(index=False))