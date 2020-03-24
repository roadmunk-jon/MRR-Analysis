import pandas as pd
import numpy as np
from datetime import datetime as dt
import re

# This file contains all of the subscriptions as they are provided by the input system.
df = pd.read_csv('schema/subscriptions_raw.csv')

# Identify subscriptions WITH an 'N/A' in any cell and write them to a file with a datetime suffix.
error_df = df.loc[df.isna().any(axis=1)]
error_path = "schema/subscriptions_errors/subscriptions_errors_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
error_df.to_csv(error_path, index=False)

# Identify subscriptions WITHOUT an 'N/A' in any cell and write them to a file with a datetime suffix.
df_for_processing = df.loc[df.notna().all(axis=1)]
clean_path = "schema/subscriptions_clean/subscriptions_clean_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
df_for_processing.to_csv(clean_path, index=False)

print(error_df, df_for_processing)