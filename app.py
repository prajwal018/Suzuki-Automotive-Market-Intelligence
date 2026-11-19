import streamlit as st
import pandas as pd
import plotly.express as px
from src.analytics import load_data, market_kpis, forecast_sales, opportunity_scores, competitor_summary, segment_trends

st.set_page_config(page_title="AutoMarket Intelligence", page_icon="🚗", layout="wide")
st.title("🚗 Automotive Market Intelligence & Product Strategy")
st.caption("Portfolio prototype | Indian passenger vehicle market | Demo data is synthetic and must not be represented as official industry data.")

sales, state, catalog = load_data()
st.sidebar.header("Analysis controls")
brands = ["All"] + sorted(sales.brand.unique().tolist())
selected_brand = st.sidebar.selectbox("Brand", brands)
year_min, year_max = pd.to_datetime(sales.month).dt.year.min(), pd.to_datetime(sales.month).dt.year.max()
year = st.sidebar.slider("Year", int(year_min), int(year_max), int(year_max))
filtered = sales[pd.to_datetime(sales.month).dt.year == year].copy()
if selected_brand != "All":
    filtered = filtered[filtered.brand == selected_brand]

k = market_kpis(filtered)
cols = st.columns(4)
for col, label, val in zip(cols, ["Units in selected year","Brands tracked","Models tracked","Average listed price"],
                           [f"{k['units']:,.0f}", str(k["brands"]), str(k["models"]), f"₹{k['avg_price']:.1f}L"]):
    col.metric(label, val)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Market overview","Competitor intelligence","Sales forecast","Regional opportunity","Product planning"])
with tab1:
    st.subheader("Market overview")
    by_brand = filtered.groupby("brand",as_index=False).units_sold.sum().sort_values("units_sold",ascending=False)
    c1,c2=st.columns(2)
    c1.plotly_chart(px.bar(by_brand,x="brand",y="units_sold",title="Demo units sold by brand",color="brand"),use_container_width=True)
    seg=filtered.groupby("segment",as_index=False).units_sold.sum().sort_values("units_sold",ascending=False)
    c2.plotly_chart(px.pie(seg,names="segment",values="units_sold",title="Segment mix in demo data"),use_container_width=True)
    trends=segment_trends(sales)
    st.plotly_chart(px.line(trends,x="month",y="units_sold",color="segment",title="Monthly segment trend (demo data)"),use_container_width=True)
    st.info("Interpretation: use the trend chart to identify segment momentum. Validate with official SIAM/VAHAN/FADA datasets before making real market claims.")
with tab2:
    st.subheader("Competitor benchmarking")

    sales_for_year = sales[
        sales["month"].dt.year == int(year)
    ]

    summary = competitor_summary(catalog, sales_for_year)

    st.dataframe(summary, width="stretch", hide_index=True)

    st.plotly_chart(
        px.scatter(
            catalog,
            x="price_lakh",
            y="feature_score_demo",
            size="variant_count_demo",
            color="brand",
            hover_name="model",
            title="Illustrative price-feature positioning (catalogue scores are synthetic)"
        ),
        width="stretch"
    )
with tab3:
    st.subheader("Monthly sales forecast")
    brand_for_forecast=st.selectbox("Forecast brand",sorted(sales.brand.unique()),key="forecast_brand")
    model_for_forecast=st.selectbox("Forecast model",sorted(sales[sales.brand==brand_for_forecast].model.unique()),key="forecast_model")
    history, future, metrics=forecast_sales(sales,brand_for_forecast,model_for_forecast,horizon=6)
    st.metric("Holdout MAE (units)", f"{metrics['mae']:,.0f}", help="Time-ordered holdout evaluation; demo data only.")
    plot=pd.concat([history.assign(series="Actual"),future.assign(series="Forecast")])
    st.plotly_chart(px.line(plot,x="month",y="units_sold",color="series",markers=True,title=f"{model_for_forecast}: actual history and 6-month baseline forecast"),use_container_width=True)
    st.caption("Forecast uses a transparent seasonal-naive baseline. Extend with SARIMA/XGBoost after validating real data and backtesting.")
with tab4:
    st.subheader("Regional opportunity screening")
    opp=opportunity_scores(state)
    st.dataframe(opp, use_container_width=True, hide_index=True)
    st.plotly_chart(px.bar(opp.head(10),x="state",y="opportunity_score",color="segment",title="Top state-segment opportunity scores (screening index)"),use_container_width=True)
    st.caption("Opportunity score is a relative screening index based on recent growth and demand in synthetic data; it is not a market-entry recommendation.")
with tab5:
    st.subheader("Product planning decision support")
    opp_seg=segment_trends(sales).groupby("segment",as_index=False).units_sold.sum().sort_values("units_sold",ascending=False)
    st.dataframe(opp_seg, use_container_width=True, hide_index=True)
    st.markdown("""
    **Suggested decision workflow**
    1. Identify segments with sustained growth across multiple periods.
    2. Compare Suzuki's model coverage and price bands against competing offerings.
    3. Validate customer needs using survey/review research.
    4. Estimate addressable demand, margin, capacity and regulatory constraints.
    5. Present a business case with assumptions, risks and a test plan.
    """)
    st.warning("This prototype does not automatically declare a winning product. Product decisions require validated customer, cost, capacity and market evidence.")

st.divider()
st.caption("Built as a portfolio project demonstrating Python, SQL-ready data pipelines, forecasting, competitive analysis and business decision support.")
