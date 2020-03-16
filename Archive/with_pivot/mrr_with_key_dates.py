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
cohort_mrr_12_mths_later = {'cohort': [], 'starting_mrr': [], 'ending_mrr': [], 'retention': []}

for cohort in list(df.columns[7:]):
    # Find the total MRR each month. This will be the denominator.
    cohort_starting_mrr = df[cohort].sum(axis = 0, skipna = True)
    # Find the MRR 12 months later from the companies that made up the denominator.
    # This will be the numerator.
    ending_month = pd.to_datetime(np.datetime64(cohort)) + pd.DateOffset(years=1)
    ending_month_string = ending_month.strftime('%Y-%m-%d')
    if ending_month < pd.to_datetime(np.datetime64('2020-01-31')):
        cohort_ending_mrr = df.apply(lambda x: x[ending_month_string] if x[cohort] >= 1 else 0, axis=1).sum()
        cohort_mrr_12_mths_later['cohort'].append(cohort)
        cohort_mrr_12_mths_later['starting_mrr'].append(cohort_starting_mrr)
        cohort_mrr_12_mths_later['ending_mrr'].append(cohort_ending_mrr)
        cohort_mrr_12_mths_later['retention'].append(cohort_starting_mrr/cohort_ending_mrr)

retention_df = pd.DataFrame(data=cohort_mrr_12_mths_later)

# print(cohort_starting_mrr.head())
print (retention_df)