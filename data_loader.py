"""
Handles data loading and preprocessing functions.
"""
import pandas as pd

def read_data():
    """
    Reads tabular data from a CSV file and preprocesses it for further use.
    Returns: pandas.DataFrame: A DataFrame containing the read data with processed coordinates.
    """
    try:
        df_perronkante = pd.read_csv('./Daten/perronkante.csv', sep=';')
        # Splitting the '1_koord' and '2_koord' columns into separate columns
        start_coords = df_perronkante['1_koord'].str.split(',', expand=True)
        end_coords = df_perronkante['2_koord'].str.split(',', expand=True)
        start_coords.columns = ['start_lat', 'start_long']
        end_coords.columns = ['end_lat', 'end_long']
        df_perronkante = pd.concat([df_perronkante, start_coords, end_coords], axis=1)
        df_perronkante = df_perronkante.drop(['1_koord', '2_koord'], axis='columns')
        return df_perronkante
    except Exception as e:
        raise RuntimeError(f"Failed to read data: {e}")
