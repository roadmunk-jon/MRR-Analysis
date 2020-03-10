import pandas as pd
import numpy as np
from datetime import datetime as dt
import re

# The original dataframe is a table of months and companies, with the companies' MRR per month in each cell.
df = pd.read_csv("key_dates.csv")

# Remove the last column. It has NaN errors.
df = df.iloc[:, :-1]

# Convert headers to datetime.
# month
# datetime_headers = []
# for column in list(df.columns.values[5:]):
#     datetime_headers += dt.strptime(column, '%Y-%M-%d')

# Retention

# cohort_starting_mrr = df.groupby(['2015-01-31']).sum()
cohort_starting_mrr = df.sum(axis = 0, skipna = True)
cohort_starting_mrr = cohort_starting_mrr[2:]

# cohort_starting_mrr =  df[[col for col in df.columns if col not in ("Customer Name", "managed?", "first_date", "last_date") 
#            and dt(col[:3], ) >= dt(2015,1,1) 
#            and dt(col) <= dt(2016,3,1)]]

# print(cohort_starting_mrr.head())
print (cohort_starting_mrr)