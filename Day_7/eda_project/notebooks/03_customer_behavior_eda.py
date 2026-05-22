"""
╔══════════════════════════════════════════════════════════╗
║  NOTEBOOK 3: CUSTOMER BEHAVIOR EDA                      ║
╚══════════════════════════════════════════════════════════╝
Run: python notebooks/03_customer_behavior_eda.py
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
sns.set_theme(style="whitegrid",palette="husl")
plt.rcParams.update({"figure.dpi":110,"font.size":10})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE,"reports")
os.makedirs(OUT,exist_ok=True)

def section(t): print(f"\n{'='*60}\n  {t}\n{'='*60}")

# ── LOAD
df = pd.read_csv(os.path.join(BASE,"data","customer_behavior_data.csv"),
                 parse_dates=["registration_date"])

# SECTION 1 – DATA UNDERSTANDING
section("SECTION 1: DATA UNDERSTANDING")
print(f" Shape        : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f" Reg range    : {df['registration_date'].min().date()} → {df['registration_date'].max().date()}")
print("\n── Column Types ──")
print(df.dtypes.to_string())
print("\n── Missing Values ──")
miss = df.isnull().sum()
print(pd.DataFrame({"Missing":miss,"Pct%":(miss/len(df)*100).round(2)})[miss>0].to_string())
print(f"\n Duplicates   : {df.duplicated().sum()}")

# SECTION 2 – DESCRIPTIVE STATISTICS
section("SECTION 2: DESCRIPTIVE STATISTICS")
num_cols = ["age","annual_income","lifetime_value","total_orders",
            "avg_order_value","sessions_per_month","churn_probability",
            "days_since_last_purchase"]
print(df[num_cols].describe().round(2).to_string())

print("\n── Variance & Std Dev ──")
for col in ["lifetime_value","annual_income","churn_probability"]:
    print(f"  {col:<28} var={df[col].var():>14,.2f}  std={df[col].std():>10,.2f}")

print("\n── Percentiles ──")
for col in ["lifetime_value","annual_income"]:
    pcts = df[col].quantile([0.1,0.25,0.5,0.75,0.9,0.95]).round(2)
    print(f"\n  {col}:")
    print(pcts.to_string())

print("\n── Skewness & Kurtosis ──")
for col in num_cols:
    print(f"  {col:<30} skew={df[col].skew():+.3f}  kurt={df[col].kurtosis():+.3f}")

# SECTION 3 – CATEGORICAL ANALYSIS
section("SECTION 3: CATEGORICAL ANALYSIS")
for col in ["segment","gender","city","preferred_channel"]:
    vc = df[col].value_counts()
    pct = (vc/len(df)*100).round(1)
    print(f"\n  {col}:")
    for k,v in vc.items():
        print(f"    {str(k):<18} {v:>5}  ({pct[k]}%)")

# SECTION 4 – SEGMENT ANALYSIS
section("SECTION 4: CUSTOMER SEGMENT ANALYSIS")
seg_stats = df.groupby("segment").agg(
    count=("customer_id","count"),
    avg_ltv=("lifetime_value","mean"),
    avg_orders=("total_orders","mean"),
    avg_churn=("churn_probability","mean"),
    avg_sessions=("sessions_per_month","mean"),
    avg_income=("annual_income","mean"),
).round(2)
print(seg_stats.to_string())

# SECTION 5 – OUTLIER DETECTION
section("SECTION 5: OUTLIER DETECTION")
for col in ["lifetime_value","annual_income","total_orders","sessions_per_month"]:
    q1,q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr = q3-q1
    cnt = ((df[col]<q1-1.5*iqr)|(df[col]>q3+1.5*iqr)).sum()
    print(f"  {col:<32} IQR outliers: {cnt}")

# SECTION 6 – CORRELATION ANALYSIS
section("SECTION 6: CORRELATION ANALYSIS")
corr = df[num_cols].corr()
print(corr.round(3).to_string())
print("\n── Top Correlations with LTV ──")
print(corr["lifetime_value"].drop("lifetime_value").abs().sort_values(ascending=False).to_string())
print("\n── Top Correlations with Churn ──")
print(corr["churn_probability"].drop("churn_probability").abs().sort_values(ascending=False).to_string())

# SECTION 7 – CHURN RISK ANALYSIS
section("SECTION 7: CHURN RISK ANALYSIS")
df["churn_risk"] = pd.cut(df["churn_probability"],bins=[0,0.2,0.5,0.8,1.0],
                          labels=["Low","Medium","High","Critical"])
print("── Churn Risk Distribution ──")
print(df["churn_risk"].value_counts().to_string())
print("\n── Churn Risk by Segment ──")
print(df.groupby("segment")["churn_probability"].agg(["mean","median","max"]).round(3).to_string())

# SECTION 8 – STATISTICAL TESTS
section("SECTION 8: STATISTICAL TESTS")
stat,p = stats.shapiro(df["lifetime_value"].sample(500,random_state=42))
print(f"\n  Shapiro-Wilk (LTV)  stat={stat:.4f}  p={p:.4e}  → {'NOT normal' if p<0.05 else 'Normal'}")

groups = [g["lifetime_value"].values for _,g in df.groupby("segment")]
f,pf = stats.f_oneway(*groups)
print(f"  ANOVA (LTV ~ segment)  F={f:.3f}  p={pf:.4e}  → {'Sig diff' if pf<0.05 else 'No sig diff'}")

ct = pd.crosstab(df["segment"],df["preferred_channel"])
chi2,pc,dof,_ = stats.chi2_contingency(ct)
print(f"  Chi-Square (segment × channel)  χ²={chi2:.3f}  dof={dof}  p={pc:.4e}  → {'Significant' if pc<0.05 else 'Not sig'}")

# T-test: male vs female LTV
m = df[df["gender"]=="Male"]["lifetime_value"].dropna()
f_grp = df[df["gender"]=="Female"]["lifetime_value"].dropna()
t,pt = stats.ttest_ind(m,f_grp)
print(f"  T-test (Male vs Female LTV)  t={t:.3f}  p={pt:.4e}  → {'Significant' if pt<0.05 else 'Not significant'}")

# SECTION 9 – PATTERN IDENTIFICATION
section("SECTION 9: PATTERN IDENTIFICATION")
print("── City-wise LTV & Churn ──")
print(df.groupby("city")[["lifetime_value","churn_probability"]].mean().round(3).to_string())
print("\n── Channel Preference by Segment ──")
print(pd.crosstab(df["segment"],df["preferred_channel"],normalize="index").round(3).to_string())
print("\n── Age Buckets ──")
df["age_bucket"] = pd.cut(df["age"],bins=[18,25,35,45,55,75],labels=["18-25","26-35","36-45","46-55","55+"])
print(df.groupby("age_bucket")["lifetime_value"].mean().round(2).to_string())

# SECTION 10 – VISUALIZATIONS
section("SECTION 10: GENERATING VISUALIZATIONS")

fig = plt.figure(figsize=(18,16))
fig.suptitle("Customer Behavior EDA Dashboard",fontsize=16,fontweight="bold",y=0.99)
gs = gridspec.GridSpec(4,3,figure=fig,hspace=0.5,wspace=0.35)

# LTV distribution by segment
ax1 = fig.add_subplot(gs[0,:2])
for seg in df["segment"].unique():
    vals = df[df["segment"]==seg]["lifetime_value"].dropna()
    ax1.hist(vals,bins=40,alpha=0.5,label=seg,density=True)
ax1.set_title("LTV Distribution by Segment"); ax1.set_xlabel("Lifetime Value (₹)"); ax1.legend()

# Segment count pie
ax2 = fig.add_subplot(gs[0,2])
sc = df["segment"].value_counts()
ax2.pie(sc,labels=sc.index,autopct="%1.1f%%",colors=sns.color_palette("husl",len(sc)))
ax2.set_title("Customer Segment Mix")

# Churn probability by segment
ax3 = fig.add_subplot(gs[1,0])
seg_order = df.groupby("segment")["churn_probability"].mean().sort_values(ascending=False).index
for i,seg_name in enumerate(seg_order):
    ax3.boxplot(df[df["segment"]==seg_name]["churn_probability"].dropna().values,
                positions=[i],patch_artist=True)
ax3.set_xticks(range(len(seg_order))); ax3.set_xticklabels(seg_order,rotation=30)
ax3.set_title("Churn Probability by Segment"); ax3.set_xlabel(""); plt.sca(ax3)

# Age distribution
ax4 = fig.add_subplot(gs[1,1])
ax4.hist(df["age"].dropna(),bins=30,color="#4C72B0",edgecolor="white",linewidth=0.5)
ax4.set_title("Age Distribution"); ax4.set_xlabel("Age"); ax4.set_ylabel("Count")

# Sessions vs LTV
ax5 = fig.add_subplot(gs[1,2])
smp = df.dropna(subset=["sessions_per_month","lifetime_value"]).sample(500,random_state=42)
scatter = ax5.scatter(smp["sessions_per_month"],smp["lifetime_value"],
           alpha=0.4,s=15,c=smp["churn_probability"],cmap="RdYlGn_r")
plt.colorbar(scatter,ax=ax5,label="Churn Prob")
ax5.set_title("Sessions vs LTV (color=Churn)"); ax5.set_xlabel("Sessions/Month"); ax5.set_ylabel("LTV (₹)")

# City heatmap
ax6 = fig.add_subplot(gs[2,0])
city_seg = df.groupby(["city","segment"])["customer_id"].count().unstack(fill_value=0)
sns.heatmap(city_seg,ax=ax6,annot=True,fmt="d",cmap="Blues",cbar=False)
ax6.set_title("Customers: City × Segment"); ax6.tick_params(axis="x",rotation=30)

# Channel preference bar
ax7 = fig.add_subplot(gs[2,1])
ch_seg = pd.crosstab(df["preferred_channel"],df["segment"],normalize="index")*100
ch_seg.plot(kind="bar",ax=ax7,stacked=True,colormap="tab10")
ax7.set_title("Channel Preference by Segment"); ax7.set_xlabel(""); ax7.tick_params(axis="x",rotation=30)
ax7.legend(fontsize=7,loc="upper right")

# Correlation heatmap
ax8 = fig.add_subplot(gs[2,2])
corr_small = df[["age","lifetime_value","total_orders","churn_probability","sessions_per_month"]].corr()
sns.heatmap(corr_small,annot=True,fmt=".2f",cmap="coolwarm",vmin=-1,vmax=1,ax=ax8,linewidths=0.5)
ax8.set_title("Key Feature Correlations")

# Age bucket LTV
ax9 = fig.add_subplot(gs[3,0])
age_ltv = df.groupby("age_bucket")["lifetime_value"].mean()
ax9.bar(age_ltv.index.astype(str),age_ltv.values,color=sns.color_palette("viridis",len(age_ltv)))
ax9.set_title("Avg LTV by Age Group"); ax9.set_xlabel("Age Bucket"); ax9.set_ylabel("Avg LTV (₹)")

# Days since purchase by segment
ax10 = fig.add_subplot(gs[3,1])
segs = df["segment"].unique()
for i,seg_name in enumerate(segs):
    ax10.boxplot(df[df["segment"]==seg_name]["days_since_last_purchase"].dropna().values,
                 positions=[i],patch_artist=True)
ax10.set_xticks(range(len(segs))); ax10.set_xticklabels(segs,rotation=30)
ax10.set_title("Days Since Purchase by Segment"); ax10.set_xlabel(""); plt.sca(ax10)

# Churn risk distribution
ax11 = fig.add_subplot(gs[3,2])
cr = df["churn_risk"].value_counts()
colors_cr = {"Low":"green","Medium":"orange","High":"red","Critical":"darkred"}
ax11.bar(cr.index,cr.values,color=[colors_cr.get(c,"grey") for c in cr.index])
ax11.set_title("Churn Risk Tier Distribution"); ax11.set_ylabel("Count")

p1 = os.path.join(OUT,"03_customer_dashboard.png")
plt.savefig(p1,bbox_inches="tight"); plt.close(); print(f"  Saved → {p1}")

# Segment deep-dive
fig2,axes = plt.subplots(2,3,figsize=(16,10))
fig2.suptitle("Customer Segment Deep Dive",fontsize=14,fontweight="bold")
metrics = ["lifetime_value","total_orders","avg_order_value","sessions_per_month","churn_probability","annual_income"]
for ax,(col,title) in zip(axes.flat,[(m,m.replace("_"," ").title()) for m in metrics]):
    seg_means = df.groupby("segment")[col].mean().sort_values(ascending=False)
    ax.bar(seg_means.index,seg_means.values,color=sns.color_palette("husl",len(seg_means)))
    ax.set_title(f"Avg {title} by Segment"); ax.tick_params(axis="x",rotation=30)
p2 = os.path.join(OUT,"03_customer_segment_deepdive.png")
plt.savefig(p2,bbox_inches="tight"); plt.close(); print(f"  Saved → {p2}")

print("\n✅  Customer Behavior EDA complete!")
