from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"

def load_data():
    sales = pd.read_csv(DATA / "monthly_vehicle_sales_demo.csv", parse_dates=["month"])
    state = pd.read_csv(DATA / "state_segment_demand_demo.csv", parse_dates=["month"])
    catalog = pd.read_csv(DATA / "competitor_catalog_demo.csv")
    return sales, state, catalog

def market_kpis(df):
    return {
        "units": int(df.units_sold.sum()),
        "brands": int(df.brand.nunique()),
        "models": int(df.model.nunique()),
        "avg_price": float(df.avg_ex_showroom_price_lakh.mean()) if len(df) else 0.0
    }

def segment_trends(sales):
    return sales.groupby(["month","segment"],as_index=False).units_sold.sum()

def competitor_summary(catalog, sales_period):
    s=sales_period.groupby("brand",as_index=False).units_sold.sum()
    out=catalog.groupby("brand",as_index=False).agg(
        models=("model","nunique"), avg_price_lakh=("price_lakh","mean"),
        avg_feature_score_demo=("feature_score_demo","mean"))
    out=out.merge(s,on="brand",how="left").fillna({"units_sold":0})
    total=out.units_sold.sum()
    out["share_pct_demo"]=(out.units_sold/total*100).round(1) if total else 0
    return out.sort_values("units_sold",ascending=False).round(2)

def forecast_sales(sales, brand, model, horizon=6):
    df=sales[(sales.brand==brand)&(sales.model==model)].sort_values("month")[["month","units_sold"]].copy()
    df["month"]=pd.to_datetime(df.month)
    # Hold out final 6 months; seasonal naive forecast uses value from 12 months earlier.
    split=max(12,len(df)-6)
    train=df.iloc[:split].copy()
    test=df.iloc[split:].copy()
    preds=[]
    for dt in test.month:
        prior=train[train.month == dt-pd.DateOffset(years=1)]
        preds.append(float(prior.units_sold.iloc[-1]) if len(prior) else float(train.units_sold.iloc[-1]))
    mae=mean_absolute_error(test.units_sold,preds) if len(test) else 0.0
    full=df.copy()
    fut=[]
    for i in range(1,horizon+1):
        dt=full.month.max()+pd.DateOffset(months=1)
        prior=full[full.month == dt-pd.DateOffset(years=1)]
        val=float(prior.units_sold.iloc[-1]) if len(prior) else float(full.units_sold.tail(3).mean())
        fut.append([dt,val])
        full=pd.concat([full,pd.DataFrame([[dt,val]],columns=["month","units_sold"])],ignore_index=True)
    return df, pd.DataFrame(fut,columns=["month","units_sold"]), {"mae":float(mae)}

def opportunity_scores(state):
    d=state.copy().sort_values("month")
    recent=d[d.month >= d.month.max()-pd.DateOffset(months=11)].groupby(["state","segment"],as_index=False).registrations.mean().rename(columns={"registrations":"recent_demand"})
    old_start=d.month.max()-pd.DateOffset(months=23)
    old_end=d.month.max()-pd.DateOffset(months=12)
    prior=d[(d.month>=old_start)&(d.month<=old_end)].groupby(["state","segment"],as_index=False).registrations.mean().rename(columns={"registrations":"prior_demand"})
    x=recent.merge(prior,on=["state","segment"],how="left")
    x["growth_pct"]=((x.recent_demand-x.prior_demand)/x.prior_demand.replace(0,np.nan)*100).fillna(0)
    # Transparent percentile-normalized screening score, not a commercial forecast.
    demand_rank=x.recent_demand.rank(pct=True)
    growth_rank=x.growth_pct.rank(pct=True)
    x["opportunity_score"]=(0.55*demand_rank+0.45*growth_rank)*100
    return x.sort_values("opportunity_score",ascending=False).round(1)
