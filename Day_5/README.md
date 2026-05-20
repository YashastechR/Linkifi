# Day 5 — Pandas for Data Engineering

Learning and practicing pandas through tasks and real-world mini projects.

---

## What I Learned Today

- Creating and reading DataFrames from CSV, Excel, JSON and SQL
- Cleaning messy data — handling nulls, duplicates, wrong data types
- Transforming data — new columns, apply functions, pivot, melt
- Grouping and aggregating — groupby, pivot tables, crosstab
- Merging and joining multiple tables
- Time series analysis and multi-level aggregations

---

## Tasks

### Task 1 — DataFrame Fundamentals
`01_dataframe_fundamentals.py`
- Created DataFrames from dictionaries and lists
- Read data from CSV, Excel, JSON and SQL
- Used head, tail, info, describe to explore data
- Selected columns, filtered rows with conditions

### Task 2 — Data Cleaning
`02_data_cleaning.py`
- Handled missing values using dropna and fillna
- Removed duplicate rows
- Fixed data types (numeric, datetime)
- Cleaned string columns (casing, whitespace, extract domain)
- Renamed columns and reset index

### Task 3 — Data Transformation
`03_data_transformation.py`
- Applied functions to columns using apply and lambda
- Created new calculated columns
- Used map and replace to convert values
- Sorted and ranked rows
- Binned values into categories using cut and qcut
- Converted between wide and long format using pivot and melt

### Task 4 — Aggregations and Groupby
`04_aggregations_groupby.py`
- Grouped data by one and multiple columns
- Used sum, mean, count, min, max per group
- Applied multiple aggregations at once using agg
- Built pivot tables and cross tabulations
- Used transform to broadcast group stats back to each row
- Filtered groups based on conditions

### Task 5 — Merge and Join
`05_merge_join.py`
- Inner, left, right and outer joins
- Merged on different column names
- Chained multiple merges together
- Stacked DataFrames using concat
- Index-based join using join()

---

## Projects

### Project 1 — Sales Data Cleaning
`project1_sales_cleaning.py`

Cleaned a messy sales dataset with inconsistent names, missing values and invalid dates. Calculated revenue after discount and analyzed results by product, region and quarter.

### Project 2 — Customer Analytics
`project2_customer_analytics.py`

Merged order data with customer profiles. Built customer metrics (total spend, order count, days since last order). Segmented customers into spend tiers and analyzed performance by city and segment.

### Project 3 — Time Series and Multi-level Aggregations
`project3_timeseries_multilevel.py`

Extracted time features from dates. Resampled daily data to monthly and weekly summaries. Calculated 7-day and 30-day rolling averages. Performed multi-level groupby across region, product and quarter.

---

## How to Run

**Install dependencies:**
```bash
pip install pandas openpyxl
```

**Run any file:**
```bash
python 01_dataframe_fundamentals.py
python 02_data_cleaning.py
python 03_data_transformation.py
python 04_aggregations_groupby.py
python 05_merge_join.py
python project1_sales_cleaning.py
python project2_customer_analytics.py
python project3_timeseries_multilevel.py
```

---

## Project Structure

```
day5-pandas/
├── 01_dataframe_fundamentals.py
├── 02_data_cleaning.py
├── 03_data_transformation.py
├── 04_aggregations_groupby.py
├── 05_merge_join.py
├── project1_sales_cleaning.py
├── project2_customer_analytics.py
├── project3_timeseries_multilevel.py
├── sample_files/               ← auto-created when you run Task 1
│   ├── sample.csv
│   ├── sample.xlsx
│   ├── sample.json
│   └── clean_sales.csv
└── README.md
```

---

## Tools Used

- Python 3.11
- pandas
- openpyxl
- sqlite3 (built into Python)

---

## Issues I Fixed Along the Way

| Error | Fix |
|-------|-----|
| `/tmp/` path not found on Windows | Changed to use a local `sample_files/` folder |
| `No module named openpyxl` | `pip install openpyxl` |
| `Invalid frequency: ME` on older pandas | Replaced `"ME"` with `"M"` |
| `fillna(method="ffill")` deprecated | Changed to `.ffill()` |