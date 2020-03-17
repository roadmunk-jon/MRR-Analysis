import pandas as pd
import numpy as np
from datetime import datetime as dt
import re

# The original dataframe is a table of months and companies, with the companies' MRR per month in each cell.
df = pd.read_csv("schema/subscriptions.csv")

print (df)