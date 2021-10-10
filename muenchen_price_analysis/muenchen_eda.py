import pandas as pd

path = r'D:\Documents\dataSets\listings.csv'
df = pd.read_csv(path)

# DF Head
df.head(10)

# DF Info
df.info()
df.count() / len(df)

# Dropping columns with 0 non-null values
na_cols = [c for c in df.columns if df[c].count() == 0]
df = df.drop([c for c in na_cols], axis=1)

# For this analysis I am not going to focus on 'host' data and I will drop columns related to it
host_cols = [c for c in df.columns if 'host' in c]
df = df.drop([c for c in host_cols], axis=1)
