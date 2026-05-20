# ============================================================
# PROJECT 2: Customer Analytics
# Run: python project2_customer_analytics.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 55)
print("  PROJECT 2: Customer Analytics")
print("=" * 55)

np.random.seed(7)
n = 200

# ── Step 1: Build datasets ────────────────────────────────
customers = pd.DataFrame({
    "customer_id": range(1, 51),
    "name":        [f"Customer_{i}" for i in range(1, 51)],
    "age":         np.random.randint(22, 65, 50),
    "city":        np.random.choice(["Delhi","Mumbai","Bangalore","Chennai","Pune"], 50),
    "segment":     np.random.choice(["Premium","Standard","Basic"], 50,
                                    p=[0.2, 0.5, 0.3])
})

orders = pd.DataFrame({
    "order_id":    range(1, n + 1),
    "customer_id": np.random.randint(1, 51, n),
    "product":     np.random.choice(["Laptop","Phone","Tablet","Accessories"], n),
    "amount":      np.random.randint(500, 100000, n),
    "order_date":  pd.date_range("2024-01-01", periods=n, freq="2D")
})

print("Customers:", customers.shape, "| Orders:", orders.shape)

# ── Step 2: Merge ──────────────────────────────────────────
df = orders.merge(customers, on="customer_id", how="left")
df["month"] = df["order_date"].dt.month
df["year"]  = df["order_date"].dt.year

# ── Step 3: Customer Metrics (RFM-style) ──────────────────
print("\n📌 Customer Summary Metrics")

last_date = df["order_date"].max()
customer_metrics = df.groupby("customer_id").agg(
    order_count    =("order_id",    "count"),
    total_spent    =("amount",      "sum"),
    avg_order_value=("amount",      "mean"),
    last_order_date=("order_date",  "max")
).reset_index()

customer_metrics["days_since_last"] = (last_date - customer_metrics["last_order_date"]).dt.days
customer_metrics["avg_order_value"] = customer_metrics["avg_order_value"].round(0)

# Segment customers by spend
customer_metrics["spend_tier"] = pd.cut(
    customer_metrics["total_spent"],
    bins=[0, 50000, 150000, 500000, float("inf")],
    labels=["Low","Medium","High","Premium"]
)

print(customer_metrics.sort_values("total_spent", ascending=False).head(8).to_string(index=False))

# ── Step 4: Cohort (which segment buys what) ──────────────
print("\n📌 Segment × Product Analysis")

seg_df = df.merge(customer_metrics[["customer_id","spend_tier"]], on="customer_id")
pivot = pd.crosstab(seg_df["spend_tier"], seg_df["product"],
                    values=seg_df["amount"], aggfunc="sum")
print(pivot.fillna(0).astype(int).to_string())

# ── Step 5: Monthly Revenue per Segment ───────────────────
print("\n📌 Monthly Revenue by Customer Segment")

monthly_seg = (df
    .groupby(["month", "segment"])["amount"]
    .sum()
    .unstack("segment")
    .fillna(0)
    .astype(int))

print(monthly_seg.head(6).to_string())

# ── Step 6: City Performance ──────────────────────────────
print("\n📌 City Performance")

city_stats = df.groupby("city").agg(
    orders        =("order_id","count"),
    customers     =("customer_id","nunique"),
    total_revenue =("amount","sum"),
    avg_per_order =("amount","mean")
).sort_values("total_revenue", ascending=False)

city_stats["avg_per_order"] = city_stats["avg_per_order"].round(0)
print(city_stats.to_string())

print("\n✅ Project 2 Complete!\n")