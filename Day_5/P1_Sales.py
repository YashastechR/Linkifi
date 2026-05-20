# ============================================================
# PROJECT 1: Clean Messy Sales Dataset
# Run: python project1_sales_cleaning.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 55)
print("  PROJECT 1: Clean Messy Sales Dataset")
print("=" * 55)

# ── Step 1: Create the messy dataset ─────────────────────
np.random.seed(42)
raw = pd.DataFrame({
    "order_id":   [f"ORD{i:03}" for i in range(1, 21)],
    "customer":   ["Alice","BOB","charlie",None,"DIANA","eve","Frank",
                   "bob","Alice","Grace","Hank",None,"Ivy","Jack",
                   "ALICE","bob","Charlie","diana","Eve","Frank"],
    "product":    ["Laptop","Phone","Tablet","Laptop",None,"Phone","Laptop",
                   "Tablet","Phone","Laptop","Phone","Tablet","Laptop","Phone",
                   "Tablet","Laptop","Phone","Tablet","Laptop","Phone"],
    "quantity":   [2,1,3,None,1,2,1,3,None,2,1,3,2,1,3,None,2,1,3,2],
    "unit_price": [75000,15000,25000,75000,15000,None,75000,25000,15000,
                   75000,15000,25000,75000,None,25000,75000,15000,25000,75000,15000],
    "date":       ["2024-01-05","2024-01-07","2024-01-07","2024-02-10","2024-02-11",
                   "2024-02-15","2024-03-01","2024-03-05","2024-03-10","2024-04-01",
                   "2024-04-05","2024-04-10","2024-05-01","2024-05-05","2024-05-10",
                   "invalid","2024-06-05","2024-06-10","2024-07-01","2024-07-05"],
    "region":     ["North","South","North","East","West","South","North","East",
                   "West","North","South","East","West","North","South",
                   "East","West","North","South","East"],
    "discount":   [0.1,0.0,0.15,0.0,0.05,0.1,None,0.0,0.2,0.1,
                   0.05,0.0,0.15,0.1,0.0,0.05,0.2,None,0.1,0.0]
})

print("Raw data shape:", raw.shape)
print("\nMissing values:\n", raw.isnull().sum())

# ── Step 2: Clean ─────────────────────────────────────────
print("\n📌 Cleaning...")
df = raw.copy()

# Fix customer names
df["customer"] = df["customer"].str.strip().str.title()
df["customer"] = df["customer"].fillna("Unknown")

# Fix numeric types & fill missing
df["quantity"]   = pd.to_numeric(df["quantity"],   errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"],  errors="coerce")
df["discount"]   = pd.to_numeric(df["discount"],    errors="coerce")

df["quantity"]   = df["quantity"].fillna(df.groupby("product")["quantity"].transform("median"))
df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))
df["discount"]   = df["discount"].fillna(0.0)

# Drop rows with missing product
df = df.dropna(subset=["product"])

# Fix invalid dates (drop them)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# ── Step 3: Derive columns ───────────────────────────────
df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
df["month"]   = df["date"].dt.to_period("M").astype(str)
df["quarter"] = df["date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})

print("Clean data shape:", df.shape)
print("\nSample clean rows:")
print(df.head(5).to_string(index=False))

# ── Step 4: Analysis ─────────────────────────────────────
print("\n📌 Analysis")

print("\nRevenue by product:")
print(df.groupby("product")["revenue"].sum().sort_values(ascending=False).to_string())

print("\nRevenue by region:")
print(df.groupby("region")["revenue"].sum().sort_values(ascending=False).to_string())

print("\nRevenue by quarter:")
print(df.groupby("quarter")["revenue"].sum().to_string())

print("\nTop 3 customers by revenue:")
print(df.groupby("customer")["revenue"].sum()
        .sort_values(ascending=False).head(3).to_string())

# ── Step 5: Save clean data ───────────────────────────────
import os; SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_files"); os.makedirs(SAVE_DIR, exist_ok=True); OUT_PATH = os.path.join(SAVE_DIR, "clean_sales.csv"); df.to_csv(OUT_PATH, index=False)
print(f"\n✅ Clean data saved to: {OUT_PATH}")
print("✅ Project 1 Complete!\n")