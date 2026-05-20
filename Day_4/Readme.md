# NumPy Fundamentals & Practice

This repository contains hands‑on examples of core NumPy concepts, from array creation to performance optimization.

## 📂 Contents

- `numpy_practice.py` – Step‑by‑step code covering all topics (or `.ipynb` notebook)
- `README.md` – This file

## 🚀 Topics Covered

- **Array creation:** `array`, `zeros`, `ones`, `arange`, `linspace`, `random`
- **Indexing & slicing:** 1D, 2D, negative indexing
- **Reshaping:** `reshape`, `ravel`, `flatten`
- **Broadcasting:** scalar, row/column vectors
- **Element‑wise operations:** arithmetic, comparison
- **Math functions:** `sin`, `exp`, `sqrt`, `log`
- **Statistics:** `mean`, `median`, `std`, `var`, `percentile`, `histogram`
- **Sorting & searching:** `sort`, `argsort`, `argmax`, `where`
- **Unique & counts:** `unique(return_counts=True)`
- **Boolean indexing:** masks, conditional selection, `np.where`
- **Fancy indexing:** integer array indexing
- **Performance & vectorization:** vectorized operations vs loops, benchmarking with `%timeit`
- **Memory:** views vs copies
- **Practice projects:** statistical analysis on simulated data, data transformation pipeline, large dataset operations

## ⚡ Key Patterns to Remember

| Pattern | Example |
|---------|---------|
| Create array | `np.arange(start, stop, step)` |
| Reshape | `arr.reshape(rows, -1)` |
| Conditional selection | `arr[arr > threshold]` |
| Replace values | `np.where(condition, true_val, false_val)` |
| Boolean indexing | `mask = (a > 2) & (a < 8)` |
| Vectorized math | `np.sin(arr)`, `arr + arr2`, `arr ** 2` |
| Statistics | `np.mean(arr)`, `np.median(arr)`, `np.percentile(arr, q)` |
| Unique elements | `np.unique(arr, return_counts=True)` |
| Handle NaN | `np.isnan(arr)`, `np.nanmean(arr)` |
| Performance | Always use NumPy built‑in functions; avoid Python loops |

## 💡 Performance Tip

NumPy’s vectorized operations (implemented in C) are **orders of magnitude faster** than Python loops. Use:

- `np.dot(a, b)` instead of loop‑based dot product
- `np.sum(arr)` instead of `sum(arr)`
- Broadcasting instead of manual loops

---

## 🛠️ How to Run

1. **Install NumPy** (if not already):
   ```bash
   pip install numpy

2. Run the code in VS Code using a Jupyter notebook (ipynb).

3. Benchmark your own code with %timeit in Jupyter.     