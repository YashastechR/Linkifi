# ============================================================
# TASK 4: Aggregations & Grouping
# Run: python 04_aggregations_groupby.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 55)
print("  TASK 4: Aggregations & Groupby")
print("=" * 55)

df = pd.DataFrame({
    "name":   ["Alice","Bob","Charlie","Diana","Eve","Frank","Grace","Hank"],
    "dept":   ["HR","IT","IT","Finance","HR","Finance","IT","HR"],
    "city":   ["Delhi","Mumbai","Delhi","Mumbai","Delhi","Mumbai","Delhi","Mumbai"],
    "salary": [50000,80000,75000,60000,52000,90000,70000,55000],
    "score":  [88,95,72,85,91,67,80,78],
    "gender": ["F","M","M","F","F","M","F","M"]
})

# ── 1. Basic groupby ──────────────────────────────────────
print("\n📌 1. Basic groupby")

# Mean salary per department
print("Mean salary by dept:")
print(df.groupby("dept")["salary"].mean())

# Count employees per dept
print("\nEmployee count per dept:")
print(df.groupby("dept")["name"].count())

# ── 2. Aggregate Functions ────────────────────────────────
print("\n📌 2. Aggregate Functions (sum, mean, count, min, max)")

grp = df.groupby("dept")["salary"]
print("Sum  :", grp.sum().to_dict())
print("Mean :", grp.mean().round(0).to_dict())
print("Count:", grp.count().to_dict())
print("Min  :", grp.min().to_dict())
print("Max  :", grp.max().to_dict())

# ── 3. Multiple Aggregations ──────────────────────────────
print("\n📌 3. Multiple Aggregations with agg()")

result = df.groupby("dept").agg(
    total_salary=("salary", "sum"),
    avg_salary  =("salary", "mean"),
    min_salary  =("salary", "min"),
    max_salary  =("salary", "max"),
    employee_cnt=("name",   "count"),
    avg_score   =("score",  "mean")
).round(1)

print(result.to_string())

# ── 4. Pivot Tables ───────────────────────────────────────
print("\n📌 4. Pivot Tables")

# Average salary by dept and city
pivot = pd.pivot_table(
    df,
    values  ="salary",
    index   ="dept",
    columns ="city",
    aggfunc ="mean",
    fill_value=0
)
print("Avg salary – dept × city:")
print(pivot.to_string())

# Multiple values
pivot2 = pd.pivot_table(
    df,
    values  =["salary","score"],
    index   ="dept",
    aggfunc ={"salary":"mean","score":"max"}
)
print("\nPivot – mean salary + max score per dept:")
print(pivot2.round(1).to_string())

# ── 5. Cross Tabulations ──────────────────────────────────
print("\n📌 5. Cross Tabulation (crosstab)")

# Count employees by dept × gender
ct = pd.crosstab(df["dept"], df["gender"])
print("Employee count – dept × gender:")
print(ct)

# With margins (totals)
ct_margin = pd.crosstab(df["dept"], df["city"], margins=True)
print("\nWith row/col totals:")
print(ct_margin)

# ── 6. Transform & Filter with groupby ───────────────────
print("\n📌 6. Transform & Filter")

# transform() – broadcast aggregated value back to each row
df["dept_avg_salary"] = df.groupby("dept")["salary"].transform("mean").round(0)
df["above_dept_avg"]  = df["salary"] > df["dept_avg_salary"]
print("Each row vs dept average:")
print(df[["name","dept","salary","dept_avg_salary","above_dept_avg"]].to_string(index=False))

# filter() – keep only groups that satisfy a condition
# Keep depts where average salary > 65000
high_pay_depts = df.groupby("dept").filter(lambda g: g["salary"].mean() > 65000)
print("\nDepts where avg salary > 65000:")
print(high_pay_depts[["name","dept","salary"]].to_string(index=False))

# Groupby + apply() for custom logic
def salary_summary(group):
    return pd.Series({
        "count":  len(group),
        "total":  group["salary"].sum(),
        "range":  group["salary"].max() - group["salary"].min()
    })

print("\nCustom agg with apply():")
print(df.groupby("dept").apply(salary_summary).to_string())

print("\n✅ Task 4 Complete!\n")