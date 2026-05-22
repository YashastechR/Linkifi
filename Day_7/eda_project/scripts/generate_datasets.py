"""
Dataset Generator for EDA Practice
Generates: E-commerce, Time Series, and Customer Behavior datasets
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ─────────────────────────────────────────
# 1. E-COMMERCE DATASET
# ─────────────────────────────────────────
def generate_ecommerce(n=5000):
    categories   = ["Electronics","Clothing","Books","Home & Garden","Sports","Beauty","Toys"]
    regions      = ["North","South","East","West","Central"]
    payment_methods = ["Credit Card","Debit Card","PayPal","UPI","Net Banking"]
    status       = ["Completed","Pending","Cancelled","Returned"]

    start = datetime(2022, 1, 1)
    dates = [start + timedelta(days=int(x)) for x in np.random.uniform(0, 730, n)]

    base_prices  = {"Electronics":15000,"Clothing":1500,"Books":500,
                    "Home & Garden":3000,"Sports":2500,"Beauty":800,"Toys":1000}
    category_arr = np.random.choice(categories, n)
    prices       = np.array([base_prices[c] * np.random.uniform(0.5, 2.5) for c in category_arr])

    # inject anomalies
    anomaly_idx  = np.random.choice(n, 50, replace=False)
    prices[anomaly_idx] *= np.random.uniform(5, 10, 50)

    qty = np.random.randint(1, 10, n)
    qty[np.random.choice(n, 20, replace=False)] = np.random.randint(50, 200, 20)

    df = pd.DataFrame({
        "order_id":        [f"ORD{str(i).zfill(6)}" for i in range(1, n+1)],
        "date":            dates,
        "category":        category_arr,
        "product_id":      [f"PROD{np.random.randint(1,500):04d}" for _ in range(n)],
        "price":           prices.round(2),
        "quantity":        qty,
        "discount_pct":    np.round(np.random.choice([0,5,10,15,20,25,30], n,
                                    p=[0.4,0.15,0.15,0.1,0.1,0.05,0.05]), 2),
        "region":          np.random.choice(regions, n),
        "payment_method":  np.random.choice(payment_methods, n),
        "order_status":    np.random.choice(status, n, p=[0.7,0.1,0.1,0.1]),
        "customer_rating": np.random.choice([1,2,3,4,5], n, p=[0.05,0.1,0.2,0.35,0.3]),
        "delivery_days":   np.random.randint(1, 15, n),
    })
    df["revenue"] = (df["price"] * df["quantity"] * (1 - df["discount_pct"]/100)).round(2)

    # introduce missing values
    for col, rate in [("customer_rating", 0.08), ("delivery_days", 0.05), ("discount_pct", 0.03)]:
        df.loc[df.sample(frac=rate).index, col] = np.nan

    path = os.path.join(DATA_DIR, "ecommerce_data.csv")
    df.to_csv(path, index=False)
    print(f"✓ E-commerce dataset saved → {path}  ({len(df)} rows)")
    return df


# ─────────────────────────────────────────
# 2. TIME SERIES DATASET (daily store sales)
# ─────────────────────────────────────────
def generate_timeseries(days=730):
    dates   = pd.date_range("2022-01-01", periods=days, freq="D")
    stores  = ["Store_A","Store_B","Store_C","Store_D","Store_E"]
    rows    = []

    for store in stores:
        base      = np.random.uniform(50_000, 200_000)
        trend     = np.linspace(0, base * 0.3, days)
        seasonal  = base * 0.2 * np.sin(2*np.pi*np.arange(days)/365)
        weekly    = base * 0.1 * np.sin(2*np.pi*np.arange(days)/7)
        noise     = np.random.normal(0, base*0.05, days)
        sales     = base + trend + seasonal + weekly + noise

        # holiday spikes
        for idx in np.random.choice(days, 20, replace=False):
            sales[idx] *= np.random.uniform(1.5, 3.0)

        # anomalous dips
        for idx in np.random.choice(days, 10, replace=False):
            sales[idx] *= np.random.uniform(0.1, 0.4)

        # missing values
        missing_idx = np.random.choice(days, int(days*0.03), replace=False)

        for i, d in enumerate(dates):
            rows.append({
                "date":         d,
                "store":        store,
                "sales":        None if i in missing_idx else round(max(0, sales[i]), 2),
                "transactions": None if i in missing_idx else int(sales[i] / np.random.uniform(200,500)),
                "avg_basket":   None if i in missing_idx else round(np.random.uniform(300, 1500), 2),
                "foot_traffic": None if i in missing_idx else int(np.random.uniform(100, 2000)),
                "temperature":  round(20 + 15*np.sin(2*np.pi*i/365) + np.random.normal(0,3), 1),
                "is_holiday":   int(d.dayofweek >= 5 or i in np.random.choice(days,15,replace=False)),
            })

    df = pd.DataFrame(rows)
    path = os.path.join(DATA_DIR, "timeseries_data.csv")
    df.to_csv(path, index=False)
    print(f"✓ Time-series dataset saved → {path}  ({len(df)} rows)")
    return df


# ─────────────────────────────────────────
# 3. CUSTOMER BEHAVIOR DATASET
# ─────────────────────────────────────────
def generate_customer_behavior(n=3000):
    segments    = ["Premium","Regular","Occasional","New","At-Risk"]
    channels    = ["Mobile App","Website","In-Store","Social Media","Email"]
    cities      = ["Mumbai","Delhi","Bangalore","Chennai","Hyderabad","Pune","Kolkata"]

    reg_start = datetime(2019, 1, 1)
    registration_dates = [reg_start + timedelta(days=int(x)) for x in np.random.uniform(0, 1825, n)]

    ages       = np.random.normal(35, 12, n).clip(18, 75).astype(int)
    incomes    = np.random.lognormal(11, 0.6, n).round(-3)
    seg_arr    = np.random.choice(segments, n, p=[0.15,0.35,0.25,0.15,0.10])

    base_spend = {"Premium":50000,"Regular":15000,"Occasional":5000,"New":8000,"At-Risk":3000}
    ltv        = np.array([base_spend[s]*np.random.uniform(0.5,2.0) for s in seg_arr])

    sessions   = np.random.poisson(15, n)
    sessions   = np.where(seg_arr=="Premium", sessions*3,
                 np.where(seg_arr=="At-Risk", sessions//3, sessions))

    df = pd.DataFrame({
        "customer_id":      [f"CUST{str(i).zfill(6)}" for i in range(1, n+1)],
        "registration_date": registration_dates,
        "age":              ages,
        "gender":           np.random.choice(["Male","Female","Other"], n, p=[0.48,0.49,0.03]),
        "city":             np.random.choice(cities, n),
        "annual_income":    incomes.clip(100000, 5000000),
        "segment":          seg_arr,
        "lifetime_value":   ltv.round(2),
        "total_orders":     np.random.poisson(8, n) + (seg_arr=="Premium").astype(int)*10,
        "avg_order_value":  (ltv / (np.random.poisson(8, n)+1)).round(2),
        "preferred_channel":np.random.choice(channels, n),
        "sessions_per_month": sessions,
        "churn_probability": np.random.beta(2, 5, n).round(4),
        "satisfaction_score": np.random.choice([1,2,3,4,5,None], n,
                               p=[0.05,0.08,0.15,0.35,0.32,0.05]),
        "days_since_last_purchase": np.where(seg_arr=="At-Risk",
                                    np.random.randint(60,365,n),
                                    np.random.randint(1,60,n)),
    })

    # missing values
    for col, rate in [("annual_income",0.07),("satisfaction_score",0.06),("age",0.04)]:
        df.loc[df.sample(frac=rate).index, col] = np.nan

    path = os.path.join(DATA_DIR, "customer_behavior_data.csv")
    df.to_csv(path, index=False)
    print(f"✓ Customer behavior dataset saved → {path}  ({len(df)} rows)")
    return df


if __name__ == "__main__":
    print("Generating datasets …\n")
    generate_ecommerce()
    generate_timeseries()
    generate_customer_behavior()
    print("\nAll datasets ready.")
