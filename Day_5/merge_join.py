# ============================================================
# TASK 5: Merge & Join Operations
# Run: python 05_merge_join.py
# ============================================================

import pandas as pd

print("=" * 55)
print("  TASK 5: Merge & Join Operations")
print("=" * 55)

# ── Sample Tables ─────────────────────────────────────────
employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4, 5],
    "name":   ["Alice","Bob","Charlie","Diana","Eve"],
    "dept_id":[101, 102, 102, 103, 104]      # 104 → no matching dept
})

departments = pd.DataFrame({
    "dept_id":  [101, 102, 103, 105],         # 105 → no matching employee
    "dept_name":["HR","IT","Finance","Marketing"]
})

salaries = pd.DataFrame({
    "emp_id": [1, 2, 3, 4],                   # Eve has no salary row
    "salary": [50000, 80000, 75000, 60000]
})

print("Employees:\n", employees.to_string(index=False))
print("\nDepartments:\n", departments.to_string(index=False))
print("\nSalaries:\n", salaries.to_string(index=False))

# ── 1. INNER JOIN (only matching rows) ───────────────────
print("\n📌 1. INNER JOIN")
inner = pd.merge(employees, departments, on="dept_id", how="inner")
print(inner.to_string(index=False))
# Eve (dept_id 104) and Marketing (dept_id 105) are excluded

# ── 2. LEFT JOIN (all left rows kept) ────────────────────
print("\n📌 2. LEFT JOIN")
left = pd.merge(employees, departments, on="dept_id", how="left")
print(left.to_string(index=False))
# Eve stays; dept_name is NaN

# ── 3. RIGHT JOIN (all right rows kept) ──────────────────
print("\n📌 3. RIGHT JOIN")
right = pd.merge(employees, departments, on="dept_id", how="right")
print(right.to_string(index=False))
# Marketing stays; emp_id/name is NaN

# ── 4. OUTER JOIN (all rows from both) ───────────────────
print("\n📌 4. OUTER (FULL) JOIN")
outer = pd.merge(employees, departments, on="dept_id", how="outer")
print(outer.to_string(index=False))

# ── 5. Merge on Different Column Names ───────────────────
print("\n📌 5. Merge on Different Key Names")
emp2 = employees.rename(columns={"emp_id": "id"})
sal2 = salaries.copy()   # still has emp_id
merged = pd.merge(emp2, sal2, left_on="id", right_on="emp_id", how="left")
print(merged.to_string(index=False))

# ── 6. Merge Multiple Tables ──────────────────────────────
print("\n📌 6. Chaining Multiple Merges")
full = (employees
        .merge(departments, on="dept_id", how="left")
        .merge(salaries,    on="emp_id",  how="left"))
full["salary"] = full["salary"].fillna(0).astype(int)
print(full.to_string(index=False))

# ── 7. concat – stack DataFrames ─────────────────────────
print("\n📌 7. concat (stack rows)")

q1 = pd.DataFrame({"month":["Jan","Feb","Mar"],"sales":[100,120,110]})
q2 = pd.DataFrame({"month":["Apr","May","Jun"],"sales":[130,140,160]})

combined = pd.concat([q1, q2], ignore_index=True)
print(combined.to_string(index=False))

# concat with keys → creates a multi-level index
labeled = pd.concat([q1, q2], keys=["Q1","Q2"])
print("\nWith keys:\n", labeled)

# ── 8. join() – index-based merge ─────────────────────────
print("\n📌 8. join() on Index")

e = employees.set_index("emp_id")
s = salaries.set_index("emp_id")
joined = e.join(s, how="left")
print(joined.to_string())

print("\n✅ Task 5 Complete!\n")