import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pandastable import Table, TableModel
import warnings

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


def search_columns(table):
    # Get all column names
    column_names = df.columns.tolist()
    print(column_names)

    # Create a frame for search fields
    search_frame = ttk.Frame(table)
    search_frame.pack(side="top", fill="x",padx=5,pady=(5,5))  # Pack on top

    # Create and position search entries for each column
    search_entries = []  # List to store search entries
    for i, column_name in enumerate(column_names):
        column_width = len(column_name)

        search_entry = ttk.Entry(search_frame, width=column_width)
        search_entry.grid(column=i, row=1, padx=(5,10), pady=5)  # Grid positioning
        search_entries.append(search_entry)
        search_entries.append(search_entry)

        # Bind a function to the search entry for filtering and highlighting
        def filter_by_column(event, col_idx=i):
            search_term = search_entries[col_idx].get()
            # Filter data based on search term
            df_filtered = df[df[column_names[col_idx]].str.contains(search_term)]

            # Update table model with filtered data
            table.model.df = df_filtered
            table.model.set_data(df_filtered.values.tolist())  # Refresh table data

            # Clear table selection (optional)
            table.unbind("<Button-1>")

            # Highlight matching rows (optional)
            for row_idx in range(table.numberofrows):
                if search_term in str(table.get_value(row_idx, col_idx)):
                    table.configure_row(row_idx, background="lightblue")
                else:
                    table.configure_row(row_idx, background="white")

        search_entry.bind("<KeyRelease>", filter_by_column)
def showTable():
    # Create a new Tkinter window
    window = tk.Toplevel(root)
    window.title("DataFrame Viewer")

    # Create a ttk.Notebook widget
    notebook = ttk.Notebook(window)
    notebook.pack(side="top", fill="both", expand=True)

    # Create a frame for search fields
    search_frame = ttk.Frame(notebook)
    search_frame.pack(side="top", fill="x", padx=5, pady=(10, 20))  # Add padding

    # Create search entries within the search frame
    search_columns(search_frame)  # Add search fields to the search frame

    # Create a frame for the table
    table_frame = ttk.Frame(notebook)
    table_frame.pack(side="top", fill="both", expand=True)

    # Create a Pandas Table object in the table frame
    global table
    table = Table(table_frame, dataframe=df)
    table.show()

    # Add horizontal scrollbar to the table frame
    hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=table.horizontal_scroll)
    hsb.pack(side="bottom", fill="x")
    table.set_xscrollcommand(hsb.set)

    # Add tabs to the notebook
    notebook.add



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