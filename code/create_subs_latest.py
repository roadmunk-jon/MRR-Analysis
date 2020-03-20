import pandas as pd
import numpy as np
from datetime import datetime as dt
import re
import glob
import os


# Get the file containing the latest output of raw_file_processor.py
list_of_files = glob.glob('schema/*.csv')

list_of_subs_files =[]
for sub in list_of_files:
    if sub.startswith('schema/subscriptions_clean_'):
        list_of_subs_files.append(sub)
latest_subs_file = max(list_of_subs_files, key=os.path.getctime)
latest_subs_df = pd.read_csv(latest_subs_file)

# Add an analysis_datetime column with the current datetime.
latest_subs_df['analysis_datetime'] = dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p")

# This section deals with calculating MRR/ARR
# Join bundles_products (an associative table between bundles and products) to subs for subs_bundles.
bundle_df = pd.read_csv('schema/bundles_products.csv')
subs_bundles_df = pd.merge(latest_subs_df, bundle_df, on='bundle_id')

# Join subs_bundles and products for subs_products.
products_df = pd.read_csv('schema/products.csv')
subs_products = pd.merge(subs_bundles_df, products_df, on='product_id')

# # Write the MRR and ARR to columns in the latest_subs_df
latest_subs_df['mrr'] = subs_products['monthly_unit_price'].sum()
latest_subs_df['arr'] = subs_products['annual_unit_price'].sum()


# latest_subs_path = "schema/subscriptions_latest_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
# latest_subs_df.to_csv(latest_subs_path, index=False)

print(latest_subs_df)