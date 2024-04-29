# import libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



import requests
from owslib.wmts import WebMapTileService


import geopandas as gpd
from shapely.geometry import Point, Polygon
import seaborn as sns

# read data
all_data_df = pd.read_csv('Daten/perronkante.csv', sep=';')
print(all_data_df.shape)
'''
pd.set_option('display.max_columns', None)
print(all_data_df.head())

data_types = all_data_df.dtypes
print(data_types)
'''
# change object to string
columns_to_string = ['Abkuerzung Bahnhof', 'Haltestellen Name', 'Perrontyp', 'Hilfstritt', 'Höhenverlauf', 'Material', 'Kantenart', 'Auftritt']
all_data_df[columns_to_string] = all_data_df[columns_to_string].astype('string')

# boolean spalte für Hilfstritt
all_data_df['Hilfstritt boolean'] = np.where(all_data_df['Hilfstritt'] == 'vorhanden', True, False)
# Trennen der Koordinaten in Start- und Endkoordinaten
all_data_df[['start_lat', 'start_lon']] = all_data_df['1_koord'].str.split(',', expand=True)
all_data_df[['end_lat', 'end_lon']] = all_data_df['2_koord'].str.split(',', expand=True)

# Benennen der neuen Spalten
all_data_df = all_data_df.rename(columns={'start_lat': 'start_lat', 'start_lon': 'start_lon',
                                          'end_lat': 'end_lat', 'end_lon': 'end_lon'})

# Konvertieren der Spalten in numerische Werte
all_data_df[['start_lat', 'start_lon', 'end_lat', 'end_lon']] = all_data_df[['start_lat', 'start_lon', 'end_lat', 'end_lon']].astype(float)



print(all_data_df.shape)
#unique values
print(all_data_df['Höhenverlauf'].unique())
def filter_by_Hilfstritt(df):
    """filtert dataframe nach Hilfstritt

        :argument
            - dataframe

        :returns
            - dataframe with stations with Hilfstritt
    """
    df_Hilfstritt = df.loc[df['Hilfstritt boolean'] == True]
    print(df_Hilfstritt.shape)

    return df_Hilfstritt

def filter_by_Höhenverlauf(df):
    """
    filtert dataframe nach Höhenverlauf
    :param df:
    :return df: 3 dataframes depending on höhenverlauf
    """
    df_konstant = df.loc[df['Höhenverlauf'] == 'konstant']
    df_nicht_konstant = df.loc[df['Höhenverlauf'] == 'nicht konstant']
    df_Karrenueberfahrten = df.loc[df['Höhenverlauf'] == 'Karrenüberfahrent']
    df_auslaufend = df.loc[df['Höhenverlauf'] == 'auslaufend']
    return df_konstant, df_nicht_konstant,df_Karrenueberfahrten, df_auslaufend

def filter_by_Perronkantenlänge(df,x,y):
    """
    filtert nach Perronlängen
    :param x: Perronlänge ist grösser als x
    :param y: Perronlänge ist kleiner als y
    :return: df mit x < Perrolänge < y
    """
    df_Perronlänge = df.loc[(df['Perronkantenlänge'] > x) & (df['Perronkantenlänge'] < y)]
    return df_Perronlänge


pd.set_option('display.max_columns', None)
print(filter_by_Perronkantenlänge(all_data_df, 100, 120))





def filter_and_plot_geographic_area(df, min_x, max_x, min_y, max_y):
    """
    Filtert den DataFrame nach Einträgen, die sich in einem bestimmten geografischen Bereich befinden,
    und stellt die Ergebnisse graphisch dar.

    :param df: DataFrame, der gefiltert werden soll.
    :param min_x: Minimale x-Koordinate des geografischen Bereichs (LV95).
    :param max_x: Maximale x-Koordinate des geografischen Bereichs (LV95).
    :param min_y: Minimale y-Koordinate des geografischen Bereichs (LV95).
    :param max_y: Maximale y-Koordinate des geografischen Bereichs (LV95).
    """

    switzerland_coords = {
        'lat_0': 46.8182,
        'lon_0': 8.2275,
        'llcrnrlon': 5.9561,
        'llcrnrlat': 45.818,
        'urcrnrlon': 10.4921,
        'urcrnrlat': 47.8085,
    }
    # Erstellen einer Basiskarte
    m = Basemap(**switzerland_coords, projection='merc', resolution='h')

    # Zeichnen von  Grenzen
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary()

    # Filtern des DataFrames nach Koordinaten im geografischen Bereich
    filtered_df = df[(df['start_lat'] >= min_y) & (df['start_lat'] <= max_y) &
                     (df['start_lon'] >= min_x) & (df['start_lon'] <= max_x) |
                     (df['end_lat'] >= min_y) & (df['end_lat'] <= max_y) &
                     (df['end_lon'] >= min_x) & (df['end_lon'] <= max_x)]

    # Konvertieren der Koordinaten in das Koordinatensystem der Basiskarte
    x_start, y_start = m(filtered_df['start_lon'].values, filtered_df['start_lat'].values)
    x_end, y_end = m(filtered_df['end_lon'].values, filtered_df['end_lat'].values)

    # Plotten der gefilterten Koordinaten auf der Karte
    m.scatter(x_start, y_start, marker='o', color='r', label='Startpunkt', zorder=5, s=10)
    m.scatter(x_end, y_end, marker='o', color='b', label='Endpunkt', zorder=5, s=10)


    plt.title('geographical representation of the edges of the platform')

    # Anzeigen der Karte
    plt.show()





# Beispielaufruf der Funktion mit einem geografischen Bereich
filter_and_plot_geographic_area(all_data_df, 6.5, 9.5, 45.5, 48.0)
