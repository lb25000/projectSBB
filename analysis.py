
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



#print(all_data_df)
#unique values


import operator
ops = {
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    '!=': operator.ne,
    ">=": operator.ge,
    ">": operator.gt
}   

#brauchbar für Linie, KM, Perronkantenlänge,GO_IPID,Didok-Nummer,IPID,FID,BPUIC
def filter_Universal_Numbers(df, firstOperator = None, firstNumber = None, secondOperator = None, secondNumber = None, columnName = None):
    """
    
    :param firstOperator: erster assignment operator nach dem gefiltert wird. Z.B >=
    :param firstNumber: erste grösse nachdem gefiltert wird, z.b. 200
    :param secondOperator: zweiter assignment operator nach dem gefiltert wird. Z.B <
    :param secondNumber: zweite grösse nachdem gefiltert wird, z.b. 400
    :param columnName: Der Column-Name in der gefiltert werden soll
    :return: gefiltertes dataframe
    """
    line_df = df
    if(firstOperator != None and secondNumber == None):
        line_df = df[ops[firstOperator](df[columnName],firstNumber)]
        
    if(operator != None and secondNumber != None):
        line_df = df[(ops[firstOperator](df[columnName],firstNumber)) & (ops[secondOperator](df[columnName],secondNumber))]
        
    return line_df    


#filter_Universal_Numbers(all_data_df, "<", 400, columnName="Linie")  
#filter_Universal_Numbers(all_data_df, "<", 400, ">=", 200, columnName="Linie") 
#filter_Universal_Numbers(all_data_df, "==", 850, columnName="Linie") 

def filter_String(df, word = None, columnName = None):
    '''
    :param word: wort nachdem gesucht und verglichen wird
    :param columnName: Der Column-Name in der gefiltert werden soll
    :return: gefiltertes dataframe'''
    line_df = df
    if(word != None):
        line_df = df[df[columnName] == word]
    
    return line_df

#filter_String(all_data_df, "vorhanden", columnName = "Hilfstritt")
