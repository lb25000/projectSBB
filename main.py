import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TableGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Table GUI")
        self.master.geometry("800x400")  # Größe der GUI anpassen

        # DataFrame einlesen
        self.df = readData()

        # copy original df, to have a backup
        self.original_df = self.df.copy()

        # copy original df to undo filters
        self.undo_df = self.original_df.copy()

        # definition of numeric and string columns

        self.integer_columns = ["Linie", "Didok-Nummer", "IPID", "FID", "BPUIC"]
        self.float_columns = ["KM", "Perronkantenlänge", "GO_IPID"]
        self.string_columns = ["Abkuerzung Bahnhof", "Haltestellen Name", "Perrontyp", "Perron Nummer",
                               "Kundengleisnummer", "Perronkantenhöhe", "Bemerkung Höhe", "Hilfstritt"
                                                                                          "Höhenverlauf", "Material",
                               "Bemerkung Material", "Kantenart",
                               "Bemerkung Kantenkrone", "Auftritt", "lod", "start_lon", "start_lat",
                               "end_lon", "end_lat"]

        # Frame for table
        self.table_frame = ttk.Frame(master)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Style für die Tabelle anpassen, um Linien zwischen den Zellen anzuzeigen
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25, foreground="black", background="white")
        style.configure("Treeview.Heading", font=('Helvetica', 10), foreground="black", background="#eaeaea",
                        relief="raised")
        style.map("Treeview", background=[('selected', '#add8e6')])

        # Tabelle erstellen
        self.table = ttk.Treeview(self.table_frame, style="Treeview")
        self.table["columns"] = list(self.df.columns)
        self.table["show"] = "headings"
        for col in self.df.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, minwidth=50, anchor="center")  # Spaltenbreite anpassen
        self.table.pack(side="left", fill="both", expand=True)

        # Zeilen in der Tabelle einfügen
        self.insert_table_rows()

        # Scrollbars für die Tabelle hinzufügen
        yscrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        yscrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        xscrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.table.xview)
        xscrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

        self.table.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        # Suchfelder Frame mit Canvas für Scrollbar
        self.search_frame = ttk.Frame(master)

        self.search_canvas = tk.Canvas(self.search_frame)
        self.search_canvas.pack(side="left", fill="both", expand=True)

        self.search_entries_frame = ttk.Frame(self.search_canvas)
        yscrollbar = ttk.Scrollbar(self.search_frame, orient="vertical", command=self.search_canvas.yview)
        yscrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        xscrollbar = ttk.Scrollbar(self.search_frame, orient="horizontal", command=self.search_canvas.xview)
        xscrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
        self.search_canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        self.search_entries = {}  # Initialisierung des search_entries-Attributs

        # Eingabefelder Frame mit Canvas für Scrollbar
        self.input_frame = ttk.Frame(master)

        self.input_canvas = tk.Canvas(self.input_frame)
        self.input_canvas.pack(side="left", fill="both", expand=True)

        self.input_entries_frame = ttk.Frame(self.input_canvas)
        yscrollbar = ttk.Scrollbar(self.input_frame, orient="vertical", command=self.input_canvas.yview)
        yscrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        xscrollbar = ttk.Scrollbar(self.input_frame, orient="horizontal", command=self.input_canvas.xview)
        xscrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
        self.input_canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        self.input_entries = {}  # Initialisierung des input_entries-Attributs

        #coordinates

        self.coordinate_frame = ttk.Frame(master)
        self.coordinate_canvas = tk.Canvas(self.coordinate_frame)
        self.coordinate_canvas.pack(side="left", fill="both", expand=True)
        self.coordinate_entries_frame = ttk.Frame(self.coordinate_canvas)
        xscrollbar = ttk.Scrollbar(self.coordinate_frame, orient="horizontal", command=self.coordinate_canvas.xview)
        xscrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
        self.coordinate_canvas.configure(xscrollcommand=xscrollbar.set)

        # Buttons
        button_frame = ttk.Frame(master)
        button_frame.pack()
        search_button = ttk.Button(button_frame, text="Search", command=self.show_search_fields)
        search_button.pack(side="left", padx=5)
        add_button = ttk.Button(button_frame, text="Add", command=self.show_input_fields)
        add_button.pack(side="left", padx=5)

        self.go_button = ttk.Button(button_frame, text="Go", command=self.execute_search)
        self.go_button.pack(side="left", padx=5)
        undo_filter_button = ttk.Button(button_frame, text="Undo filters", command=self.undo_filter)
        undo_filter_button.pack(side="left", padx=5)
        plot_coordinates_button = ttk.Button(button_frame, text="Plot coordinates", command=self.show_coordinate_search)
        plot_coordinates_button.pack(side="left", padx=5)

        self.pack_search_and_input()
        self.column_stats = {}

    def update_table(self):
        """
        Updates the table by removing all existing rows and inserting rows from the updated DataFrame.
        """
        for row in self.table.get_children():
            self.table.delete(row)
        self.insert_table_rows()

    def insert_table_rows(self):
        """
        Inserts rows (data) into the table based on the DataFrame.
        """
        for col in self.df.columns:
            self.table.heading(col, text=col, command=lambda c=col: self.show_column_stats(c))  # bind command to header

        for i, row in self.df.iterrows():
            row = row.fillna('')
            self.table.insert("", "end", values=list(row))

    def calculate_column_stats(self, column_name):
        column = self.df[column_name]
        if column_name in self.integer_columns or column_name in self.float_columns:
            return {
                "min": column.min(),
                "max": column.max(),
                "mean": column.mean()
            }
        return None

    def show_column_stats(self, column_name):
        stats = self.calculate_column_stats(column_name)
        if stats:
            message = f"Min: {stats['min']}, Max: {stats['max']}, Mean: {stats['mean']}"
            self.show_feedback_window(message)

    def create_search_fields(self):
        """
        Creates search fields for each column in the DataFrame.
        """
        num_cols = 4
        for i, col in enumerate(self.df.columns):
            search_label = ttk.Label(self.search_entries_frame, text=f"Search {col}:")
            search_label.grid(row=i // num_cols, column=i % num_cols * 2, sticky="e", padx=(10, 5), pady=5)
            search_entry = ttk.Entry(self.search_entries_frame)
            search_entry.grid(row=i // num_cols, column=i % num_cols * 2 + 1, sticky="we", padx=(0, 10), pady=5)
            self.search_entries[col] = search_entry

        self.search_canvas.create_window((0, 0), window=self.search_entries_frame, anchor="nw")
        self.search_entries_frame.update_idletasks()
        self.search_canvas.config(scrollregion=self.search_canvas.bbox("all"))

    def create_input_fields(self):
        """
        Creates input fields for each column in the DataFrame.
        """
        num_cols = 4
        for i, col in enumerate(self.df.columns):
            if col != "ID":  # Beispiel: "ID" ist eine Spalte, die nicht bearbeitet werden soll
                input_label = ttk.Label(self.input_entries_frame, text=f"Enter {col}:")
                input_label.grid(row=i // num_cols, column=i % num_cols * 2, sticky="e", padx=(10, 5), pady=5)
                input_entry = ttk.Entry(self.input_entries_frame)
                input_entry.grid(row=i // num_cols, column=i % num_cols * 2 + 1, sticky="we", padx=(0, 10), pady=5)
                self.input_entries[col] = input_entry

        self.input_canvas.create_window((0, 0), window=self.input_entries_frame, anchor="nw")
        self.input_entries_frame.update_idletasks()  # Für die Berechnung der Größe des Canvas-Widgets
        self.input_canvas.config(scrollregion=self.input_canvas.bbox("all"))

    def pack_search_and_input(self):
        self.search_frame.pack_forget()
        self.input_frame.pack_forget()

    def show_search_fields(self):
        self.go_button.configure(command=self.execute_search)
        self.input_frame.pack_forget()
        self.coordinate_frame.pack_forget()
        self.create_search_fields()
        self.search_frame.pack(side="top", fill="x", padx=10, pady=10)

    def execute_search(self):
        """
           Executes the search functionality based on the input provided in the search fields.
           Iterates through each search entry and its corresponding column.Filters the DataFrame
            based on the search criteria provided.
           """
        search_df = self.original_df.copy()  # Kopie der ursprünglichen Tabelle erstellen
        for column, entry in self.search_entries.items():
            word = entry.get()
            if column in self.string_columns:
                if len(word) != 0:
                    search_df = self.filter_String(self.df, word, column)
            elif column in self.integer_columns:
                if len(word) != 0:
                    search_df = self.filter_Integer(self.df, word, column)
            elif column in self.float_columns:
                if len(word) != 0:
                    search_df = self.filter_Float(self.df, word, column)

        self.df = search_df
        self.update_table()

    def show_coordinate_search(self):
        self.go_button.configure(command=self.filter_and_plot_coordinates)
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self.create_coordinate_search_fields()
        self.coordinate_frame.pack(side="top", fill="x", padx=10, pady=10)

    def create_coordinate_search_fields(self):
        """
        Creates search fields for start and end coordinates.
        """
        num_cols = 4
        coordinate_columns = ["start_lat", "start_long", "end_lat", "end_long"]
        for i, col in enumerate(coordinate_columns):
            search_label = ttk.Label(self.coordinate_entries_frame, text=f"Search {col}:")
            search_label.grid(row=i // num_cols, column=i % num_cols * 2, sticky="e", padx=(10, 5), pady=5)
            search_entry = ttk.Entry(self.coordinate_entries_frame)
            search_entry.grid(row=i // num_cols, column=i % num_cols * 2 + 1, sticky="we", padx=(0, 10), pady=5)
            self.search_entries[col] = search_entry

        self.coordinate_canvas.create_window((0, 0), window=self.coordinate_entries_frame, anchor="nw")
        self.coordinate_entries_frame.update_idletasks()
        self.coordinate_canvas.config(scrollregion=self.coordinate_canvas.bbox("all"))

    def filter_and_plot_coordinates(self):
        """
        Takes input from user for coordinates and converts to float.
        """

        # check if all values are present
        if (
                not self.search_entries["start_long"].get()
                or not self.search_entries["end_long"].get()
                or not self.search_entries["start_lat"].get()
                or not self.search_entries["end_lat"].get()
        ):
            self.show_feedback_window("All four coordinate values are required.")
            return
        # convert to float and check if values are valide input
        try:
            min_x = float(self.search_entries["start_long"].get())
            max_x = float(self.search_entries["end_long"].get())
            min_y = float(self.search_entries["start_lat"].get())
            max_y = float(self.search_entries["end_lat"].get())
        except ValueError:
            self.show_feedback_window("Invalid input for coordinate values.")
            return


        self.filter_and_plot_geographic_area(self.original_df, min_x, max_x, min_y, max_y)

    def filter_and_plot_geographic_area(self, df, min_x, max_x, min_y, max_y):
        """
        Filters the DataFrame for entries that are located in a specific geographical area,
        and displays the results graphically.

        :param df: DataFrame to be filtered.
        :param min_x: Minimum x-coordinate of the geographical area (LV95).
        :param max_x: Maximum x-coordinate of the geographical area (LV95).
        :param min_y: Minimum y-coordinate of the geographical area (LV95).
        :param max_y: Maximum y-coordinate of the geographical area (LV95).
        """

        switzerland_coords = {
            'lat_0': 46.8182,
            'lon_0': 8.2275,
            'llcrnrlon': 5.9561,
            'llcrnrlat': 45.818,
            'urcrnrlon': 10.4921,
            'urcrnrlat': 47.8085,
        }
        # base map for switzerland
        m = Basemap(**switzerland_coords, projection='merc', resolution='h')

        df['start_lat'] = df['start_lat'].astype(float)
        df['end_lat'] = df['end_lat'].astype(float)
        df['start_long'] = df['start_long'].astype(float)
        df['end_long'] = df['end_long'].astype(float)

        # Filtering the DataFrame by coordinates in the geographical area
        filtered_df = df[(df['start_lat'] >= min_y) & (df['start_lat'] <= max_y) &
                         (df['start_long'] >= min_x) & (df['start_long'] <= max_x) |
                         (df['end_lat'] >= min_y) & (df['end_lat'] <= max_y) &
                         (df['end_long'] >= min_x) & (df['end_long'] <= max_x)]

        # transform coordinates into format vor base map
        x_start, y_start = m(filtered_df['start_long'].values, filtered_df['start_lat'].values)
        x_end, y_end = m(filtered_df['end_long'].values, filtered_df['end_lat'].values)

        # draw borders
        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary()

        # scatter coordinates
        m.scatter(x_start, y_start, marker='o', color='b', label='Startpunkt', zorder=5, s=0.5)
        m.scatter(x_end, y_end, marker='o', color='b', label='Endpunkt', zorder=5, s=0.5)
        fig = plt.gcf()

        # create a new window
        map_window = tk.Toplevel(self.master)
        map_window.title("Stations within the searched coordinates ")

        # convert to Tkinter Widget
        canvas = FigureCanvasTkAgg(fig, master=map_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)



    def execute_input(self):
        """
        Executes the input functionality based on the data provided in the input fields. Iterates
         through each input entry and its corresponding column.Converts the input data to
         the appropriate data type. Concatenates the input DataFrame with the original DataFrame.
        """
        df = self.df.copy()
        input_df = pd.DataFrame(columns=df.columns)
        for column, entry in self.input_entries.items():
            word = entry.get()
            if column in self.string_columns:
                if len(word) != 0:
                    input_df.loc[0, column] = word
                else:
                    input_df.loc[0, column] = np.NaN
            elif column in self.integer_columns:
                if len(word) != 0 and word.isdigit():
                    input_df.loc[0, column] = int(word)
                elif len(word) == 0:
                    input_df.loc[0, column] = np.NaN
                else:
                    self.show_feedback_window(f"Invalid input for column '{column}'. Please enter an integer value.")
                    return
            elif column in self.float_columns:
                if len(word) != 0 and (word.replace('.', '', 1).isdigit() or word.replace(',', '', 1).isdigit()):
                    input_df.loc[0, column] = float(word)
                elif len(word) == 0:
                    input_df.loc[0, column] = np.NaN
                else:
                    self.show_feedback_window(f"Invalid input for column '{column}'. Please enter a float value.")
                    return

        print(input_df)

        if input_df.isnull().values.all():
            self.show_feedback_window("Please enter values for at least one column.")
            return

        self.df = pd.concat([df, input_df])
        self.undo_df = self.df
        self.update_table()

    def show_input_fields(self):
        self.go_button.configure(command=self.execute_input)
        self.search_frame.pack_forget()
        self.coordinate_frame.pack_forget()
        self.create_input_fields()
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

    def undo_filter(self):
        self.df = self.undo_df
        self.update_table()

    @staticmethod
    def filter_String(df, word=None, columnName=None):
        """
        :param word: wort nachdem gesucht und verglichen wird
        :param columnName: Der Column-Name in der gefiltert werden soll
        :return: gefiltertes datafram

        """
        line_df = df
        if (word != None):
            line_df = df[df[columnName] == word]

        return line_df

    @staticmethod
    def filter_Integer(df, word=None, columnName=None):
        """
        :param word: wort nachdem gesucht und verglichen wird
        :param columnName: Der Column-Name in der gefiltert werden soll
        :return: gefiltertes datafram

        """
        line_df = df
        if (word != None):
            line_df = df[df[columnName] == int(word)]

        return line_df

    @staticmethod
    def filter_Float(df, word=None, columnName=None):
        """
        :param word: wort nachdem gesucht und verglichen wird
        :param columnName: Der Column-Name in der gefiltert werden soll
        :return: gefiltertes datafram

        """
        line_df = df
        if (word != None):
            line_df = df[df[columnName] == float(word)]

        return line_df

    def show_feedback_window(self, message):
        """
        opens a feedback window which shows the user what is incorrect about the input
        :param message: indicates the type and nature of the error
        """
        feedback_window = tk.Toplevel(self.master)
        feedback_window.title("Feedback")
        feedback_label = ttk.Label(feedback_window, text=message)
        feedback_label.pack(padx=10, pady=10)





def readData():
    # silent warnings
    pd.set_option('future.no_silent_downcasting', True)
    # Read data from CSV File
    df_perronkante = pd.read_csv('./Daten/perronkante.csv', sep=';')

    # Splitting the '1_koord' and '2_koord' columns into separate columns
    start_coords = df_perronkante['1_koord'].str.split(',', expand=True)
    end_coords = df_perronkante['2_koord'].str.split(',', expand=True)

    # Renaming columns
    start_coords.columns = ['start_lat', 'start_long']
    end_coords.columns = ['end_lat', 'end_long']

    # Concatenating start and end coordinates with original DataFrame
    df_perronkante = pd.concat([df_perronkante, start_coords, end_coords], axis=1)
    df_perronkante = df_perronkante.drop(['1_koord', '2_koord'], axis='columns')

    return df_perronkante


def main():
    root = tk.Tk()
    app = TableGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()