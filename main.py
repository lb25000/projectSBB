import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pandastable import Table

def readData():
    #silent warnings
    pd.set_option('future.no_silent_downcasting', True)
    # Read data from CSV File
    df_perronkante = pd.read_csv('./Daten/perronkante.csv', sep=';')

    # Splitting the '1_koord' and '2_koord' columns into separate columns
    start_coords = df_perronkante['1_koord'].str.split(',', expand=True)
    end_coords = df_perronkante['2_koord'].str.split(',', expand=True)

    # Renaming columns
    start_coords.columns = ['start_lon', 'start_lat']
    end_coords.columns = ['end_lon', 'end_lat']

    # Concatenating start and end coordinates with original DataFrame
    df_perronkante = pd.concat([df_perronkante, start_coords, end_coords], axis=1)


    df_perronkante = df_perronkante.drop(['1_koord', '2_koord'], axis='columns')

    return df_perronkante

def showTable():
    # Create a new Tkinter window
    window = tk.Toplevel(root)
    window.title("DataFrame Viewer")

    # Create a Pandas Table object
    table = Table(window, dataframe=df)
    table.show()
    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(window, orient="horizontal", command=table.horizontal_scroll)
    hsb.pack(side="bottom", fill="x")
    table.set_xscrollcommand(hsb.set)

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
