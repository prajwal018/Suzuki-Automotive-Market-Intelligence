from src.analytics import load_data, market_kpis, forecast_sales, opportunity_scores

def test_demo_data_loads():
    sales, state, catalog = load_data()
    assert not sales.empty and not state.empty and not catalog.empty

def test_kpis():
    sales, _, _ = load_data()
    k = market_kpis(sales)
    assert k["units"] > 0
    assert k["brands"] >= 5

def test_forecast_shape():
    sales, _, _ = load_data()
    brand = sales.brand.iloc[0]
    model = sales[sales.brand == brand].model.iloc[0]
    _, future, metrics = forecast_sales(sales, brand, model)
    assert len(future) == 6
    assert metrics["mae"] >= 0

def test_opportunity_scores():
    _, state, _ = load_data()
    scores = opportunity_scores(state)
    assert "opportunity_score" in scores.columns
    assert scores.opportunity_score.between(0, 100).all()
