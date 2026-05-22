# EDA Project – Complete Exploratory Data Analysis

## Project Structure
```
eda_project/
├── data/
│   ├── ecommerce_data.csv          ← 5,000 order records (2 years)
│   ├── timeseries_data.csv         ← 3,650 daily store sales (5 stores)
│   └── customer_behavior_data.csv  ← 3,000 customer profiles
├── notebooks/
│   ├── 01_ecommerce_eda.py         ← Notebook 1: E-Commerce EDA
│   ├── 02_timeseries_eda.py        ← Notebook 2: Time Series EDA
│   └── 03_customer_behavior_eda.py ← Notebook 3: Customer Behavior EDA
├── scripts/
│   ├── generate_datasets.py        ← Generates all 3 synthetic datasets
│   ├── automated_profiling.py      ← ydata-profiling + custom profiler
│   └── pattern_identification.py  ← Cross-dataset pattern analysis
├── reports/                        ← All outputs saved here
│   ├── 01_ecommerce_dashboard.png
│   ├── 01_ecommerce_outliers.png
│   ├── 01_ecommerce_correlation.png
│   ├── 02_timeseries_dashboard.png
│   ├── 02_timeseries_correlation.png
│   ├── 03_customer_dashboard.png
│   ├── 03_customer_segment_deepdive.png
│   ├── patterns_summary.png
│   ├── pattern_identification_report.txt
│   ├── profile_ecommerce.txt
│   ├── profile_timeseries.txt
│   ├── profile_customer.txt
│   └── data_quality_summary.csv
└── README.md
```

---

## WHERE TO RUN THE CODE

### Option A – Terminal / Command Line (Recommended for beginners)
```bash
# 1. Navigate to the project folder
cd eda_project

# 2. Install dependencies (one time only)
pip install pandas numpy matplotlib seaborn scipy scikit-learn ydata-profiling plotly

# 3. Generate datasets
python scripts/generate_datasets.py

# 4. Run each EDA notebook
python notebooks/01_ecommerce_eda.py
python notebooks/02_timeseries_eda.py
python notebooks/03_customer_behavior_eda.py

# 5. Run profiling & pattern analysis
python scripts/automated_profiling.py
python scripts/pattern_identification.py
```

### Option B – Jupyter Notebook
```bash
pip install jupyter
jupyter notebook
# Then: File → New → Notebook, paste each .py script cell by cell
```

### Option C – Google Colab (Free, No Setup)
1. Go to https://colab.research.google.com
2. File → New Notebook
3. First cell: `!pip install pandas numpy matplotlib seaborn scipy ydata-profiling`
4. Upload the .py files OR paste the code into cells
5. Run each cell with Shift+Enter

### Option D – VS Code
1. Install VS Code + Python extension
2. Open the eda_project folder
3. Right-click any .py file → "Run Python File in Terminal"

---

## EDA CHECKLIST ✅

### Phase 1: Data Loading & Initial Understanding
- [ ] Load data and check shape (rows × columns)
- [ ] Inspect column names and data types
- [ ] Check memory usage
- [ ] Identify date range (for time-based data)
- [ ] Look at first/last 5 rows (head/tail)

### Phase 2: Data Quality Assessment
- [ ] Count missing values per column (and %)
- [ ] Identify duplicate rows
- [ ] Check for constant columns (zero variance)
- [ ] Verify date formats are parsed correctly
- [ ] Validate ID columns are unique
- [ ] Detect impossible/invalid values (e.g. negative price)

### Phase 3: Descriptive Statistics
- [ ] Mean, median, mode for all numeric columns
- [ ] Standard deviation and variance
- [ ] Min / Max values
- [ ] Quartiles (Q1, Q2, Q3) and IQR
- [ ] Percentiles (P10, P25, P50, P75, P90, P95, P99)
- [ ] Skewness (|skew| > 1 = significant skew)
- [ ] Kurtosis (> 3 = heavy tails)

### Phase 4: Univariate Analysis (one variable at a time)
- [ ] Histograms for all numerical columns
- [ ] Bar charts for all categorical columns
- [ ] Value counts for categorical variables
- [ ] Distribution shape (normal? skewed? bimodal?)

### Phase 5: Outlier Detection
- [ ] IQR method: flag values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- [ ] Z-score method: flag |z| > 3
- [ ] Boxplots for visual outlier inspection
- [ ] Decide: remove, cap, or keep outliers

### Phase 6: Bivariate / Multivariate Analysis
- [ ] Correlation matrix (Pearson for linear, Spearman for ranked)
- [ ] Scatter plots for key numeric pairs
- [ ] Group-by aggregations (mean/median by category)
- [ ] Pivot tables (row × column breakdowns)
- [ ] Heatmaps for categorical × numerical combinations

### Phase 7: Statistical Tests
- [ ] Normality test: Shapiro-Wilk (n < 5000) or D'Agostino-Pearson
- [ ] Compare groups: ANOVA (3+ groups) or T-test (2 groups)
- [ ] Categorical association: Chi-Square test
- [ ] Correlation significance: Pearson r with p-value

### Phase 8: Pattern Identification
- [ ] Time trends (upward/downward/flat)
- [ ] Seasonal patterns (monthly, quarterly, weekly)
- [ ] Day-of-week effects
- [ ] Anomaly detection (spikes, dips, outliers in time)
- [ ] Customer/product segments

### Phase 9: Handle Different Data Types
- [ ] **Numerical**: distributions, outliers, correlations
- [ ] **Categorical**: frequency tables, encoding check, rare categories
- [ ] **DateTime**: extract year/month/week/day, lag features
- [ ] **Text**: word counts, character counts, missing patterns
- [ ] **Mixed**: group-wise statistics per category

### Phase 10: Visualizations
- [ ] Distribution plots (histogram + KDE)
- [ ] Boxplots (outliers + IQR)
- [ ] Line charts (time trends)
- [ ] Bar charts (categorical comparisons)
- [ ] Heatmaps (correlations, pivot tables)
- [ ] Scatter plots (bivariate relationships)
- [ ] Pair plots (for small datasets, all numeric pairs)

---

## KEY FINDINGS SUMMARY

### Dataset 1: E-Commerce (5,000 orders)
| Finding | Value |
|---------|-------|
| Revenue is RIGHT-SKEWED | skew = +35.0 (heavy outliers) |
| Best revenue day | Friday (₹35,690 avg) |
| Top category | Electronics (₹92M total) |
| Missing data | customer_rating: 8%, delivery_days: 5% |
| Anomalies | 705 price outliers (IQR method) |
| Statistical test | Revenue differs sig. across categories (ANOVA p<0.001) |

### Dataset 2: Time Series (3,650 daily rows, 5 stores)
| Finding | Value |
|---------|-------|
| Trend | Significant upward trend (linear regression) |
| Seasonality | ~20% variation between peak and low months |
| Holiday effect | Holiday sales notably higher than weekday |
| Anomalies | ~15-30 per store (holiday spikes + operational dips) |
| Temperature | Weak correlation with sales |
| Missing data | ~1.4% across all columns |

### Dataset 3: Customer Behavior (3,000 customers)
| Finding | Value |
|---------|-------|
| Premium LTV | ~3× higher than Regular customers |
| Churn risk | At-Risk segment has highest churn probability |
| Top channel | Mobile App most preferred overall |
| LTV driver | Sessions/month positively correlated with LTV |
| Gender LTV | No statistically significant difference (T-test) |
| Missing data | ~1.4% in income, satisfaction score |

---

## STATISTICAL TESTS QUICK REFERENCE

| Test | Use Case | Python Code |
|------|----------|-------------|
| Shapiro-Wilk | Test if data is normally distributed | `scipy.stats.shapiro(data)` |
| One-Way ANOVA | Compare means of 3+ groups | `scipy.stats.f_oneway(g1, g2, g3)` |
| T-Test | Compare means of 2 groups | `scipy.stats.ttest_ind(a, b)` |
| Chi-Square | Association between 2 categorical vars | `scipy.stats.chi2_contingency(ct)` |
| Pearson r | Linear correlation between 2 numeric vars | `scipy.stats.pearsonr(x, y)` |
| Spearman r | Rank correlation (non-parametric) | `scipy.stats.spearmanr(x, y)` |

---

## INSTALLED LIBRARIES

```
pandas          – Data manipulation
numpy           – Numerical computing
matplotlib      – Base plotting
seaborn         – Statistical visualizations
scipy           – Statistical tests
scikit-learn    – ML utilities (preprocessing, clustering)
ydata-profiling – Automated EDA HTML reports
plotly          – Interactive charts
```
