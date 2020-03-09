import pandas as pd
import numpy as np

# The original dataframe is a table of months and companies, with the companies' MRR per month in each cell.
df = pd.read_csv("mrr.csv")

# For now, all numbers are rounded to avoid very small negative values, e.g. -0.01.
df = df.round(0)

#  WIP: Round only values that are less than 0.
# num = df._get_numeric_data()
# num[num < 0] = 0

# Finding the first date a company produced MRR.
first_date = df.keys()[2+np.argmax(df.values!=0,axis=1)]
df.insert(2, "first_date", first_date)

print(df.head())