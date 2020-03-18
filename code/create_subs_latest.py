import pandas as pd
import numpy as np
from datetime import datetime as dt
import re
import glob
import os


# Get the file containing the latest output of raw_file_processor.py
list_of_subs_files = glob.glob('schema/*.csv')
latest_subs_file = max(list_of_subs_files, key=os.path.getctime)
subs_df = pd.read_csv(latest_subs_file)

# Add an analysis_datetime column with the current datetime.
subs_df['analysis_datetime'] = dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p")



# Add gross and net MRR/ARR columns based on products.


latest_subs_path = "schema/subscriptions_latest_" + dt.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + ".csv"
subs_df.to_csv(latest_subs_path, index=False)

print(subs_df)