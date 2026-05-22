"""
╔══════════════════════════════════════════════════════════╗
║  NOTEBOOK 2: TIME SERIES EDA                            ║
╚══════════════════════════════════════════════════════════╝
Run: python notebooks/02_timeseries_eda.py
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from scipy.signal import periodogram
import warnings, os

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.dpi":110,"font.size":10})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE,"reports")
os.makedirs(OUT,exist_ok=True)

def section(t): print(f"\n{'='*60}\n  {t}\n{'='*60}")

# ── LOAD
df = pd.read_csv(os.path.join(BASE,"data","timeseries_data.csv"), parse_dates=["date"])
df = df.sort_values(["store","date"]).reset_index(drop=True)

# SECTION 1 – DATA UNDERSTANDING
section("SECTION 1: DATA UNDERSTANDING")
print(f" Shape      : {df.shape}")
print(f" Stores     : {df['store'].nunique()} → {df['store'].unique().tolist()}")
print(f" Date range : {df['date'].min().date()} → {df['date'].max().date()}")
print(f" Days       : {df['date'].nunique()}")
print("\n── Column Info ──")
print(df.dtypes.to_string())
print("\n── Missing Values ──")
miss = df.isnull().sum()
print(pd.DataFrame({"Missing":miss,"Pct%":(miss/len(df)*100).round(2)})[miss>0].to_string())

# SECTION 2 – SUMMARY STATISTICS
section("SECTION 2: SUMMARY STATISTICS")
num_cols = ["sales","transactions","avg_basket","foot_traffic","temperature"]
print(df[num_cols].describe().round(2).to_string())
print("\n── Per-Store Summary ──")
print(df.groupby("store")["sales"].agg(["mean","median","std","min","max"]).round(2).to_string())

# SECTION 3 – DATETIME FEATURES & PATTERNS
section("SECTION 3: DATETIME FEATURES")
df["year"]      = df["date"].dt.year
df["month"]     = df["date"].dt.month
df["weekday"]   = df["date"].dt.dayofweek
df["week"]      = df["date"].dt.isocalendar().week.astype(int)
df["quarter"]   = df["date"].dt.quarter
df["month_name"]= df["date"].dt.month_name()

print("── Monthly Avg Sales (all stores) ──")
print(df.groupby("month")["sales"].mean().round(2).to_string())
print("\n── Weekday Avg Sales ──")
wd = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
print(df.groupby("weekday")["sales"].mean().rename({i:wd[i] for i in range(7)}).round(2).to_string())
print("\n── Holiday vs Non-Holiday Sales ──")
print(df.groupby("is_holiday")["sales"].agg(["mean","median","count"]).round(2).to_string())

# SECTION 4 – TREND ANALYSIS
section("SECTION 4: TREND ANALYSIS")
store_a = df[df["store"]=="Store_A"].dropna(subset=["sales"]).copy()
x = np.arange(len(store_a))
slope, intercept, r, p, se = stats.linregress(x, store_a["sales"])
print(f"\n  Store_A linear trend: slope={slope:.2f}/day  R²={r**2:.4f}  p={p:.4e}")
print(f"  → {'Significant upward trend' if slope>0 and p<0.05 else 'No significant trend'}")

# Rolling stats
for store in ["Store_A","Store_B"]:
    s = df[df["store"]==store].dropna(subset=["sales"]).set_index("date")["sales"]
    roll_mean = s.rolling(30).mean()
    roll_std  = s.rolling(30).std()
    cv_end = (roll_std.iloc[-1]/roll_mean.iloc[-1]*100)
    print(f"  {store} – 30-day rolling CV at end: {cv_end:.1f}%")

# SECTION 5 – SEASONALITY DETECTION
section("SECTION 5: SEASONALITY DETECTION")
pivot_monthly = df.pivot_table(values="sales",index="month",columns="year",aggfunc="mean").round(2)
print("── Monthly Avg Sales by Year ──")
print(pivot_monthly.to_string())
print("\n── Q-Quarter Analysis ──")
print(df.groupby("quarter")["sales"].mean().round(2).to_string())

# SECTION 6 – ANOMALY DETECTION
section("SECTION 6: ANOMALY DETECTION")
def detect_anomalies_zscore(series, threshold=3):
    z = np.abs(stats.zscore(series.dropna()))
    return (z > threshold).sum()

def detect_anomalies_iqr(series):
    q1,q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3-q1
    return ((series < q1-3*iqr) | (series > q3+3*iqr)).sum()

print("\n── Anomaly Count per Store ──")
for store, grp in df.groupby("store"):
    s = grp["sales"].dropna()
    z_cnt  = detect_anomalies_zscore(s)
    iq_cnt = detect_anomalies_iqr(s)
    print(f"  {store}: Z-score anomalies={z_cnt}, IQR anomalies={iq_cnt}")

# SECTION 7 – CORRELATION (sales vs external factors)
section("SECTION 7: CORRELATION WITH EXTERNAL FACTORS")
corr_cols = ["sales","transactions","avg_basket","foot_traffic","temperature","is_holiday"]
corr_matrix = df[corr_cols].corr()
print(corr_matrix.round(3).to_string())

# SECTION 8 – MISSING VALUE PATTERNS
section("SECTION 8: MISSING VALUE PATTERNS")
miss_by_store = df.groupby("store")[["sales","transactions","avg_basket"]].apply(
    lambda x: x.isnull().sum()).rename(columns=lambda c: c+"_missing")
print(miss_by_store.to_string())

# SECTION 9 – VISUALIZATIONS
section("SECTION 9: GENERATING VISUALIZATIONS")

# Main dashboard
fig = plt.figure(figsize=(18,16))
fig.suptitle("Time Series EDA Dashboard",fontsize=16,fontweight="bold",y=0.99)
gs = gridspec.GridSpec(4,2,figure=fig,hspace=0.5,wspace=0.3)

# All stores sales over time
ax1 = fig.add_subplot(gs[0,:])
for store in df["store"].unique():
    s = df[df["store"]==store].dropna(subset=["sales"])
    s_weekly = s.set_index("date")["sales"].resample("W").mean()
    ax1.plot(s_weekly.index, s_weekly.values, label=store, linewidth=1.5, alpha=0.8)
ax1.set_title("Weekly Average Sales – All Stores")
ax1.set_xlabel("Date"); ax1.set_ylabel("Sales (₹)")
ax1.legend(loc="upper left",fontsize=8); ax1.tick_params(axis="x",rotation=30)

# Seasonal – monthly boxplot
ax2 = fig.add_subplot(gs[1,0])
month_order = list(range(1,13))
data_by_month = [df[df["month"]==m]["sales"].dropna().values for m in month_order]
ax2.boxplot(data_by_month,labels=[str(m) for m in month_order],patch_artist=True,
            boxprops=dict(facecolor="#4C72B0",alpha=0.5))
ax2.set_title("Monthly Sales Distribution"); ax2.set_xlabel("Month"); ax2.set_ylabel("Sales (₹)")

# Weekday pattern
ax3 = fig.add_subplot(gs[1,1])
wd_sales = df.groupby("weekday")["sales"].mean()
ax3.bar([wd[i] for i in range(7)],[wd_sales.get(i,0) for i in range(7)],
        color=sns.color_palette("muted",7))
ax3.set_title("Average Sales by Day of Week")
ax3.set_xlabel("Day"); ax3.set_ylabel("Avg Sales (₹)")

# Temperature vs Sales scatter
ax4 = fig.add_subplot(gs[2,0])
sample = df.dropna(subset=["sales","temperature"]).sample(1000,random_state=42)
ax4.scatter(sample["temperature"],sample["sales"],alpha=0.3,s=10,c="#4C72B0")
m,b = np.polyfit(sample["temperature"],sample["sales"],1)
x_line = np.linspace(sample["temperature"].min(),sample["temperature"].max(),100)
ax4.plot(x_line,m*x_line+b,"r--",linewidth=2,label=f"Trend (slope={m:.0f})")
ax4.set_title("Temperature vs Sales"); ax4.set_xlabel("Temp (°C)"); ax4.set_ylabel("Sales (₹)")
ax4.legend()

# Holiday vs non-holiday
ax5 = fig.add_subplot(gs[2,1])
df_plot = df.dropna(subset=["sales"])
df_plot["holiday_label"] = df_plot["is_holiday"].map({0:"Regular",1:"Holiday"})
df_plot.boxplot(column="sales",by="holiday_label",ax=ax5,patch_artist=True,grid=False)
ax5.set_title("Sales: Holiday vs Regular Days"); ax5.set_xlabel(""); plt.sca(ax5)

# Rolling mean + std band (Store_A)
ax6 = fig.add_subplot(gs[3,:])
sa = df[df["store"]=="Store_A"].dropna(subset=["sales"]).set_index("date")["sales"].sort_index()
roll_mean = sa.rolling(30,center=True).mean()
roll_std  = sa.rolling(30,center=True).std()
ax6.plot(sa.index,sa.values,alpha=0.3,color="#4C72B0",linewidth=0.8,label="Raw")
ax6.plot(roll_mean.index,roll_mean.values,color="darkblue",linewidth=2,label="30-day MA")
ax6.fill_between(roll_mean.index,roll_mean-2*roll_std,roll_mean+2*roll_std,
                 alpha=0.2,color="blue",label="±2σ band")
# Mark anomalies
z = np.abs(stats.zscore(sa))
anom = sa[z>3]
ax6.scatter(anom.index,anom.values,color="red",s=50,zorder=5,label=f"Anomalies ({len(anom)})")
ax6.set_title("Store_A – Rolling Mean with Anomaly Detection")
ax6.set_xlabel("Date"); ax6.set_ylabel("Sales (₹)"); ax6.legend()

p1 = os.path.join(OUT,"02_timeseries_dashboard.png")
plt.savefig(p1,bbox_inches="tight"); plt.close(); print(f"  Saved → {p1}")

# Correlation heatmap
fig2,ax = plt.subplots(figsize=(8,7))
mask = np.triu(np.ones_like(corr_matrix,dtype=bool))
sns.heatmap(corr_matrix,mask=mask,annot=True,fmt=".2f",cmap="coolwarm",
            vmin=-1,vmax=1,ax=ax,linewidths=0.5)
ax.set_title("Time Series Feature Correlation Matrix",fontsize=13)
p2 = os.path.join(OUT,"02_timeseries_correlation.png")
plt.savefig(p2,bbox_inches="tight"); plt.close(); print(f"  Saved → {p2}")

print("\n✅  Time Series EDA complete!")
