# ============================================================
# TASK 3: Data Transformation
# Run: python 03_data_transformation.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 55)
print("  TASK 3: Data Transformation")
print("=" * 55)

df = pd.DataFrame({
    "name":   ["Alice","Bob","Charlie","Diana","Eve","Frank"],
    "dept":   ["HR","IT","IT","Finance","HR","Finance"],
    "salary": [50000, 80000, 75000, 60000, 52000, 90000],
    "score":  [88, 95, 72, 85, 91, 67],
    "city":   ["delhi","mumbai","bangalore","delhi","mumbai","bangalore"]
})

# ── 1. Apply Functions to Columns ────────────────────────
print("\n📌 1. Apply Functions")

# apply() with a lambda
df["salary_inr"] = df["salary"].apply(lambda x: f"₹{x:,}")
print("salary_inr:\n", df["salary_inr"])

# apply on multiple columns via axis=1 (row-wise)
df["summary"] = df.apply(
    lambda row: f"{row['name']} works in {row['dept']}", axis=1
)
print("\nsummary:\n", df["summary"])

# ── 2. Create New Columns ─────────────────────────────────
print("\n📌 2. Create New Columns")

df["tax"]         = df["salary"] * 0.10          # 10% tax
df["net_salary"]  = df["salary"] - df["tax"]
df["above_avg"]   = df["salary"] > df["salary"].mean()

print(df[["name","salary","tax","net_salary","above_avg"]])

# ── 3. Map and Replace Values ─────────────────────────────
print("\n📌 3. Map & Replace")

# map() – transform using a dict
dept_code = {"HR": "H", "IT": "I", "Finance": "F"}
df["dept_code"] = df["dept"].map(dept_code)
print("\ndept_code:\n", df["dept_code"])

# replace() – replace specific values
df["city"] = df["city"].replace({
    "delhi":     "Delhi",
    "mumbai":    "Mumbai",
    "bangalore": "Bangalore"
})
print("\ncity after replace:\n", df["city"])

# ── 4. Sorting and Ranking ────────────────────────────────
print("\n📌 4. Sorting & Ranking")

# Sort by salary descending
df_sorted = df.sort_values("salary", ascending=False)
print("Sorted by salary:\n", df_sorted[["name","salary"]].to_string(index=False))

# Sort by multiple columns
df_multi = df.sort_values(["dept","salary"], ascending=[True, False])
print("\nSorted by dept then salary:\n",
      df_multi[["name","dept","salary"]].to_string(index=False))

# Rank (1 = highest salary)
df["salary_rank"] = df["salary"].rank(ascending=False).astype(int)
print("\nWith salary rank:\n", df[["name","salary","salary_rank"]].to_string(index=False))

# ── 5. Binning and Categorization ────────────────────────
print("\n📌 5. Binning")

# cut() – equal-width bins
df["salary_band"] = pd.cut(
    df["salary"],
    bins=[0, 55000, 75000, 100000],
    labels=["Low", "Mid", "High"]
)
print("\nSalary bands:\n", df[["name","salary","salary_band"]].to_string(index=False))

# qcut() – equal-frequency bins (quartiles)
df["score_tier"] = pd.qcut(df["score"], q=3, labels=["Bronze","Silver","Gold"])
print("\nScore tiers:\n", df[["name","score","score_tier"]].to_string(index=False))

# ── 6. Pivot and Melt ─────────────────────────────────────
print("\n📌 6. Pivot & Melt")

pivot_data = pd.DataFrame({
    "name":    ["Alice","Alice","Bob","Bob"],
    "metric":  ["salary","score","salary","score"],
    "value":   [50000, 88, 80000, 95]
})

# melt  – wide → long (already long in this example, but shown for demo)
wide = pd.DataFrame({
    "name":   ["Alice","Bob"],
    "salary": [50000, 80000],
    "score":  [88, 95]
})
long = wide.melt(id_vars="name", var_name="metric", value_name="value")
print("melt (wide → long):\n", long.to_string(index=False))

# pivot – long → wide
wide_again = long.pivot(index="name", columns="metric", values="value")
wide_again.columns.name = None
wide_again = wide_again.reset_index()
print("\npivot (long → wide):\n", wide_again.to_string(index=False))

print("\n✅ Task 3 Complete!\n")