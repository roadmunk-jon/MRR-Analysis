import pandas as pd
import numpy as np
from datetime import datetime as dt
import re

# This file contains all of the subscriptions as they are provided by the input system.
df = pd.read_csv("schema/subscriptions_raw.csv")



print (df)