import pandas as pd
import numpy as np
from datetime import datetime as dt
import re

# The original dataframe is a table of months and companies, with the companies' MRR per month in each cell.
df = pd.read_csv("key_dates.csv")

# Remove the last column. It has NaN errors.
df = df.iloc[:, :-1]

# Retention

cohort_starting_mrr = df.sum(axis = 0, skipna = True)
cohort_starting_mrr = cohort_starting_mrr[2:]

cohort_ending_mrr = df.sum(axis = 0, skipna = True).where(df['2015-01-31'] > 0, 0)

# print(cohort_starting_mrr.head())
print (cohort_ending_mrr)