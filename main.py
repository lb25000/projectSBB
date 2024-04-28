import pandas as pd

def main():
    # Read data from CSV File
    df_perronkante = pd.read_csv('./Daten/perronkante.csv', sep=';')
    print(df_perronkante['2_koord'])

    # Create DataFrame for coordinates
    koord = pd.DataFrame(data=df_perronkante['2_koord'].str.split(',', expand=True))
    koord.columns=['lon', 'lat']

    # Adding longtitude and latitude in df_perronkante
    df_perronkante.insert(22, koord['lon'].name, koord['lon'])
    df_perronkante.insert(23, koord['lat'].name, koord['lat'])
    df_perronkante = df_perronkante.astype({'lon':float, 'lat':float})

    # Remove redundant column "2_koord"
    df_perronkante = df_perronkante.drop("2_koord", axis='columns')
    
    # Printing to check the modifications
    print(df_perronkante)
    print(df_perronkante.dtypes)


if __name__ == '__main__':
    main()
