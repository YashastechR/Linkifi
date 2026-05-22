"""
╔══════════════════════════════════════════════════════════╗
║  AUTOMATED DATA PROFILING (ydata-profiling)             ║
╚══════════════════════════════════════════════════════════╝
Run: python scripts/automated_profiling.py
Generates HTML profiling reports for all 3 datasets.
"""
import pandas as pd
import os, time

try:
    from ydata_profiling import ProfileReport
    HAS_PROFILING = True
except ImportError:
    HAS_PROFILING = False
    print("⚠  ydata-profiling not available – using custom profiler instead")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE,"reports")
os.makedirs(OUT,exist_ok=True)

datasets = {
    "ecommerce": {
        "file":  "ecommerce_data.csv",
        "parse": ["date"],
        "title": "E-Commerce Dataset Profile"
    },
    "timeseries": {
        "file":  "timeseries_data.csv",
        "parse": ["date"],
        "title": "Time Series Dataset Profile"
    },
    "customer": {
        "file":  "customer_behavior_data.csv",
        "parse": ["registration_date"],
        "title": "Customer Behavior Dataset Profile"
    }
}

# ── CUSTOM PROFILER (works without ydata-profiling) ───────
def custom_profile(df, name):
    lines = []
    lines.append(f"{'='*70}")
    lines.append(f"  DATA PROFILE: {name.upper()}")
    lines.append(f"{'='*70}")
    lines.append(f"\n  Rows          : {df.shape[0]:,}")
    lines.append(f"  Columns       : {df.shape[1]}")
    lines.append(f"  Total cells   : {df.shape[0]*df.shape[1]:,}")
    lines.append(f"  Duplicate rows: {df.duplicated().sum()}")
    lines.append(f"  Memory        : {df.memory_usage(deep=True).sum()/1024:.1f} KB\n")

    total_missing = df.isnull().sum().sum()
    missing_pct   = total_missing/(df.shape[0]*df.shape[1])*100
    lines.append(f"  Total missing : {total_missing} ({missing_pct:.2f}%)\n")

    lines.append("  COLUMN-LEVEL ANALYSIS")
    lines.append("  " + "-"*66)
    for col in df.columns:
        s = df[col]
        dtype = str(s.dtype)
        miss  = s.isnull().sum()
        uniq  = s.nunique()
        lines.append(f"\n  [{col}]  dtype={dtype}  missing={miss}({miss/len(df)*100:.1f}%)  unique={uniq}")

        if pd.api.types.is_numeric_dtype(s) and not s.dropna().empty:
            mn,mx = s.min(),s.max()
            mu,med= s.mean(),s.median()
            sd    = s.std()
            sk    = s.skew()
            ku    = s.kurtosis()
            q1,q3 = s.quantile(0.25), s.quantile(0.75)
            lines.append(f"    min={mn:.3g}  max={mx:.3g}  mean={mu:.3g}  median={med:.3g}")
            lines.append(f"    std={sd:.3g}  IQR={q3-q1:.3g}  skew={sk:.3f}  kurt={ku:.3f}")
            lines.append(f"    Q1={q1:.3g}  Q3={q3:.3g}")
        elif pd.api.types.is_object_dtype(s) or str(dtype)=="category":
            vc = s.value_counts()
            top5 = vc.head(5)
            lines.append(f"    Top 5: {dict(top5)}")
        elif "datetime" in dtype:
            lines.append(f"    Range: {s.min()} → {s.max()}")

    report_text = "\n".join(lines)
    path = os.path.join(OUT, f"profile_{name}.txt")
    with open(path,"w", encoding='utf-8') as fh:
        fh.write(report_text)
    print(f"  ✓ Text profile → {path}")
    return report_text

# ── DATA QUALITY METRICS ──────────────────────────────────
def data_quality_report(df, name):
    report = {}
    report["dataset"]          = name
    report["rows"]             = df.shape[0]
    report["columns"]          = df.shape[1]
    report["duplicates"]       = int(df.duplicated().sum())
    report["total_missing"]    = int(df.isnull().sum().sum())
    report["missing_pct"]      = round(df.isnull().sum().sum()/(df.shape[0]*df.shape[1])*100,2)
    report["num_numeric_cols"] = int(df.select_dtypes(include="number").shape[1])
    report["num_cat_cols"]     = int(df.select_dtypes(include="object").shape[1])
    report["num_datetime_cols"]= int(df.select_dtypes(include="datetime").shape[1])

    # Check for constant cols
    report["constant_cols"] = [c for c in df.columns if df[c].nunique()<=1]

    # Outlier count (IQR) for numeric
    outlier_info = {}
    for col in df.select_dtypes(include="number").columns:
        s = df[col].dropna()
        if len(s)>0:
            q1,q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3-q1
            cnt = int(((s<q1-1.5*iqr)|(s>q3+1.5*iqr)).sum())
            if cnt > 0:
                outlier_info[col] = cnt
    report["outlier_counts"] = outlier_info
    return report

print("Starting automated profiling …\n")
all_quality = []

for key, cfg in datasets.items():
    print(f"─── Processing: {cfg['title']} ───")
    df = pd.read_csv(os.path.join(BASE,"data",cfg["file"]), parse_dates=cfg["parse"])

    # Custom profile (always)
    custom_profile(df, key)

    # Data quality metrics
    qr = data_quality_report(df, key)
    all_quality.append(qr)
    print(f"  Quality → rows={qr['rows']}, missing={qr['missing_pct']}%, duplicates={qr['duplicates']}")

    # ydata-profiling HTML report (if available)
    if HAS_PROFILING:
        try:
            print(f"  Generating ydata HTML report (this takes ~60 s) …")
            profile = ProfileReport(df, title=cfg["title"], minimal=True,
                                    progress_bar=False)
            html_path = os.path.join(OUT,f"profile_{key}.html")
            profile.to_file(html_path)
            print(f"  ✓ HTML profile → {html_path}")
        except Exception as e:
            print(f"  ⚠  ydata-profiling failed ({e}) – text profile saved above")
    print()

# Consolidated quality report
print("\n── CONSOLIDATED DATA QUALITY REPORT ──")
for qr in all_quality:
    print(f"\n  {qr['dataset'].upper()}")
    print(f"    Rows: {qr['rows']:,} | Cols: {qr['columns']}")
    print(f"    Missing: {qr['missing_pct']}% | Duplicates: {qr['duplicates']}")
    print(f"    Outlier summary: {qr['outlier_counts']}")

# Save consolidated quality to CSV
qa_path = os.path.join(OUT,"data_quality_summary.csv")
pd.DataFrame([{k:v for k,v in qr.items() if k!="outlier_counts"} for qr in all_quality]).to_csv(qa_path,index=False)
print(f"\n✓ Quality summary CSV → {qa_path}")
print("\n✅  Automated profiling complete!")
