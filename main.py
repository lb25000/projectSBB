import pandas as pd

def main():
    df_perronkante = pd.read_csv('./Daten/perronkante.csv',sep=';')
    print(df_perronkante)
    print(df_perronkante.keys())


if __name__ == '__main__':
    main()
