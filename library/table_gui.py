"""
This module implements a GUI application for interacting with tabular data.
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import os
from library.data_loader import read_data
from library.filter_functions import FilterFunctions
from library.plotting import plot_map, plot_histogram, plot_correlation
from library.utils import show_feedback_window

class TableGUI:
    """
    User interaction is realised in this class as TableGUI.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Table GUI")
        self.master.geometry("800x400")  # Adjust the size of the GUI

        # Set the path for the hyperlink icon
        icon_path = os.path.join("image", "hyperlink.png")

        # Load and resize the hyperlink icon using PIL
        self.hyperlink_icon = Image.open(icon_path)
        self.hyperlink_icon = self.hyperlink_icon.resize((18, 18))  # Change size as needed
        self.hyperlink_icon = ImageTk.PhotoImage(self.hyperlink_icon)

        # Read DataFrame
        self.df = read_data()
        # copy original df, to have a backup
        self.original_df = self.df.copy()
        # copy original df to undo filters
        self.undo_df = self.original_df.copy()
        # dynamically determine column types and define numeric and string columns
        column_types = self.df.dtypes
        self.integer_columns = column_types[column_types == 'int64'].index.tolist()
        self.float_columns = column_types[column_types == 'float64'].index.tolist()
        self.string_columns = column_types[column_types == 'object'].index.tolist()

        # Frame for table
        self.table_frame = ttk.Frame(master)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Customise style for the table to display lines between the cells
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25,
                        foreground="black", background="white")
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), foreground="grey",
                        background="#eaeaea", relief="raised")
        style.map("Treeview", background=[('selected', '#add8e6')])

        # Create table
        self.create_table()
        # Insert rows in the table
        self._insert_table_rows()
        # Add scrollbars for the table
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
        # Bind events to the table
        for col in self.df.columns:
            self.table.heading(col, text=col, command=lambda c=col: self._show_column_stats(c))

        # Bind the hyperlink click event
        self.table.bind("<Button-1>", self.on_click)
        # Bind the motion event for changing cursor
        self.table.bind("<Motion>", self.change_cursor)

    def change_cursor(self, event):
        """
        Change cursor if it is above a column that can be clicked on
        :param event: mouse hovers over a column name
        """
        widget = event.widget
        col = widget.identify_column(event.x)
        row = widget.identify_row(event.y)
        current_cursor = widget.cget("cursor")

        new_cursor = self.get_new_cursor(col, row)

        if new_cursor != current_cursor:
            widget.config(cursor=new_cursor)

    def get_new_cursor(self, col, row):
        """
        Get the new cursor based on column and row
        :param col: column identifier
        :param row: row identifier
        :return: new cursor
        """
        if col and not row:
            col_index = int(col.replace("#", "")) - 1  # get column index
            col_name = self.df.columns[col_index]  # get column name
            if (col_name in self.integer_columns or col_name in self.float_columns)\
                    and col_name not in ['GO_IPID', 'IPID', 'FID', 'Didok-Nummer', 'BPUIC']:
                return 'hand1'
            if col_name in ['Perrontyp', 'Hilfstritt', 'Material',
                            'Höhenverlauf', 'Kantenart', 'Auftritt']:
                return 'hand2'
        elif row and col:
            col_index = int(col.replace("#", "")) - 1  # get column index
            col_name = self.df.columns[col_index]  # get column name
            if col_name == 'lod':
                return 'exchange'  # Set cursor to 'hand1' for 'lod' entries
        return ''  # default cursor for other columns


    def create_table(self):
        """
        Creates a table in the GUI.
        """
        self.table = ttk.Treeview(self.table_frame, style="Treeview")
        self.table["columns"] = list(self.df.columns)
        self.table["show"] = "headings"
        for col in self.df.columns:
            if col == 'lod':
                self.table.heading(col, text=col, image=self.hyperlink_icon, anchor='center')
            else:
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

        self.search_button = ttk.Button(button_frame, text="Search", command=self.show_search_fields)
        self.search_button.pack(side="left", padx=5)

        self.add_button = ttk.Button(button_frame, text="Add", command=self.show_input_fields)
        self.add_button.pack(side="left", padx=5)

        self.plot_button = ttk.Button(button_frame, text="Plot", command=self.show_coordinate_and_relation_search)
        self.plot_button.pack(side="left", padx=5)

        self.go_button = ttk.Button(button_frame, text="Go", command=self.execute_search)

        self.hide_button = ttk.Button(button_frame, text="Hide", command=self.hide_frame)

        self.undo_button = ttk.Button(button_frame, text="Undo filters", command=self.undo_filter)
        self.undo_button.pack(side="left", padx=5)


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
        if (column_name in self.integer_columns or column_name in self.float_columns)\
                and column_name not in ['GO_IPID', 'IPID', 'FID', 'Didok-Nummer', 'BPUIC']:
            return {
                "min": column.min(),
                "max": column.max(),
                "mean": round(column.mean(), 3)
            }
        return None

    def _show_column_stats(self, column_name):
        """
        Shows statistics of columns. 
        """
        if column_name in ['Perrontyp', 'Hilfstritt', 'Material',
                            'Höhenverlauf', 'Kantenart', 'Auftritt']:
            self._show_value_counts(column_name)
        else:
            stats = self._calculate_column_stats(column_name)
            if stats:
                message = f"Min: {stats['min']}, Max: {stats['max']}, Mean: {stats['mean']}"
                show_feedback_window(self, message)

                # histogram
                plot_histogram(self, column_name)

    def _show_value_counts(self, column_name):
        """
        Show frequency of values in categorical columns
        :param column_name: name of selected column
        """
        counts = self.df[column_name].value_counts()
        total_count = counts.sum()
        relative_percentages = ((counts / total_count) * 100).round(2).astype(str) + '%'
        message = "Absolute frequencies:\n{}\n\nRelative percentages:\n{}".format(counts.to_string(),
                                                                                  relative_percentages.to_string())
        show_feedback_window(self, message)

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
            if col != "ID":  # Example: "ID" is a column that should not be edited
                input_label = ttk.Label(self.input_entries_frame, text=f"Enter {col}:")
                input_label.grid(row=i // num_cols, column=i % num_cols * 2, sticky="e",
                                 padx=(10, 5), pady=5)
                input_entry = ttk.Entry(self.input_entries_frame)
                input_entry.grid(row=i // num_cols, column=i % num_cols * 2 + 1,
                                 sticky="we", padx=(0, 10), pady=5)
                self.input_entries[col] = input_entry

        self.input_canvas.create_window((0, 0), window=self.input_entries_frame, anchor="nw")
        self.input_entries_frame.update_idletasks()  # To calculate the size of the canvas widget
        self.input_canvas.config(scrollregion=self.input_canvas.bbox("all"))

    def _create_coordinate_and_relation_search_fields(self):
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

        # Create and pack the label for the second dropdown field
        relation_label = ttk.Label(self.coordinate_entries_frame, text="Select relation to be plotted:")
        relation_label.pack(side="left", padx=(10, 5), pady=5)
        
        # Create and pack the dropdown for relation selection
        self.relation_dropdown = ttk.Combobox(self.coordinate_entries_frame, values=[
            "Perronkantenlänge - Perrontyp",
            "Perronkantenlänge - Material",
            "Perronkantenlänge - Anzahl Linien pro Haltestelle",
            "Material - Hilfstritt",
            "Perronkantenlänge - KM",
            ""
        ])
        self.relation_dropdown.pack(side="left", anchor="w", padx=(0, 10), pady=5)

        # Update the canvas with the new frame
        self.coordinate_canvas.create_window((0, 0), window=self.coordinate_entries_frame,
                                             anchor="nw")
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
        self.go_button.pack(side="left", padx=5)
        self.hide_button.pack(side="left", padx=5)
        self.undo_button.pack_forget()
        self.undo_button.pack(side="left", padx=5)
        self.input_frame.pack_forget()
        self.coordinate_frame.pack_forget()
        self.search_button.pack_forget()
        self.add_button.pack_forget()
        self.plot_button.pack_forget()
        self._create_search_fields()
        self.search_frame.pack(side="top", fill="x", padx=10, pady=10)

    def show_input_fields(self):
        """
        Show the input fields and configure the 'Go' button to execute input.
        """
        self.go_button.configure(command=self.execute_input)
        self.go_button.pack(side="left", padx=5)
        self.hide_button.pack(side="left", padx=5)
        self.undo_button.pack_forget()
        self.undo_button.pack(side="left", padx=5)
        self.search_frame.pack_forget()
        self.coordinate_frame.pack_forget()
        self.search_button.pack_forget()
        self.add_button.pack_forget()
        self.plot_button.pack_forget()
        self._create_input_fields()
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

    def show_coordinate_and_relation_search(self):
        """
        Show the coordinate search fields 
        and configure the 'Go' button to filter and plot coordinates.
        """
        self.go_button.configure(command=self.filter_and_plot)
        self.go_button.pack(side="left", padx=5)
        self.hide_button.pack(side="left", padx=5)
        self.undo_button.pack_forget()
        self.undo_button.pack(side="left", padx=5)
        self.search_button.pack_forget()
        self.add_button.pack_forget()
        self.plot_button.pack_forget()
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self.coordinate_entries_frame.pack_forget()
        for widget in self.coordinate_entries_frame.winfo_children():
           widget.destroy()
        self._create_coordinate_and_relation_search_fields()
        self.coordinate_frame.pack(side="top", fill="x", padx=10, pady=10)

    def hide_frame(self):
        """
        Hides the frame like coordinate_search, input_fields, search_fields.
        """
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self.coordinate_frame.pack_forget()
        self.go_button.pack_forget()
        self.hide_button.pack_forget()
        self.undo_button.pack_forget()
        self.search_button.pack(side="left", padx=5)
        self.add_button.pack(side="left", padx=5)
        self.plot_button.pack(side="left", padx=5)
        self.undo_button.pack(side="left", padx=5)

    def execute_search(self):
        """
        Executes the search functionality based on the input provided in the search fields.
        Iterates through each search entry and its corresponding column.Filters the DataFrame
        based on the search criteria provided.
        """
        search_df = self.original_df.copy()
        all_empty = all(not entry.get() for entry in self.search_entries.values())
        if all_empty:
            show_feedback_window(self, "Please enter at least one value.")
            return
        try:
            wordop = None
            for column, entry in self.search_entries.items():
                word = entry.get()
                if word[0:1].isdigit() and column not in self.string_columns:
                    search_df = FilterFunctions.filter_direct(self.df, word, column)
                else:
                    if word[1:2] != '=':
                        if not word[0:1].isalpha():
                            wordop = word[:1]
                            word = word[1:]
                    else:
                        wordop = word[:2]
                        word = word[2:]
                    if column in self.string_columns:
                        word = entry.get()
                        if len(word) != 0:
                            if(wordop == '=='):
                                search_df = FilterFunctions.filter_assignmentString(self.df, wordop, word[2:], column )
                            else:
                                search_df = FilterFunctions.filter_string(self.df, word, column)
                    else:
                        if len(word) != 0:
                            search_df = FilterFunctions.filter_general(self.df,
                                    first_operator=wordop, first_number=word, column_name=column)
       
        except ValueError as ve:
            error_message = f"Value error: {str(ve)}. Please check your input"
            print(error_message)
            show_feedback_window(self, "Invalid search entry. Please check your input. Use numbers for numeric fields and letters for text fields.")
            
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            show_feedback_window(self, "An unexpected error occurred. Please try again later.")

        self.df = search_df
        self._update_table()

    def filter_and_plot(self):
        """
        Triggers filtering the coordinates and plotting based on user inputs.
        If the entry field for plotting the station or the realtion is empty
        the corresponding method is not called.
        """
        if self.search_entries["Haltestellen Name"].get().strip():
            self.filter_coordinates()
        if self.relation_dropdown.get().strip():
            self.plot_correlation_selected_relation()

    def filter_coordinates(self):
        """
        Takes input from user for coordinates and converts to float.
        """
        station_name = self.search_entries["Haltestellen Name"].get()
        filtered_df = self.df[self.df["Haltestellen Name"] == station_name]
        #check user input
        if filtered_df.empty:
            show_feedback_window(self, f"No matching stations with name {station_name} found.")
            return
        if filtered_df[['start_long', 'start_lat', 'end_long', 'end_lat']].isna().all().any():
            show_feedback_window(self, "This station has no coordinates to plot.")
            return
        filtered_df.loc[:, 'start_long'] = filtered_df['start_long'].astype(float)
        filtered_df.loc[:, 'start_lat'] = filtered_df['start_lat'].astype(float)
        filtered_df.loc[:, 'end_long'] = filtered_df['end_long'].astype(float)
        filtered_df.loc[:, 'end_lat'] = filtered_df['end_lat'].astype(float)
        plot_map(self, filtered_df, station_name)

    def plot_correlation_selected_relation(self):
        """
        Plot correlation based on the selected relation from the dropdown.
        """
        selected_relation = self.relation_dropdown.get()
        plot_correlation(self, selected_relation)

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
                    show_feedback_window(self,
                        f"Invalid input for column '{column}'. Please enter an integer value.")
                    return
            elif column in self.float_columns:
                if len(word) != 0 and (word.replace('.', '', 1).isdigit()
                                       or word.replace(',', '', 1).isdigit()):
                    input_df.loc[0, column] = float(word)
                elif len(word) == 0:
                    input_df.loc[0, column] = np.NaN
                else:
                    show_feedback_window(self,
                        f"Invalid input for column '{column}'. Please enter a float value.")
                    return


        if input_df.isnull().values.all():
            show_feedback_window(self, "Please enter values for at least one column.")
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


    def on_click(self, event):
        """
        Handle clicks on the 'lod' column to open URLs in a web browser.
        """
        item = self.table.identify_row(event.y)
        column = self.table.identify_column(event.x)
        col_index = int(column.replace('#', '')) - 1
        col_name = self.df.columns[col_index]

        if col_name == "lod":
            value = self.table.item(item, "values")[col_index]
            if value.startswith("http"):
                webbrowser.open(value)
