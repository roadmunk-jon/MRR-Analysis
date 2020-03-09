import pandas as pd

# The original dataframe is a table of months and companies, with the companies' MRR per month in each cell.
df = pd.read_csv("mrr.csv")

# Some MRR values have very small negatives. These are rounded up to 0.
# df = df.round(0)

num = df._get_numeric_data()

num[num < 0] = 0

print(df.head())