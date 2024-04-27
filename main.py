import pandas as pd

def main():
    # Read data from CSV File
    df_perronkante = pd.read_csv('./Daten/perronkante.csv', sep=';')
    
    print(df_perronkante)
    print(df_perronkante.dtypes)


if __name__ == '__main__':
    main()
