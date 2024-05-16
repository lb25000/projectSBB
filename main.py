"""
This module implements a GUI application for interacting with tabular data.
"""
import tkinter as tk
from tkinter import ttk
import operator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TableGUI:
    """
    User interaction is realised in this class as TableGUI.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Table GUI")
        self.master.geometry("800x400")  # Größe der GUI anpassen

        # DataFrame einlesen
        self.df = read_data()
        # copy original df, to have a backup
        self.original_df = self.df.copy()
        # copy original df to undo filters
        self.undo_df = self.original_df.copy()
        # definition of numeric and string columns
        self.integer_columns = ["Linie", "Didok-Nummer", "IPID", "FID", "BPUIC"]
        self.float_columns = ["KM", "Perronkantenlänge", "GO_IPID"]
        self.string_columns = ["Abkuerzung Bahnhof", "Haltestellen Name", "Perrontyp",
                               "Perron Nummer", "Kundengleisnummer", "Perronkantenhöhe",
                               "Bemerkung Höhe", "Hilfstritt", "Höhenverlauf", "Material",
                               "Bemerkung Material", "Kantenart", "Bemerkung Kantenkrone",
                               "Auftritt", "lod", "start_lon", "start_lat",
                               "end_lon", "end_lat"]

        # Frame for table
        self.table_frame = ttk.Frame(master)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Style für die Tabelle anpassen, um Linien zwischen den Zellen anzuzeigen
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25,
                        foreground="black", background="white")
        style.configure("Treeview.Heading", font=('Helvetica', 10), foreground="black",
                        background="#eaeaea", relief="raised")
        style.map("Treeview", background=[('selected', '#add8e6')])

        # Tabelle erstellen
        self.create_table()
        # Zeilen in der Tabelle einfügen
        self._insert_table_rows()
        # Scrollbars für die Tabelle hinzufügen
        self.create_scrollbars_in_table()
        self.search_frame = ttk.Frame(master)
        self.input_frame = ttk.Frame(master)
        self.coordinate_frame = ttk.Frame(master)
        # Canvas
        self.search_canvas = self.create_scrollable_canvas(self.search_frame)
        self.input_canvas = self.create_scrollable_canvas(self.input_frame)
        self.coordinate_canvas = self.create_scrollable_canvas(self.coordinate_frame)
        # Entries
        self.search_entries = {}
        self.input_entries = {}
        # Buttons
        self.create_buttons()
        self.pack_search_and_input()

        def change_cursor(event):
            """
            Change cursor if it is above a column that can be clicked on
            :param event:
            """
            widget = event.widget
            col = widget.identify_column(event.x)
            if col:
                col_index = int(col.replace("#", "")) - 1  # get column index
                col_name = self.df.columns[col_index]  # get column name
                if col_name in self.integer_columns or col_name in self.float_columns:
                    widget.config(cursor="hand1")
                else:
                    widget.config(cursor="")

        for col in self.df.columns:
            self.table.heading(col, text=col, command=lambda c=col: self._show_column_stats(c))
            self.table.bind("<Motion>", change_cursor, "+")



    def create_table(self):
        """
        Creates a table in the GUI.
        """
        self.table = ttk.Treeview(self.table_frame, style="Treeview")
        self.table["columns"] = list(self.df.columns)
        self.table["show"] = "headings"
        for col in self.df.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, minwidth=50, anchor="center")
        self.table.pack(side="left", fill="both", expand=True)

    def create_scrollbars_in_table(self):
        """
        Creates scrollbars in the GUI.
        """
        yscrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        yscrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        xscrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.table.xview)
        xscrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
        self.table.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

    def create_scrollable_canvas(self, frame):
        """
        Creates scrollable canvas  in the GUI.
        """
        canvas = tk.Canvas(frame)
        canvas.pack(side="left", fill="both", expand=True)

        if frame == self.search_frame:
            self.search_entries_frame = ttk.Frame(canvas)
        elif frame == self.input_frame:
            self.input_entries_frame = ttk.Frame(canvas)
        elif frame == self.coordinate_frame:
            self.coordinate_entries_frame = ttk.Frame(canvas)
        entries_frame = ttk.Frame(canvas)
        yscrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        yscrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        xscrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        xscrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
        canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        canvas.create_window((0, 0), window=entries_frame, anchor="nw")
        entries_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        return canvas

    def create_buttons(self):
        """
        Create the relevant buttons for the GUI.
        """
        button_frame = ttk.Frame(self.master)
        button_frame.pack()

        buttons = [
            ("Search", self.show_search_fields),
            ("Add", self.show_input_fields),
            ("Go", self.execute_search),
            ("Undo filters", self.undo_filter),
            ("Plot station", self.show_coordinate_search)
        ]
        for text, command in buttons:
            if text == "Go":
                self.go_button = ttk.Button(button_frame, text=text, command=command)
                self.go_button.pack(side="left", padx=5)
            else:
                button = ttk.Button(button_frame, text=text, command=command)
                button.pack(side="left", padx=5)

    def _update_table(self):
        """
        Updates the table by removing all existing rows and inserting
         rows from the updated DataFrame.
        """
        for row in self.table.get_children():
            self.table.delete(row)
        self._insert_table_rows()

    def _insert_table_rows(self):
        """
        Inserts rows (data) into the table based on the DataFrame.
        """
        for col in self.df.columns:
            self.table.heading(col, text=col, command=lambda c=col: self._show_column_stats(c))

        for i, row in self.df.iterrows():
            row = row.fillna('')
            self.table.insert("", "end", values=list(row))

    def _calculate_column_stats(self, column_name):
        """
        Calculates statistics in the relevant integer or float column.
        """
        column = self.df[column_name]
        if column_name in self.integer_columns or column_name in self.float_columns:
            return {
                "min": column.min(),
                "max": column.max(),
                "mean": column.mean()
            }
        return None

    def _show_column_stats(self, column_name):
        """
        Shows statistics of integer or float column. 
        """
        stats = self._calculate_column_stats(column_name)
        if stats:
            message = f"Min: {stats['min']}, Max: {stats['max']}, Mean: {stats['mean']}"
            self.show_feedback_window(message)

    def _create_search_fields(self):
        """
        Creates search fields for each column in the DataFrame.
        """
        num_cols = 4
        for i, col in enumerate(self.df.columns):
            search_label = ttk.Label(self.search_entries_frame, text=f"Search {col}:")
            search_label.grid(row=i // num_cols, column=i % num_cols * 2, sticky="e",
                              padx=(10, 5), pady=5)
            search_entry = ttk.Entry(self.search_entries_frame)
            search_entry.grid(row=i // num_cols, column=i % num_cols * 2 + 1,
                              sticky="we", padx=(0, 10), pady=5)
            self.search_entries[col] = search_entry

        self.search_canvas.create_window((0, 0), window=self.search_entries_frame, anchor="nw")
        self.search_entries_frame.update_idletasks()
        self.search_canvas.config(scrollregion=self.search_canvas.bbox("all"))

    def _create_input_fields(self):
        """
        Creates input fields for each column in the DataFrame.
        """
        num_cols = 4
        for i, col in enumerate(self.df.columns):
            if col != "ID":  # Beispiel: "ID" ist eine Spalte, die nicht bearbeitet werden soll
                input_label = ttk.Label(self.input_entries_frame, text=f"Enter {col}:")
                input_label.grid(row=i // num_cols, column=i % num_cols * 2, sticky="e",
                                 padx=(10, 5), pady=5)
                input_entry = ttk.Entry(self.input_entries_frame)
                input_entry.grid(row=i // num_cols, column=i % num_cols * 2 + 1,
                                 sticky="we", padx=(0, 10), pady=5)
                self.input_entries[col] = input_entry

        self.input_canvas.create_window((0, 0), window=self.input_entries_frame, anchor="nw")
        self.input_entries_frame.update_idletasks()  # Für die Berechnung der Größe des Canvas-Widgets
        self.input_canvas.config(scrollregion=self.input_canvas.bbox("all"))

    def _create_coordinate_search_fields(self):
        """
        Creates search fields for station name, used to plot coordinates.
        """
        coordinate_column = "Haltestellen Name"
        # Create and pack the label
        search_label = ttk.Label(self.coordinate_entries_frame, text=f"Search {coordinate_column}:")
        search_label.pack(side="left", padx=(10, 5), pady=5)
        # Create and pack the entry
        search_entry = ttk.Entry(self.coordinate_entries_frame)
        search_entry.pack(side="left", padx=(0, 10), pady=5)
        # Store the entry widget in the dictionary
        self.search_entries[coordinate_column] = search_entry
        # Update the canvas with the new frame
        self.coordinate_canvas.create_window((0, 0), window=self.coordinate_entries_frame, anchor="nw")
        self.coordinate_entries_frame.update_idletasks()
        self.coordinate_canvas.config(scrollregion=self.coordinate_canvas.bbox("all"))

    def pack_search_and_input(self):
        """
        Pack the search, input and coordinate frame.
        """
        self.search_frame.pack_forget()
        self.input_frame.pack_forget()
        self.coordinate_frame.pack_forget()

    def show_search_fields(self):
        """
        Show the search fields and configure the 'Go' button to execute search.
        """
        self.go_button.configure(command=self.execute_search)
        self.input_frame.pack_forget()
        self.coordinate_frame.pack_forget()
        self._create_search_fields()
        self.search_frame.pack(side="top", fill="x", padx=10, pady=10)

    def show_input_fields(self):
        """
        Show the input fields and configure the 'Go' button to execute input.
        """
        self.go_button.configure(command=self.execute_input)
        self.search_frame.pack_forget()
        self.coordinate_frame.pack_forget()
        self._create_input_fields()
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

    def show_coordinate_search(self):
        """
        Show the coordinate search fields and configure the 'Go' button to filter and plot coordinates.
        """
        self.go_button.configure(command=self.filter_coordinates)
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self._create_coordinate_search_fields()
        self.coordinate_frame.pack(side="top", fill="x", padx=10, pady=10)

    def execute_search(self):
        """
           Executes the search functionality based on the input provided in the search fields.
           Iterates through each search entry and its corresponding column.Filters the DataFrame
            based on the search criteria provided.
           """
        search_df = self.original_df.copy()
        all_empty = all(not entry.get() for entry in self.search_entries.values())
        if all_empty:
            self.show_feedback_window("Please enter at least one value.")
            return
        try:
            wordop = None
            for column, entry in self.search_entries.items():
                word = entry.get()
                #print(word[0:1])
                if word[0:1].isdigit():
                    search_df = self.filter_Direct(self.df, word, column)
                else:
                    if word[1:2] != '=':
                        if not word[0:1].isalpha():
                            wordop = word[:1]
                            word = word[1:]
                        else:
                            word = word
                    else:
                        wordop = word[:2]
                        word = word[2:]
                    if column in self.string_columns:
                        if len(word) != 0:
                            search_df = self.filter_string(self.df, word, column)
                    else:
                        if len(word) != 0:
                            search_df = self.filter_general(self.df, first_operator=wordop,
                                                            first_number=word, column_name=column)
        except:
            self.show_feedback_window("Invalid search entry: An error occurred during search. "
                                      "Please check your input")
            return
        self.df = search_df
        self._update_table()

    def filter_coordinates(self):
        """
        Takes input from user for coordinates and converts to float.
        """
        station_name = self.search_entries["Haltestellen Name"].get()
        filtered_df = self.df[self.df["Haltestellen Name"] == station_name]
        #check user input
        if filtered_df.empty:
            self.show_feedback_window(f"No matching stations with name {station_name} found.")
            return
        if filtered_df[['start_long', 'start_lat', 'end_long', 'end_lat']].isna().all().any():
            self.show_feedback_window("This station has no coordinates to plot.")
            return
        filtered_df.loc[:, 'start_long'] = filtered_df['start_long'].astype(float)
        filtered_df.loc[:, 'start_lat'] = filtered_df['start_lat'].astype(float)
        filtered_df.loc[:, 'end_long'] = filtered_df['end_long'].astype(float)
        filtered_df.loc[:, 'end_lat'] = filtered_df['end_lat'].astype(float)
        print(filtered_df)
        self.plot_map(filtered_df, station_name)

    def plot_map(self, df, station_name):
        """
        Filters the DataFrame for entries that are located in a specific geographical area,
        and displays the results graphically.

        :param df: DataFrame to be filtered.
        :param min_x: Minimum x-coordinate of the geographical area (LV95).
        :param max_x: Maximum x-coordinate of the geographical area (LV95).
        :param min_y: Minimum y-coordinate of the geographical area (LV95).
        :param max_y: Maximum y-coordinate of the geographical area (LV95).
        """

        # base map for switzerland
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
        # draw borders
        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary()
        # transform coordinates into format vor base map
        x_start, y_start = m(df['start_long'].values, df['start_lat'].values)
        x_end, y_end = m(df['end_long'].values, df['end_lat'].values)
        # Scatter start and end coordinates
        m.scatter(x_start, y_start, marker='o', color='b', label=station_name, zorder=5, s=5)
        m.scatter(x_end, y_end, marker='o', color='b', label=station_name, zorder=5, s=5)
        # Calculate the center of the point cloud
        x_center = (x_start.mean() + x_end.mean()) / 2
        y_center = (y_start.mean() + y_end.mean()) / 2
        # Add station_name as label for the center of the point cloud
        plt.text(x_center, y_center, station_name, fontsize=8, ha='center', color='black')
        fig = plt.gcf()
        # create a new window
        map_window = tk.Toplevel(self.master)
        map_window.title(station_name)
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
        self._update_table()


    def undo_filter(self):
        """
        Reverts the DataFrame to its state before any filtering operations.
        """
        self.df = self.undo_df
        self._update_table()

    @staticmethod
    def filter_string(df, word=None, column_name=None):
        """
        :param word: word to be searched and compared
        :param column_name: The column name to filter on
        :return: filtered dataframe
        """
        line_df = df
        if word is not None:
            line_df = df[df[column_name] == word]

        return line_df

    @staticmethod
    def filter_integer(df, word=None, column_name=None):
        """
        :param word: Word to be searched and compared
        :param column_name: The column name to filter on
        :return: Filtered dataframe
        """
        line_df = df
        if word is not None:
            line_df = df[df[column_name] == int(word)]

        return line_df

    @staticmethod
    def filter_float(df, word=None, column_name=None):
        """
        :param word: wort nachdem gesucht und verglichen wird
        :param column_name: Der Column-Name in der gefiltert werden soll
        :return: gefiltertes datafram

        """
        line_df = df
        if word is not None:
            line_df = df[df[column_name] == float(word)]

        return line_df
    
    @staticmethod
    def filter_Direct(df, word=None, column_name=None):
        """
        :param word: Word to search for and compare
        :param column_name: The column name to filter on
        :return: Filtered dataframe
        """
        if word.isdigit():
            word = int(word)
        else:
            word = float(word)
        line_df = df
        if word is not None:
            line_df = df[df[column_name] == word]

        return line_df

    @staticmethod
    def filter_general(df, first_operator=None, first_number=None, second_operator=None, second_number=None, column_name=None):
        """
        :param first_operator: erster assignment operator nach dem gefiltert wird. Z.B >=
        :param first_number: erste grösse nachdem gefiltert wird, z.b. 200
        :param second_operator: zweiter assignment operator nach dem gefiltert wird. Z.B <
        :param second_number: zweite grösse nachdem gefiltert wird, z.b. 400
        :param column_name: Der Column-Name in der gefiltert werden soll
        :return: gefiltertes dataframe
        """
        ops = {
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        '!=': operator.ne,
        ">=": operator.ge,
        ">": operator.gt
        } 
        if first_number.isdigit():
            first_number = int(first_number)
        else:
            first_number = float(first_number)
        #print(firstOperator)
        #print(firstNumber)
        line_df = df
        if first_operator is not None and second_number is None:
            line_df = line_df[ops[first_operator](line_df[column_name], first_number)]
        if first_operator is not None and second_number is not None:
            line_df = line_df[(ops[first_operator](line_df[column_name], first_number))
                              & (ops[second_operator](line_df[column_name], second_number))]
            
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



def read_data():
    """
    Reads tabular data from a CSV file and preprocesses it for further use.
    Returns: pandas.DataFrame: A DataFrame containing the read data with processed coordinates.
    """
    pd.set_option('future.no_silent_downcasting', True)
    df_perronkante = pd.read_csv('./Daten/perronkante.csv', sep=';')
    # Splitting the '1_koord' and '2_koord' columns into separate columns
    start_coords = df_perronkante['1_koord'].str.split(',', expand=True)
    end_coords = df_perronkante['2_koord'].str.split(',', expand=True)
    start_coords.columns = ['start_lat', 'start_long']
    end_coords.columns = ['end_lat', 'end_long']
    df_perronkante = pd.concat([df_perronkante, start_coords, end_coords], axis=1)
    df_perronkante = df_perronkante.drop(['1_koord', '2_koord'], axis='columns')
    return df_perronkante


def main():
    root = tk.Tk()
    app = TableGUI(root) #pylint: unused variable, but the Gui display does not work without the app
    root.mainloop()


if __name__ == "__main__":
    main()
