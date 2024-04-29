import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pandastable import Table

def readData():
    # Read data from CSV File
    df_perronkante = pd.read_csv('./Daten/perronkante.csv', sep=';')

    # Create DataFrame for coordinates
    koord = pd.DataFrame(data=df_perronkante['2_koord'].str.split(',', expand=True))
    koord.columns=['lon', 'lat']

    # Adding longtitude and latitude in df_perronkante
    df_perronkante.insert(22, koord['lon'].name, koord['lon'])
    df_perronkante.insert(23, koord['lat'].name, koord['lat'])
    df_perronkante = df_perronkante.astype({'lon':float, 'lat':float})

    # Remove redundant column "2_koord"
    df_perronkante = df_perronkante.drop("2_koord", axis='columns')

    return df_perronkante

def showTable():
    # Create a new Tkinter window
    window = tk.Toplevel(root)
    window.title("DataFrame Viewer")

    # Create a Pandas Table object
    table = Table(window, dataframe=df)
    table.show()

def plot_data():
    # Add code to plot data here
    messagebox.showinfo("Plot Data", "Plotting functionality will be added here.")

def main():
    global df
    df = readData()

    global root
    root = tk.Tk()
    root.title("SBB Dataset Exploration")

    # Create a frame for the buttons
    button_frame = ttk.Frame(root, padding="10")
    button_frame.grid(column=0, row=0)

    # Create buttons for different actions
    ttk.Button(button_frame, text="Show Table", command=showTable).grid(column=0, row=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Plot data", command=plot_data).grid(column=0, row=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Exit", command=root.quit).grid(column=0, row=3, padx=5, pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
