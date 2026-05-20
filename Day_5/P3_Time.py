# ============================================================
# PROJECT 3: Time Series + Multi-level Aggregations
# Run: python project3_timeseries_multilevel.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 55)
print("  PROJECT 3: Time Series & Multi-level Aggregations")
print("=" * 55)

np.random.seed(0)

# ── Step 1: Build daily sales time series ────────────────
dates  = pd.date_range("2024-01-01", "2024-12-31", freq="D")
n      = len(dates)

ts = pd.DataFrame({
    "date":    dates,
    "region":  np.random.choice(["North","South","East","West"], n),
    "product": np.random.choice(["Laptop","Phone","Tablet"], n),
    "units":   np.random.randint(1, 20, n),
    "price":   np.random.choice([75000, 15000, 25000], n)
})
ts["revenue"] = ts["units"] * ts["price"]

print("Time series shape:", ts.shape)
print(ts.head(4).to_string(index=False))

# ── Step 2: Time-based features ───────────────────────────
print("\n📌 Time Features")

ts["year"]      = ts["date"].dt.year
ts["month"]     = ts["date"].dt.month
ts["month_name"]= ts["date"].dt.month_name()
ts["week"]      = ts["date"].dt.isocalendar().week.astype(int)
ts["day_name"]  = ts["date"].dt.day_name()
ts["quarter"]   = ts["date"].dt.quarter
ts["is_weekend"]= ts["date"].dt.dayofweek >= 5

print("Columns:", list(ts.columns))

# ── Step 3: Resample (aggregate by time period) ───────────
print("\n📌 Resample")

ts_indexed = ts.set_index("date")

# Monthly total revenue
monthly = ts_indexed["revenue"].resample("M").sum()
print("Monthly Revenue (first 6 months):")
print(monthly.head(6).to_string())

# Weekly average units
weekly_avg = ts_indexed["units"].resample("W").mean().round(1)
print("\nWeekly Avg Units (first 4 weeks):")
print(weekly_avg.head(4).to_string())

# ── Step 4: Rolling windows ───────────────────────────────
print("\n📌 Rolling Windows")

daily_rev = ts_indexed["revenue"].resample("D").sum()
daily_rev_df = daily_rev.reset_index()
daily_rev_df["7d_rolling_avg"]  = daily_rev_df["revenue"].rolling(7).mean().round(0)
daily_rev_df["30d_rolling_avg"] = daily_rev_df["revenue"].rolling(30).mean().round(0)

print("Daily revenue with rolling averages (days 30-35):")
print(daily_rev_df.iloc[29:35].to_string(index=False))

# ── Step 5: Multi-level groupby ───────────────────────────
print("\n📌 Multi-level Aggregation")

# Level 1: Region → Level 2: Product → Level 3: Quarter
ml = ts.groupby(["region","product","quarter"]).agg(
    total_units  =("units","sum"),
    total_revenue=("revenue","sum"),
    avg_price    =("price","mean"),
    num_days     =("date","nunique")
).round(1)

print("Multi-level (Region > Product > Quarter):")
print(ml.head(12).to_string())

# ── Step 6: Unstacking multi-level index ──────────────────
print("\n📌 Unstack multi-level index")

# Revenue by region and quarter
rq = ts.groupby(["region","quarter"])["revenue"].sum().unstack("quarter")
rq.columns = [f"Q{c}" for c in rq.columns]
rq["Total"] = rq.sum(axis=1)
print("\nRevenue by Region × Quarter:")
print(rq.to_string())

# ── Step 7: Year-over-Year (mock with 2 years of data) ────
print("\n📌 Year comparison: Weekday vs Weekend")

wkday_rev = ts.groupby("is_weekend")["revenue"].agg(["mean","sum"]).round(0)
wkday_rev.index = ["Weekday","Weekend"]
print(wkday_rev.to_string())

print("\nBest performing day of the week:")
dow = ts.groupby("day_name")["revenue"].mean().sort_values(ascending=False).round(0)
print(dow.to_string())

print("\n✅ Project 3 Complete!\n")