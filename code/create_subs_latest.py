import pandas as pd
import numpy as np
from datetime import datetime as dt
import re
import glob
import os


# Get the file containing the latest output of raw_file_processor.py
list_of_files = glob.glob('schema/subscriptions_clean/*.csv')
latest_subs_file = max(list_of_files, key=os.path.getctime)
latest_subs_df = pd.read_csv(latest_subs_file)

# # Add an analysis_datetime column with the current datetime.
latest_subs_df['analysis_datetime'] = dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p")

# # This section deals with calculating MRR/ARR
# # Join bundles_products (an associative table between bundles and products) to subs for subs_bundles.
bundle_df = pd.read_csv('schema/bundles_products.csv')
subs_bundles_df = pd.merge(latest_subs_df, bundle_df, on='bundle_id')
subs_bundles_df = subs_bundles_df[subs_bundles_df['valid'] == 1]

# # Join subs_bundles and products for subs_products.
products_df = pd.read_csv('schema/products.csv')
subs_products_df = pd.merge(subs_bundles_df, products_df, on='product_id')
subs_products_df = subs_products_df.groupby('RMID')[['annual_unit_price', 'monthly_unit_price']].sum()

# # Merge the MRR and ARR into the latest_subs_df
latest_subs_df = pd.merge(latest_subs_df, subs_products_df, on='RMID')
latest_subs_df.rename(columns={'annual_unit_price': 'arr', 'monthly_unit_price': 'mrr'}, inplace=True)

# # This section deals with movement classification.
# # Join accounts and logos for accounts_logos
accounts_df = pd.read_csv('schema/accounts.csv')
logos_df = pd.read_csv('schema/logos.csv')
accounts_logos_df = pd.merge(accounts_df, logos_df, on='logo_id')

# # Add the relevant columns to latest_subs_df.
latest_subs_df = pd.merge(latest_subs_df, accounts_logos_df)

latest_subs_df['logo_start'] = latest_subs_df['first_start_of_term_y']
latest_subs_df['logo_end'] = latest_subs_df['last_end_of_term_y']
latest_subs_df['last_gross_mrr'] = latest_subs_df['gross_mrr_y']
latest_subs_df['last_gross_arr'] = latest_subs_df['gross_arr_y']
latest_subs_df['last_net_mrr'] = latest_subs_df['net_mrr_y']
latest_subs_df['last_net_arr'] = latest_subs_df['net_arr_y']

latest_subs_df.drop(['first_start_of_term_y',
                    'last_end_of_term_y',
                    'gross_mrr_y',
                    'gross_arr_y',
                    'net_mrr_y',
                    'net_arr_y',
                    'first_start_of_term_x',
                    'last_end_of_term_x',
                    'gross_mrr_x',
                    'gross_arr_x',
                    'net_mrr_x',
                    'net_arr_x'
                    ], axis=1)

'''
Assigning the classification is done from least to most precise.
E.g. churning is a form of contraction ($1 -> $0), so first the subscription
is classified as contraction, then the classification is overwritten as a churn.
'''

# # Is it an increase since the last subscriptions (expansion)?
# latest_subs_df.loc[(latest_subs_df['mrr'] > latest_subs_df['last_gross_mrr'])
#     , 'movement_classification'] = "expansion"

# Is it a decrease since the last subscriptions (contraction)?
latest_subs_df.loc[(latest_subs_df['mrr'] < latest_subs_df['last_gross_mrr'])
    , 'movement_classification'] = "contraction"

# Is it the same as the last subscriptions (stable)?
latest_subs_df.loc[(latest_subs_df['mrr'] == latest_subs_df['last_gross_mrr'])
    , 'movement_classification'] = "stable"

# Is it the first time this logo has a subscription (new)?
latest_subs_df.loc[(latest_subs_df['start_of_term'] == latest_subs_df['logo_start'])
    , 'movement_classification'] = "new"

# # Is it the last time this logo has a subscription (churn)?
latest_subs_df.loc[(latest_subs_df['end_of_term'] == latest_subs_df['logo_end'])
    , 'movement_classification'] = "churn"

latest_subs_path = "schema/subscriptions_latest/subscriptions_latest_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
latest_subs_df.to_csv(latest_subs_path, index=False)

print(latest_subs_df)