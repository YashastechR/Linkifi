# Advanced Pandas Project

## Project Structure

```
pandas_project/
├── 01_combining_dataframes.py     # Merge, concat, join operations
├── 02_time_series_analysis.py     # DateTime, resampling, rolling windows
├── 03_excel_automation.py         # Read, write, and format Excel files
├── 04_performance_optimization.py # dtypes, chunking, vectorization
├── output/                        # Generated Excel files
└── README.md
```

---

## How to Run

```bash
# Install dependencies
pip install pandas numpy openpyxl xlsxwriter

# Run each script
python 01_combining_dataframes.py
python 02_time_series_analysis.py
python 03_excel_automation.py
python 04_performance_optimization.py
```

> You can also paste any section into a **Jupyter Notebook** cell or run directly in **VS Code**.

---

## Task 1 — Combining DataFrames

```python
# Inner join (default) — only matching rows
pd.merge(df1, df2, on="key", how="inner")

# Left join — all rows from left table
pd.merge(df1, df2, on="key", how="left")

# Multi-key merge
pd.merge(df1, df2, on=["col_a", "col_b"])

# Different column names
pd.merge(df1, df2, left_on="emp_id", right_on="employee_id")

# Handle duplicate column names
pd.merge(df1, df2, on="id", suffixes=("_before", "_after"))

# Stack rows
pd.concat([df1, df2, df3], ignore_index=True)

# Add columns side by side
pd.concat([df1, df2], axis=1)

# Chained 3-table merge
df1.merge(df2, on="key1").merge(df3, on="key2")
```

---

## Task 2 — Time Series

```python
# Create DatetimeIndex
dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")

# Parse date column
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# Resample to monthly totals
df.resample("ME").sum()

# 7-day rolling average
df["MA_7"] = df["sales"].rolling(7).mean()

# Lag / shift
df["yesterday"] = df["sales"].shift(1)
df["pct_change"] = df["sales"].pct_change() * 100

# Timezone
ts = ts.tz_localize("Asia/Kolkata").tz_convert("UTC")
```

| Alias | Frequency    |
|-------|--------------|
| `D`   | Daily        |
| `B`   | Business day |
| `W`   | Weekly       |
| `ME`  | Month end    |
| `QE`  | Quarter end  |
| `YE`  | Year end     |

---

## Task 3 — Excel Automation

```bash
pip install openpyxl xlsxwriter
```

```python
# Write single sheet
df.to_excel("output.xlsx", sheet_name="Sales", index=False)

# Read all sheets at once
all_sheets = pd.read_excel("file.xlsx", sheet_name=None)  # returns dict

# Write multiple sheets
with pd.ExcelWriter("report.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="Sales")
    df2.to_excel(writer, sheet_name="Employees")

# Style headers
from openpyxl.styles import PatternFill, Font
for cell in ws[1]:
    cell.fill = PatternFill("solid", fgColor="1F4E79")
    cell.font = Font(color="FFFFFF", bold=True)

ws.freeze_panes = "A2"  # freeze header row
```

**Excel files generated:**

| File | Contents |
|------|----------|
| `sales_simple.xlsx` | Single-sheet sales data |
| `company_data.xlsx` | 3 sheets: Sales, Employees, Inventory |
| `formatted_report.xlsx` | Styled sheets with color headers and conditional formatting |
| `executive_summary.xlsx` | KPI summary + bar chart + line chart |

---

## Task 4 — Performance Optimization

### Memory savings with dtypes

| Type       | Use when                        | Savings vs default |
|------------|---------------------------------|--------------------|
| `float32`  | Decimals, full precision not needed | 50%            |
| `int8/16`  | Small integer ranges            | 75–87%             |
| `bool`     | True/False flags                | 87%                |
| `category` | Strings with few unique values  | Up to 98%          |

### Speed: slowest → fastest

```
Python loop  →  apply(axis=1)  →  apply(axis=0)  →  vectorized
  6677 ms           1082 ms           35 ms             1 ms
```

```python
# SLOW
df["result"] = df.apply(lambda row: row["a"] * 2 + row["b"], axis=1)

# FAST
df["result"] = df["a"] * 2 + df["b"]

# Conditional — use np.select instead of apply
conditions = [df["score"] >= 90, df["score"] >= 75]
df["grade"] = np.select(conditions, ["A", "B"], default="C")

# Large files — use chunksize
for chunk in pd.read_csv("big.csv", chunksize=100_000, dtype={"region": "category"}):
    process(chunk)
```

---

## Common Gotchas

| Issue | Fix |
|-------|-----|
| `SettingWithCopyWarning` | Use `.copy()` when slicing: `df2 = df[mask].copy()` |
| `KeyError` on merge | Check column names with `df.columns` |
| Dates not parsing | Use `pd.to_datetime()` or `parse_dates=["col"]` in `read_csv` |
| `NaN` after merge | Check join type; use `.fillna()` after merge |
| Memory error on large CSV | Use `chunksize` + `dtype=` in `read_csv` |
| Slow `apply` | Replace with vectorized ops or `np.where` / `np.select` |