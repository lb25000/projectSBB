# import libraries

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

# read data
all_data_df = pd.read_csv('Daten/perronkante.csv', sep=';')
pd.set_option('display.max_columns', None)
print(all_data_df.head())

data_types = all_data_df.dtypes
print(data_types)

# change object to string
columns_to_string = ['Abkuerzung Bahnhof', 'Haltestellen Name', 'Perrontyp', 'Hilfstritt', 'Höhenverlauf', 'Material', 'Kantenart', 'Auftritt']
all_data_df[columns_to_string] = all_data_df[columns_to_string].astype('string')

# boolean spalte für Hilfstritt
all_data_df['Hilfstritt boolean'] = np.where(all_data_df['Hilfstritt'] == 'vorhanden', True, False)
