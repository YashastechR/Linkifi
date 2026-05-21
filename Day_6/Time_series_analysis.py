"""
=============================================================
TASK 2: Time Series Operations
=============================================================
Topics: DatetimeIndex, resampling (D/W/M/Y), rolling windows,
        shift/lag, date ranges, timezone handling

WHERE TO RUN:
  - Terminal:  python 02_time_series_analysis.py
  - Jupyter:   jupyter notebook  → paste sections into cells
=============================================================
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("TASK 2: TIME SERIES ANALYSIS")
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# 1. CREATING A DATETIME INDEX
# ─────────────────────────────────────────────────────────────
print("\n─── 1. Creating DatetimeIndex ───")

# Daily date range for 2024
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
print(f"Total days: {len(dates)}")
print(f"First 5: {dates[:5].tolist()}")

# Simulate daily sales data
np.random.seed(42)
sales = pd.Series(
    np.random.randint(500, 2000, size=len(dates)) +
    np.sin(np.arange(len(dates)) * 2 * np.pi / 30) * 200,   # monthly seasonality
    index=dates,
    name="sales"
)
print("\nSales (first 10 days):")
print(sales.head(10))

# ─────────────────────────────────────────────────────────────
# 2. PARSING DATES FROM A DataFrame
# ─────────────────────────────────────────────────────────────
print("\n─── 2. Parsing Dates from DataFrame ───")

raw_data = pd.DataFrame({
    "date":   ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05"],
    "amount": [1200, 3400, 2100, 4500],
    "region": ["North", "South", "East", "West"],
})

raw_data["date"] = pd.to_datetime(raw_data["date"])
raw_data = raw_data.set_index("date")
print(raw_data)
print(f"\ndtypes:\n{raw_data.dtypes}")

# ─────────────────────────────────────────────────────────────
# 3. DATE COMPONENTS — extracting parts of a date
# ─────────────────────────────────────────────────────────────
print("\n─── 3. Extracting Date Components ───")

ts_df = pd.DataFrame({"sales": sales})
ts_df["year"]       = ts_df.index.year
ts_df["month"]      = ts_df.index.month
ts_df["month_name"] = ts_df.index.month_name()
ts_df["day"]        = ts_df.index.day
ts_df["weekday"]    = ts_df.index.day_name()
ts_df["week_num"]   = ts_df.index.isocalendar().week.values
ts_df["quarter"]    = ts_df.index.quarter

print(ts_df.head(7))

# ─────────────────────────────────────────────────────────────
# 4. DATE RANGES — different frequencies
# ─────────────────────────────────────────────────────────────
print("\n─── 4. Date Ranges with Different Frequencies ───")

freqs = {
    "Business days (B)":   pd.date_range("2024-01-01", periods=5, freq="B"),
    "Weekly (W-MON)":      pd.date_range("2024-01-01", periods=5, freq="W-MON"),
    "Month-end (M)":      pd.date_range("2024-01-01", periods=6, freq="M"),
    "Quarter-end (Q)":    pd.date_range("2024-01-01", periods=4, freq="Q"),
    "Hourly (h)":          pd.date_range("2024-01-01", periods=5, freq="h"),
}
for label, dr in freqs.items():
    print(f"\n{label}:\n  {dr.tolist()}")

# ─────────────────────────────────────────────────────────────
# 5. SLICING & INDEXING TIME SERIES
# ─────────────────────────────────────────────────────────────
print("\n─── 5. Slicing Time Series ───")

# By year
print("January 2024 sales:")
print(sales["2024-01"].describe())

# By range
print("\nMarch 1–7 sales:")
print(sales["2024-03-01":"2024-03-07"].to_frame())

# ─────────────────────────────────────────────────────────────
# 6. RESAMPLING — aggregate to coarser frequency
# ─────────────────────────────────────────────────────────────
print("\n─── 6. Resampling ───")

# Weekly totals
weekly = sales.resample("W").sum()
print("Weekly totals (first 5):")
print(weekly.head())

# Monthly stats
monthly = sales.resample("M").agg(
    total=("sum"),
    average=("mean"),
    min_sales=("min"),
    max_sales=("max"),
)
# Fix: use named agg properly
monthly = sales.resample("M").agg(
    total   = "sum",
    average = "mean",
    minimum = "min",
    maximum = "max",
)
print("\nMonthly stats:")
print(monthly)

# Quarterly total
quarterly = sales.resample("Q").sum()
print("\nQuarterly totals:")
print(quarterly)

# Yearly total
yearly = sales.resample("Y").sum()
print("\nYearly total:")
print(yearly)

# ─────────────────────────────────────────────────────────────
# 7. ROLLING WINDOWS — moving statistics
# ─────────────────────────────────────────────────────────────
print("\n─── 7. Rolling Windows ───")

roll_df = pd.DataFrame({"sales": sales})

roll_df["MA_7"]  = sales.rolling(window=7).mean()    # 7-day moving average
roll_df["MA_30"] = sales.rolling(window=30).mean()   # 30-day moving average
roll_df["STD_7"] = sales.rolling(window=7).std()     # 7-day rolling std
roll_df["MAX_7"] = sales.rolling(window=7).max()     # 7-day rolling max

print("Rolling stats (rows 30–37):")
print(roll_df.iloc[30:37].round(1))

# Expanding window — cumulative stats
roll_df["cum_mean"] = sales.expanding().mean()
roll_df["cum_max"]  = sales.expanding().max()
print("\nExpanding (cumulative) stats (rows 0–5):")
print(roll_df[["sales", "cum_mean", "cum_max"]].head(6).round(1))

# ─────────────────────────────────────────────────────────────
# 8. SHIFT and LAG — compare current vs past values
# ─────────────────────────────────────────────────────────────
print("\n─── 8. Shift / Lag Operations ───")

shift_df = pd.DataFrame({"sales": sales.head(15)})

shift_df["lag_1"]       = shift_df["sales"].shift(1)     # yesterday's sales
shift_df["lag_7"]       = shift_df["sales"].shift(7)     # same day last week
shift_df["lead_1"]      = shift_df["sales"].shift(-1)    # tomorrow's sales
shift_df["pct_change"]  = shift_df["sales"].pct_change() * 100   # % day-over-day change
shift_df["diff"]        = shift_df["sales"].diff()               # absolute change

print(shift_df.round(1))

# ─────────────────────────────────────────────────────────────
# 9. TIMEZONE HANDLING
# ─────────────────────────────────────────────────────────────
print("\n─── 9. Timezone Handling ───")

# Create timezone-naive series, then localize
ts_naive = pd.Timestamp("2024-06-15 10:30:00")
print(f"Naive:               {ts_naive}")

ts_ist = ts_naive.tz_localize("Asia/Kolkata")
print(f"IST (localized):     {ts_ist}")

ts_utc = ts_ist.tz_convert("UTC")
print(f"UTC (converted):     {ts_utc}")

ts_ny  = ts_ist.tz_convert("America/New_York")
print(f"New York (converted):{ts_ny}")

# Applying to a Series
tz_series = pd.Series(
    [100, 200, 300],
    index=pd.date_range("2024-01-01", periods=3, freq="h", tz="Asia/Kolkata")
)
print("\nIST Series:")
print(tz_series)
print("\nSame series in UTC:")
print(tz_series.tz_convert("UTC"))

# ─────────────────────────────────────────────────────────────
# 10. PRACTICAL EXAMPLE — full time series pipeline
# ─────────────────────────────────────────────────────────────
print("\n─── 10. Full Time Series Pipeline ───")

np.random.seed(0)
dates2 = pd.date_range("2023-01-01", "2024-12-31", freq="D")
revenue = pd.Series(
    1000 + np.cumsum(np.random.randn(len(dates2)) * 50) +
    np.sin(np.arange(len(dates2)) * 2 * np.pi / 365) * 200,
    index=dates2, name="revenue"
)

result = pd.DataFrame({
    "revenue":    revenue,
    "MA_30":      revenue.rolling(30).mean(),
    "pct_change": revenue.pct_change() * 100,
    "yoy_growth": revenue.pct_change(365) * 100,
})

monthly_summary = result["revenue"].resample("M").agg(["sum", "mean", "std"]).round(2)
monthly_summary.index = monthly_summary.index.strftime("%b-%Y")
print("\nMonthly Revenue Summary:")
print(monthly_summary)

print("\n✅  Task 2 complete — all time series operations demonstrated.")