"""
=============================================================
TASK 4: Performance Optimization
=============================================================
Topics: appropriate dtypes, category dtype, chunk processing,
        vectorization vs apply, query vs boolean indexing

WHERE TO RUN:
  - Terminal:  python 04_performance_optimization.py
  - Each section prints timing comparisons side by side
=============================================================
"""

import pandas as pd
import numpy as np
import time
import os
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("TASK 4: PERFORMANCE OPTIMIZATION")
print("=" * 60)


# ─────────────────────────────────────────────────────────────
# HELPER — simple timer context manager
# ─────────────────────────────────────────────────────────────
class Timer:
    def __init__(self, label=""):
        self.label = label
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *args):
        self.elapsed = (time.perf_counter() - self.start) * 1000
        print(f"  {self.label:<45} {self.elapsed:>8.2f} ms")


# ─────────────────────────────────────────────────────────────
# 1. APPROPRIATE DATA TYPES — memory & speed
# ─────────────────────────────────────────────────────────────
print("\n─── 1. Appropriate Data Types ───")

N = 500_000
np.random.seed(0)

df_default = pd.DataFrame({
    "user_id":   np.random.randint(1, 10000, N).astype(str),   # object by default
    "age":       np.random.randint(18, 80, N),                  # int64
    "score":     np.random.uniform(0, 100, N),                  # float64
    "active":    np.random.choice(["yes", "no"], N),            # object
    "region":    np.random.choice(["North","South","East","West"], N),
    "product":   np.random.choice(["A","B","C","D","E"], N),
    "amount":    np.random.uniform(100, 10000, N),
})

print(f"\n  Default dtypes memory: {df_default.memory_usage(deep=True).sum() / 1e6:.2f} MB")

# Optimise: downcast numbers, use category for low-cardinality strings, bool for flags
df_optimized = df_default.copy()
df_optimized["user_id"]  = df_optimized["user_id"].astype("string")   # StringDtype
df_optimized["age"]      = pd.to_numeric(df_optimized["age"], downcast="unsigned")   # uint8
df_optimized["score"]    = df_optimized["score"].astype("float32")
df_optimized["active"]   = df_optimized["active"].map({"yes": True, "no": False}).astype("bool")
df_optimized["region"]   = df_optimized["region"].astype("category")
df_optimized["product"]  = df_optimized["product"].astype("category")
df_optimized["amount"]   = df_optimized["amount"].astype("float32")

print(f"  Optimized dtypes memory:{df_optimized.memory_usage(deep=True).sum() / 1e6:.2f} MB")

print("\n  dtype comparison:")
comparison = pd.DataFrame({
    "Column":   df_default.columns,
    "Default":  [str(t) for t in df_default.dtypes],
    "Optimized":[str(t) for t in df_optimized.dtypes],
    "Orig_MB":  [df_default[c].memory_usage(deep=True)/1e6  for c in df_default.columns],
    "Opt_MB":   [df_optimized[c].memory_usage(deep=True)/1e6 for c in df_optimized.columns],
})
comparison["Savings_%"] = ((comparison["Orig_MB"] - comparison["Opt_MB"]) /
                            comparison["Orig_MB"] * 100).round(1)
print(comparison.to_string(index=False))

# ─────────────────────────────────────────────────────────────
# 2. CATEGORY DTYPE — speed benchmark
# ─────────────────────────────────────────────────────────────
print("\n─── 2. Category dtype — groupby speed ───")

df_str = df_default.copy()
df_cat = df_default.copy()
df_cat["region"]  = df_cat["region"].astype("category")
df_cat["product"] = df_cat["product"].astype("category")

with Timer("groupby on object (string) columns"):
    _ = df_str.groupby(["region", "product"])["amount"].mean()

with Timer("groupby on category columns"):
    _ = df_cat.groupby(["region", "product"])["amount"].mean()

with Timer("value_counts on object column"):
    _ = df_str["region"].value_counts()

with Timer("value_counts on category column"):
    _ = df_cat["region"].value_counts()

# ─────────────────────────────────────────────────────────────
# 3. VECTORIZATION vs apply() vs loop
# ─────────────────────────────────────────────────────────────
print("\n─── 3. Vectorization vs apply vs loop ───")

df_perf = pd.DataFrame({
    "a": np.random.uniform(1, 100, 200_000),
    "b": np.random.uniform(1, 100, 200_000),
})

# Python loop (DO NOT USE in production)
with Timer("Python for-loop  (200k rows)"):
    result_loop = []
    for i in range(len(df_perf)):
        result_loop.append(df_perf["a"].iloc[i] * 2 + df_perf["b"].iloc[i])

# apply (row-wise lambda)
with Timer("apply (row-wise lambda)"):
    result_apply = df_perf.apply(lambda row: row["a"] * 2 + row["b"], axis=1)

# apply (column-wise — faster)
with Timer("apply (column-wise)"):
    result_col_apply = df_perf["a"].apply(lambda x: x * 2) + df_perf["b"]

# numpy vectorized operation
with Timer("Vectorized (pandas/numpy op)"):
    result_vec = df_perf["a"] * 2 + df_perf["b"]

print("\n  Rule: Loop → apply (row) → apply (col) → vectorized  [slowest → fastest]")

# ─────────────────────────────────────────────────────────────
# 4. QUERY vs BOOLEAN INDEXING
# ─────────────────────────────────────────────────────────────
print("\n─── 4. .query() vs boolean indexing ───")

df_q = df_default[["age", "score", "amount", "region"]].copy()
df_q["age"]    = df_q["age"].astype(int)
df_q["score"]  = df_q["score"].astype(float)
df_q["amount"] = df_q["amount"].astype(float)

# Boolean indexing
with Timer("Boolean indexing (3 conditions)"):
    r1 = df_q[(df_q["age"] > 30) & (df_q["score"] > 50) & (df_q["amount"] < 5000)]

# .query()
with Timer(".query() (3 conditions)"):
    r2 = df_q.query("age > 30 and score > 50 and amount < 5000")

print(f"\n  Both return same rows: {len(r1)} rows  (match: {r1.equals(r2)})")

# ─────────────────────────────────────────────────────────────
# 5. CHUNK PROCESSING — large CSV files
# ─────────────────────────────────────────────────────────────
print("\n─── 5. Chunk Processing for Large Files ───")

# Create a synthetic large CSV (5M rows, ~200 MB)
large_csv = OUTPUT_DIR / "large_data.csv"
print("  Generating 1M-row CSV...")

chunk_size_gen = 100_000
rows_total = 1_000_000

with open(large_csv, "w") as f:
    f.write("id,region,product,amount,qty\n")
    written = 0
    while written < rows_total:
        n = min(chunk_size_gen, rows_total - written)
        ids      = np.arange(written + 1, written + n + 1)
        regions  = np.random.choice(["North","South","East","West"], n)
        products = np.random.choice(["A","B","C","D","E"], n)
        amounts  = np.random.uniform(100, 10000, n).round(2)
        qty      = np.random.randint(1, 20, n)
        chunk_df = pd.DataFrame({
            "id":      ids,
            "region":  regions,
            "product": products,
            "amount":  amounts,
            "qty":     qty,
        })
        chunk_df.to_csv(f, index=False, header=False)
        written += n

file_mb = os.path.getsize(large_csv) / 1e6
print(f"  Created: {large_csv.name}  ({file_mb:.1f} MB)")

# ── Method A: read all at once ──────────────────────────────
with Timer("read_csv — entire file at once"):
    df_full = pd.read_csv(large_csv)
    total_full = df_full.groupby("region")["amount"].sum()
del df_full

# ── Method B: chunk processing ──────────────────────────────
with Timer("read_csv — chunk processing (100k/chunk)"):
    results = []
    for chunk in pd.read_csv(large_csv, chunksize=100_000,
                              dtype={"region": "category", "product": "category",
                                     "amount": "float32", "qty": "int16"}):
        # Process each chunk: compute partial sum
        partial = chunk.groupby("region")["amount"].sum()
        results.append(partial)
    total_chunks = pd.concat(results).groupby(level=0).sum()

print(f"\n  Totals match: {total_full.round(0).equals(total_chunks.round(0))}")
print(f"\n  Regional revenue:\n{total_chunks.round(2)}")

# ── Memory-efficient dtype in read_csv ──────────────────────
print("\n─── 5b. dtype spec in read_csv ───")
with Timer("read_csv — default dtypes"):
    df_def = pd.read_csv(large_csv)
    mb_def = df_def.memory_usage(deep=True).sum() / 1e6

with Timer("read_csv — optimized dtypes"):
    df_opt = pd.read_csv(large_csv, dtype={
        "id":      "int32",
        "region":  "category",
        "product": "category",
        "amount":  "float32",
        "qty":     "int16",
    })
    mb_opt = df_opt.memory_usage(deep=True).sum() / 1e6

print(f"\n  Default dtypes:   {mb_def:.1f} MB")
print(f"  Optimized dtypes: {mb_opt:.1f} MB  ({(1 - mb_opt/mb_def)*100:.0f}% savings)")

del df_def, df_opt

# ─────────────────────────────────────────────────────────────
# 6. VECTORIZED STRING OPERATIONS vs apply
# ─────────────────────────────────────────────────────────────
print("\n─── 6. Vectorized String Operations ───")

str_series = pd.Series(["hello world"] * 100_000)

with Timer("apply + str.title()  (100k items)"):
    _ = str_series.apply(lambda x: x.title())

with Timer(".str.title() vectorized (100k items)"):
    _ = str_series.str.title()

# ─────────────────────────────────────────────────────────────
# 7. np.where / np.select vs apply for conditionals
# ─────────────────────────────────────────────────────────────
print("\n─── 7. Conditional Columns — np.where vs apply ───")

scores = pd.Series(np.random.randint(0, 100, 500_000))

with Timer("apply for grade assignment (500k)"):
    _ = scores.apply(lambda x:
        "A" if x >= 90 else
        "B" if x >= 75 else
        "C" if x >= 60 else
        "D" if x >= 45 else "F"
    )

with Timer("np.select for grade assignment (500k)"):
    conditions = [scores >= 90, scores >= 75, scores >= 60, scores >= 45]
    choices    = ["A", "B", "C", "D"]
    _ = np.select(conditions, choices, default="F")

# ─────────────────────────────────────────────────────────────
# 8. SUMMARY TABLE
# ─────────────────────────────────────────────────────────────
print("""
─── 8. Optimization Cheat-Sheet ───

  TECHNIQUE                  WHEN TO USE
  ─────────────────────────────────────────────────────────
  category dtype             String col with < 50% unique values
  int8/int16/float32         Numeric col where range is known
  bool instead of yes/no     Binary flags
  Vectorized ops (*, +, /)   Any arithmetic — fastest always
  .str.*  methods            String manipulation (not apply)
  np.where / np.select       Simple conditional columns
  .query()                   Readable filtering (slightly faster)
  chunksize in read_csv      Files > available RAM
  dtype= in read_csv         Parse correctly + save memory
  .groupby on category       Faster than groupby on string
  ─────────────────────────────────────────────────────────
""")

print("✅  Task 4 complete — all performance optimizations demonstrated.")