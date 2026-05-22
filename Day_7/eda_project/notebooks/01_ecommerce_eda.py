"""
╔══════════════════════════════════════════════════════════╗
║  NOTEBOOK 1: E-COMMERCE EDA                             ║
╚══════════════════════════════════════════════════════════╝
Run: python notebooks/01_ecommerce_eda.py
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings, os

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams.update({"figure.dpi":110,"font.size":10})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE,"reports")
os.makedirs(OUT, exist_ok=True)

def section(t): print(f"\n{'='*60}\n  {t}\n{'='*60}")

# ── LOAD
df = pd.read_csv(os.path.join(BASE,"data","ecommerce_data.csv"), parse_dates=["date"])

# SECTION 1 – DATA UNDERSTANDING
section("SECTION 1: DATA UNDERSTANDING")
print(f" Shape        : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f" Memory usage : {df.memory_usage(deep=True).sum()/1024:.1f} KB")
print(f" Date range   : {df['date'].min().date()} → {df['date'].max().date()}")
print("\n── Column Types ──")
print(df.dtypes.to_string())
print("\n── Missing Values ──")
miss = df.isnull().sum()
miss_pct = (miss/len(df)*100).round(2)
print(pd.DataFrame({"Missing":miss,"Pct%":miss_pct})[miss>0].to_string())
print(f"\n Duplicate rows: {df.duplicated().sum()}")

# SECTION 2 – SUMMARY STATISTICS
section("SECTION 2: SUMMARY STATISTICS")
num_cols = ["price","quantity","discount_pct","revenue","customer_rating","delivery_days"]
print(df[num_cols].describe().round(2).to_string())
print("\n── Skewness & Kurtosis ──")
for col in ["price","quantity","revenue"]:
    print(f"  {col:<18} skew={df[col].skew():+.3f}  kurtosis={df[col].kurtosis():+.3f}")
print("\n── Categorical Value Counts ──")
for col in ["category","region","order_status","payment_method"]:
    print(f"\n  {col}:")
    print(df[col].value_counts().to_string())

# SECTION 3 – OUTLIER DETECTION
section("SECTION 3: OUTLIER DETECTION")
def iqr_outliers(s):
    q1,q3=s.quantile(0.25),s.quantile(0.75); iqr=q3-q1
    return ((s<q1-1.5*iqr)|(s>q3+1.5*iqr)).sum(), q1-1.5*iqr, q3+1.5*iqr
for col in ["price","quantity","revenue"]:
    cnt,lo,hi = iqr_outliers(df[col].dropna())
    print(f"  {col:<18} {cnt:>5} outliers  (fence: {lo:.0f} – {hi:.0f})")
for col in ["price","revenue"]:
    z = np.abs(stats.zscore(df[col].dropna()))
    print(f"  Z>3  {col:<14}: {(z>3).sum()} extreme values")

# SECTION 4 – DISTRIBUTION ANALYSIS
section("SECTION 4: DISTRIBUTION ANALYSIS")
print("── Revenue Percentiles ──")
for p in [10,25,50,75,90,95,99]:
    print(f"  P{p:>2}: ₹{df['revenue'].quantile(p/100):>12,.2f}")
print("\n── Category Revenue ──")
print(df.groupby("category")["revenue"].agg(["sum","mean","median","std"]).round(2).to_string())

# SECTION 5 – CORRELATION
section("SECTION 5: CORRELATION ANALYSIS")
corr = df[num_cols].corr()
print(corr.round(3).to_string())
print("\n── Top Correlations with Revenue ──")
print(corr["revenue"].drop("revenue").abs().sort_values(ascending=False).to_string())

# SECTION 6 – PATTERNS
section("SECTION 6: PATTERN IDENTIFICATION")
df["month"]   = df["date"].dt.month
df["weekday"] = df["date"].dt.day_name()
df["quarter"] = df["date"].dt.quarter
df["year"]    = df["date"].dt.year
wd_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
weekday_rev = df.groupby("weekday")["revenue"].mean().reindex(wd_order)
print("── Avg Revenue by Weekday ──")
print(weekday_rev.round(2).to_string())
print("\n── Region × Category Revenue ──")
print(df.pivot_table(values="revenue",index="region",columns="category",aggfunc="sum").round(0).to_string())

# SECTION 7 – STATISTICAL TESTS
section("SECTION 7: STATISTICAL TESTS")
stat,p = stats.shapiro(df["revenue"].sample(500,random_state=42))
print(f"\n  Shapiro-Wilk  stat={stat:.4f}  p={p:.4e}  → {'NOT normal' if p<0.05 else 'Normal'}")
groups = [g["revenue"].values for _,g in df.groupby("category")]
f,pf = stats.f_oneway(*groups)
print(f"  One-Way ANOVA F={f:.3f}  p={pf:.4e}  → {'Significant differences' if pf<0.05 else 'No sig diff'}")
ct = pd.crosstab(df["payment_method"],df["order_status"])
chi2,pc,dof,_ = stats.chi2_contingency(ct)
print(f"  Chi-Square    χ²={chi2:.3f}  dof={dof}  p={pc:.4e}  → {'Significant association' if pc<0.05 else 'No association'}")

# SECTION 8 – VISUALIZATIONS
section("SECTION 8: GENERATING VISUALIZATIONS")

# Dashboard
fig = plt.figure(figsize=(18,14))
fig.suptitle("E-Commerce EDA Dashboard",fontsize=16,fontweight="bold",y=0.98)
gs = gridspec.GridSpec(3,3,figure=fig,hspace=0.45,wspace=0.35)

ax1 = fig.add_subplot(gs[0,0])
rev_clean = df["revenue"][df["revenue"]<df["revenue"].quantile(0.99)]
ax1.hist(rev_clean,bins=50,color="#4C72B0",edgecolor="white",linewidth=0.5)
ax1.set_title("Revenue Distribution (excl. top 1%)")
ax1.set_xlabel("Revenue (₹)"); ax1.set_ylabel("Count")

ax2 = fig.add_subplot(gs[0,1])
cat_data = df.groupby("category")["revenue"].sum().sort_values()
cat_data.plot(kind="barh",ax=ax2,color=sns.color_palette("husl",len(cat_data)))
ax2.set_title("Total Revenue by Category"); ax2.set_xlabel("Revenue (₹)")

ax3 = fig.add_subplot(gs[0,2])
monthly_plot = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
monthly_plot.plot(ax=ax3,color="#4C72B0",linewidth=2)
ax3.set_title("Monthly Revenue Trend"); ax3.tick_params(axis="x",rotation=45)

ax4 = fig.add_subplot(gs[1,0])
sc = df["order_status"].value_counts()
ax4.pie(sc,labels=sc.index,autopct="%1.1f%%",colors=sns.color_palette("pastel"))
ax4.set_title("Order Status Distribution")

ax5 = fig.add_subplot(gs[1,1])
weekday_rev.plot(kind="bar",ax=ax5,color=sns.color_palette("muted",7))
ax5.set_title("Avg Revenue by Weekday"); ax5.tick_params(axis="x",rotation=45)

ax6 = fig.add_subplot(gs[1,2])
smp = df.sample(500,random_state=42)
ax6.scatter(smp["discount_pct"],smp["revenue"],alpha=0.4,c=smp["quantity"],cmap="viridis",s=20)
ax6.set_title("Discount % vs Revenue"); ax6.set_xlabel("Discount %"); ax6.set_ylabel("Revenue (₹)")

ax7 = fig.add_subplot(gs[2,:2])
pivot_plot = df.pivot_table(values="revenue",index="region",columns="category",aggfunc="sum")
sns.heatmap(pivot_plot/1e6,ax=ax7,annot=True,fmt=".1f",cmap="YlOrRd",cbar_kws={"label":"Revenue (₹M)"})
ax7.set_title("Revenue Heatmap – Region × Category (₹M)")

ax8 = fig.add_subplot(gs[2,2])
df_no_out = df[df["price"]<df["price"].quantile(0.95)]
cat_order = df_no_out.groupby("category")["price"].median().sort_values().index
plot_data = [df_no_out[df_no_out["category"]==c]["price"].values for c in cat_order]
ax8.boxplot(plot_data,labels=list(cat_order),patch_artist=True)
ax8.tick_params(axis="x",rotation=45)
ax8.set_title("Price Distribution by Category"); ax8.set_xlabel("")
fig.suptitle("E-Commerce EDA Dashboard",fontsize=16,fontweight="bold",y=0.99)
p1 = os.path.join(OUT,"01_ecommerce_dashboard.png")
plt.savefig(p1,bbox_inches="tight"); plt.close(); print(f"  Saved → {p1}")

# Outlier boxplots
fig2,axes = plt.subplots(1,3,figsize=(16,5))
fig2.suptitle("E-Commerce: Outlier Boxplots",fontsize=13,fontweight="bold")
for ax,col in zip(axes,["price","revenue","quantity"]):
    ax.boxplot(df[col].dropna(),vert=True,patch_artist=True,boxprops=dict(facecolor="#4C72B0",alpha=0.6))
    ax.set_title(f"{col} Boxplot"); ax.set_ylabel(col)
p2 = os.path.join(OUT,"01_ecommerce_outliers.png")
plt.savefig(p2,bbox_inches="tight"); plt.close(); print(f"  Saved → {p2}")

# Correlation heatmap
fig3,ax = plt.subplots(figsize=(9,7))
mask = np.triu(np.ones_like(corr,dtype=bool))
sns.heatmap(corr,mask=mask,annot=True,fmt=".2f",cmap="coolwarm",vmin=-1,vmax=1,ax=ax,linewidths=0.5)
ax.set_title("Correlation Matrix – Numerical Features",fontsize=13)
p3 = os.path.join(OUT,"01_ecommerce_correlation.png")
plt.savefig(p3,bbox_inches="tight"); plt.close(); print(f"  Saved → {p3}")

print("\n✅  E-Commerce EDA complete!")
