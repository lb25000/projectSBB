# import libraries

import pandas as pd
import numpy as np
import matplotlib as plt
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
columns_to_string = ['Abkuerzung Bahnhof', 'Haltestellen Name', 'Perrontyp', 'Hilfstritt', 'Höhenverlauf', 'Material', 'Kantenart', 'Auftritt', '1_koord', '2_koord']
all_data_df[columns_to_string] = all_data_df[columns_to_string].astype('string')

# boolean spalte für Hilfstritt
all_data_df['Hilfstritt boolean'] = np.where(all_data_df['Hilfstritt'] == 'vorhanden', True, False)

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

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

def filter_and_plot_geographic_area(df, min_lon, max_lon, min_lat, max_lat):
    """
    Filtert den DataFrame nach Einträgen, die sich in einem bestimmten geografischen Bereich befinden,
    und stellt die Ergebnisse graphisch dar.

    :param df: DataFrame, der gefiltert werden soll.
    :param min_lon: Minimale Längenkoordinate des geografischen Bereichs.
    :param max_lon: Maximale Längenkoordinate des geografischen Bereichs.
    :param min_lat: Minimale Breitencoordinate des geografischen Bereichs.
    :param max_lat: Maximale Breitencoordinate des geografischen Bereichs.
    """
    # Erstelle ein Polygon, das den geografischen Bereich definiert
    bounding_box = Polygon([(min_lon, min_lat), (min_lon, max_lat), (max_lon, max_lat), (max_lon, min_lat)])

    # Konvertiere Koordinaten in Punkte
    df['point_1'] = df['1_koord'].apply(lambda x: Point(map(float, x.split(', '))))
    df['point_2'] = df['2_koord'].apply(lambda x: Point(map(float, x.split(', '))))

    # Filtere Einträge, die sich in dem geografischen Bereich befinden
    filtered_df = df[(df['point_1'].apply(lambda x: bounding_box.contains(x))) |
                     (df['point_2'].apply(lambda x: bounding_box.contains(x)))]

    # Erstelle eine GeoDataFrame für die Punkte innerhalb des geografischen Bereichs
    points_within_area = gpd.GeoDataFrame(filtered_df, geometry='point_1')

    # Erstelle die Abbildung und die Achsen
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plotte den geografischen Bereich
    gpd.GeoSeries(bounding_box).plot(ax=ax, color='lightblue', alpha=0.5, label='Geographic Area')

    # Plotte die Punkte innerhalb des geografischen Bereichs
    points_within_area.plot(ax=ax, color='red', markersize=50, label='Points within Area')

    # Beschriftungen hinzufügen
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Points within Geographic Area')

    # Anzeigen der Abbildung
    plt.show()

# Beispielaufruf der Funktion mit einem geografischen Bereich
filter_and_plot_geographic_area(all_data_df, 47, 8.2, 47, 8.7)
