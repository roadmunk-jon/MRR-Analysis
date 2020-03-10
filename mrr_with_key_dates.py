import pandas as pd
import numpy as np
from datetime import datetime as dt
import re

# The original dataframe is a table of months and companies, with the companies' MRR per month in each cell.
# The first 5 fields are non-MRR : 'Row Labels', 'managed?', 'tier', 'first_date', and 'last_date'.
df = pd.read_csv("key_dates.csv")

# Remove the last column. It has NaN errors.
df = df.iloc[:, :-1]

# Retention

# Find the total MRR each month. This will be the denominator.
cohort_starting_mrr = df.sum(axis = 0, skipna = True)
cohort_starting_mrr = cohort_starting_mrr[2:]

# Find the MRR 12 months later from companies that made up the denominator. This will be the numerator.
# df['matches'] = df.apply(lambda x: x['2016-01-31'] if x['2015-01-31'] >= 1 else 0, axis=1)
# cohort_ending_mrr = df.matches.sum()
cohort_mrr_12_mths_later = []

for cohort in list(df.columns[17:]):
    ending_month = pd.to_datetime(np.datetime64(cohort)) + pd.DateOffset(years=1)
    ending_month_string = ending_month.strftime('%Y-%m-%d')
    if ending_month < pd.to_datetime(np.datetime64('2019-01-31')):
        ending_mrr = df.apply(lambda x: x[cohort] if x[ending_month_string] >= 1 else 0, axis=1)
        sum_of_ending_mrr = ending_mrr.sum()
        mrr_object = {cohort: ending_mrr}
        cohort_mrr_12_mths_later.append(mrr_object)


# print(cohort_starting_mrr.head())
print (cohort_mrr_12_mths_later)