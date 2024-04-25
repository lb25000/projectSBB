# import libraries

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

# read data
all_data_df = pd.read_csv('Daten/perronkante.csv', sep=';')
pd.set_option('display.max_columns', None)
print(all_data_df.head())



