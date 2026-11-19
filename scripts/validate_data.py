import pandas as pd
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"data"/"raw"
for f in p.glob("*.csv"):
    df=pd.read_csv(f)
    print(f"{f.name}: {len(df):,} rows | {len(df.columns)} columns | missing={int(df.isna().sum().sum())}")
