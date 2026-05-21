"""
=============================================================
TASK 1: Combining DataFrames
=============================================================
Topics: merge, concat, join, inner/left/right/outer joins,
        handling merge keys, multi-key merges

WHERE TO RUN:
  - Terminal:  python 01_combining_dataframes.py
  - Jupyter:   jupyter notebook  → paste each section into cells
=============================================================
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("TASK 1: COMBINING DATAFRAMES")
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# SAMPLE DATA — three realistic tables
# ─────────────────────────────────────────────────────────────
customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name":        ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "city":        ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad"],
})

orders = pd.DataFrame({
    "order_id":    [101, 102, 103, 104, 105, 106],
    "customer_id": [1,   2,   2,   3,   6,   4],       # customer 6 doesn't exist → tests outer join
    "amount":      [250, 450, 300, 150, 500, 200],
    "product":     ["Laptop", "Phone", "Tablet", "Earbuds", "Watch", "Camera"],
})

products = pd.DataFrame({
    "product":     ["Laptop", "Phone", "Tablet", "Earbuds", "Watch"],
    "category":    ["Electronics", "Electronics", "Electronics", "Accessories", "Accessories"],
    "price":       [60000, 25000, 35000, 2000, 15000],
})

print("\n--- Source Tables ---")
print("\ncustomers:\n", customers)
print("\norders:\n", orders)
print("\nproducts:\n", products)

# ─────────────────────────────────────────────────────────────
# 1. INNER JOIN — only matching rows from both tables
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("1. INNER JOIN (default) — only matched rows")
print("─" * 50)

inner = pd.merge(customers, orders, on="customer_id", how="inner")
print(inner)
# Note: customer 5 (Eve) has no orders → excluded
# Note: order 105 (customer_id=6) has no customer → excluded

# ─────────────────────────────────────────────────────────────
# 2. LEFT JOIN — all rows from LEFT table; NaN where no match
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("2. LEFT JOIN — keep all customers (left table)")
print("─" * 50)

left = pd.merge(customers, orders, on="customer_id", how="left")
print(left)
# Eve (customer 5) appears with NaN in order columns

# ─────────────────────────────────────────────────────────────
# 3. RIGHT JOIN — all rows from RIGHT table; NaN where no match
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("3. RIGHT JOIN — keep all orders (right table)")
print("─" * 50)

right = pd.merge(customers, orders, on="customer_id", how="right")
print(right)
# Order 105 (customer_id=6) appears with NaN in customer columns

# ─────────────────────────────────────────────────────────────
# 4. OUTER JOIN — all rows from BOTH tables
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("4. OUTER (FULL) JOIN — all rows from both tables")
print("─" * 50)

outer = pd.merge(customers, orders, on="customer_id", how="outer", indicator=True)
print(outer)
# _merge column shows: both / left_only / right_only

# ─────────────────────────────────────────────────────────────
# 5. MULTI-KEY MERGE — merge on more than one column
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("5. MULTI-KEY MERGE")
print("─" * 50)

inventory = pd.DataFrame({
    "product":  ["Laptop", "Phone", "Laptop", "Phone"],
    "city":     ["Mumbai", "Mumbai", "Delhi", "Delhi"],
    "stock":    [10, 25, 5, 40],
})

sales_data = pd.DataFrame({
    "product": ["Laptop", "Phone", "Laptop"],
    "city":    ["Mumbai", "Mumbai", "Delhi"],
    "sold":    [3, 10, 2],
})

multi = pd.merge(inventory, sales_data, on=["product", "city"], how="left")
multi["remaining"] = multi["stock"] - multi["sold"].fillna(0)
print(multi)

# ─────────────────────────────────────────────────────────────
# 6. MERGE WITH DIFFERENT COLUMN NAMES (left_on / right_on)
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("6. MERGE — different column names in each table")
print("─" * 50)

staff = pd.DataFrame({
    "emp_id": [1, 2, 3],
    "emp_name": ["Raj", "Priya", "Arjun"],
})
salaries = pd.DataFrame({
    "employee_id": [1, 2, 4],
    "monthly_pay": [50000, 60000, 45000],
})

diff_keys = pd.merge(staff, salaries,
                     left_on="emp_id", right_on="employee_id",
                     how="left")
print(diff_keys)

# ─────────────────────────────────────────────────────────────
# 7. CONCAT — stack DataFrames vertically or horizontally
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("7a. CONCAT — vertical (append rows)")
print("─" * 50)

q1 = pd.DataFrame({"month": ["Jan","Feb","Mar"], "sales": [100, 120, 110]})
q2 = pd.DataFrame({"month": ["Apr","May","Jun"], "sales": [130, 115, 140]})
q3 = pd.DataFrame({"month": ["Jul","Aug","Sep"], "sales": [160, 155, 170]})

all_quarters = pd.concat([q1, q2, q3], ignore_index=True)
print(all_quarters)

print("\n7b. CONCAT — horizontal (add columns side by side)")
revenue = pd.DataFrame({"revenue": [500, 600, 700, 550, 620, 710, 800, 790, 850]})
combined = pd.concat([all_quarters, revenue], axis=1)
print(combined)

# ─────────────────────────────────────────────────────────────
# 8. .join() — index-based join
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("8. .join() — index-based join")
print("─" * 50)

ratings = pd.DataFrame(
    {"rating": [4.5, 3.8, 4.2, 4.7, 3.9]},
    index=["Laptop", "Phone", "Tablet", "Earbuds", "Watch"]
)
weights = pd.DataFrame(
    {"weight_kg": [1.8, 0.2, 0.5, 0.05, 0.15]},
    index=["Laptop", "Phone", "Tablet", "Earbuds", "Watch"]
)

joined = ratings.join(weights)
print(joined)

# ─────────────────────────────────────────────────────────────
# 9. CHAINED MERGE — 3-table join in one chain
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("9. CHAINED MERGE — customers → orders → products")
print("─" * 50)

full = (customers
        .merge(orders,   on="customer_id", how="inner")
        .merge(products, on="product",     how="left"))

full["total_value"] = full["price"] * 1   # assume qty = 1
print(full[["name", "city", "product", "category", "amount", "price"]])

# ─────────────────────────────────────────────────────────────
# 10. HANDLING DUPLICATE COLUMN NAMES with suffixes
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 50)
print("10. HANDLING DUPLICATE COLUMN NAMES (suffixes)")
print("─" * 50)

df_a = pd.DataFrame({"id": [1, 2, 3], "value": [10, 20, 30], "score": [90, 85, 88]})
df_b = pd.DataFrame({"id": [1, 2, 3], "value": [15, 25, 35], "rank":  [1, 2, 3]})

merged_dup = pd.merge(df_a, df_b, on="id", suffixes=("_before", "_after"))
print(merged_dup)

print("\n✅  Task 1 complete — all combining operations demonstrated.")