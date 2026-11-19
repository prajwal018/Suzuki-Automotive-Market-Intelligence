# Automotive Market Intelligence & Product Strategy Platform

A portfolio-ready analytics application aligned with automotive marketing, market research, sales strategy and product planning responsibilities.

## What it demonstrates
- Multi-table automotive data analysis with Python and Pandas
- Competitor benchmarking and price-feature positioning
- Segment and monthly trend analysis
- Time-ordered sales forecasting with a seasonal-naive baseline and MAE evaluation
- Regional opportunity screening using transparent demand and growth scoring
- Interactive executive dashboard with Streamlit and Plotly
- Decision-oriented product planning workflow

## Important data disclosure
The included CSV files are **synthetic demonstration data generated for this portfolio project**. They are not official Maruti Suzuki, SIAM, VAHAN, FADA or competitor sales figures. Do not present demo outputs as real market findings.

For a credible real-world version, replace the demo CSVs with licensed or publicly available data and document the source, retrieval date, units, coverage and limitations. Suggested sources:
- VAHAN Analytics: https://www.analytics.parivahan.gov.in/analytics/publicdashboard/vahan
- SIAM: https://www.siam.in/statistical-services/statistical-profile
- FADA: https://www.fada.in/
- Maruti Suzuki investor reports: https://www.marutisuzuki.com/corporate/investors/company-reports
- UN Comtrade: https://comtradeplus.un.org/

Check each source's terms, access restrictions and data definitions before reuse. Public dashboard data may not be downloadable in bulk.

## Quick start

### 1. Clone
```bash
git clone https://github.com/<your-username>/suzuki-automotive-market-intelligence.git
cd suzuki-automotive-market-intelligence
```

### 2. Create environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

### 5. Validate input data
```bash
python scripts/validate_data.py
```

## Data dictionary

### monthly_vehicle_sales_demo.csv
| Column | Meaning |
|---|---|
| month | Month start date |
| brand | Manufacturer |
| model | Vehicle model |
| segment | Illustrative vehicle segment |
| avg_ex_showroom_price_lakh | Approximate demo price in lakh; synthetic |
| fuel_type | Synthetic fuel category |
| units_sold | Synthetic monthly unit volume |

### state_segment_demand_demo.csv
| Column | Meaning |
|---|---|
| month | Month start date |
| state | State/UT label |
| segment | Vehicle segment |
| registrations | Synthetic registrations |

### competitor_catalog_demo.csv
Contains synthetic model-level price, fuel options, variant count and feature score. The feature score is illustrative only.

## Architecture

```text
Data sources / CSV extracts
        |
        v
Data validation (scripts/validate_data.py)
        |
        v
Pandas analytics layer (src/analytics.py)
        |
        +--> Market and segment analysis
        +--> Competitor benchmarking
        +--> Forecast baseline + MAE
        +--> Regional opportunity score
        |
        v
Streamlit + Plotly executive dashboard
        |
        v
Business interpretation and product planning
```

## Methodology notes
- Forecasting uses a seasonal-naive baseline (same month in the prior year) so assumptions are transparent and easy to explain.
- The last six observations are held out in chronological order for MAE evaluation.
- Regional opportunity score combines percentile ranks of recent demand (55%) and year-over-year growth (45%). It is a screening index, not an investment decision.
- The dashboard intentionally distinguishes illustrative data from verified market evidence.

## Recommended next upgrades
1. Add official source adapters and a source metadata table.
2. Add SQL persistence (PostgreSQL) and scheduled ETL.
3. Backtest SARIMA/XGBoost against seasonal-naive baseline using rolling-origin validation.
4. Add confidence intervals and forecast error monitoring.
5. Add real model specifications and customer review data with citations.
6. Add an executive report export and scenario assumptions.
7. Add unit tests and CI workflow before production deployment.

## Suggested GitHub description
Automotive market intelligence and product strategy dashboard using Python, Pandas, forecasting, competitor benchmarking, regional opportunity scoring, Streamlit and Plotly. Includes clearly labeled synthetic demo data.

## Resume wording (use only after you have run and verified it)
**Automotive Market Intelligence & Product Strategy Platform**
- Built an interactive automotive market intelligence dashboard to analyze manufacturer performance, vehicle segment trends, competitor positioning and regional demand.
- Implemented time-ordered sales forecasting with holdout MAE evaluation and a transparent regional opportunity scoring framework.
- Developed decision-support views for market research and product planning using Python, Pandas, Scikit-learn, Streamlit and Plotly.

Do not claim improved business revenue, official market share or model accuracy unless you validate those results with real data.
