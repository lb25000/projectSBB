import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np



class TableGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Table GUI")
        self.master.geometry("800x400")  # Größe der GUI anpassen

        # DataFrame einlesen
        self.df = readData()

        #copy original df, to have a backup
        self.original_df = self.df.copy()

        #copy original df to undo filters
        self.undo_df = self.original_df.copy()

        #definition of numeric and string columns

        self.integer_columns = ["Linie", "Didok-Nummer", "IPID", "FID", "BPUIC"]
        self.float_columns = ["KM", "Perronkantenlänge", "GO_IPID"]
        self.string_columns = ["Abkuerzung Bahnhof", "Haltestellen Name", "Perrontyp", "Perron Nummer",
                                "Kundengleisnummer", "Perronkantenhöhe", "Bemerkung Höhe", "Hilfstritt"
                                "Höhenverlauf", "Material", "Bemerkung Material", "Kantenart", 
                                "Bemerkung Kantenkrone", "Auftritt", "lod", "start_lon", "start_lat",
                                "end_lon", "end_lat"]


        # Frame für die Tabelle
        self.table_frame = ttk.Frame(master)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Style für die Tabelle anpassen, um Linien zwischen den Zellen anzuzeigen
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25, foreground="black", background="white")
        style.configure("Treeview.Heading", font=('Helvetica', 10), foreground="black", background="#eaeaea",
                        relief="raised")
        style.map("Treeview", background=[('selected', '#347083')])
        #style.layout("Treeview.Row", [('Treeview.Cell', {'sticky': 'nswe'})])  # Linien zwischen den Zellen anzeigen


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


        # Packen der Suchfelder und Eingabefelder
        self.pack_search_and_input()


    def update_table(self):
        # Entfernen aller Zeilen aus der Tabelle
        for row in self.table.get_children():
            self.table.delete(row)

        # Wieder einfügen der Zeilen entsprechend des aktualisierten DataFrames
        self.insert_table_rows()

    def insert_table_rows(self):
        for i, row in self.df.iterrows():
            row = row.fillna('')
            self.table.insert("", "end", values=list(row))

    def create_search_fields(self):
        num_cols = 4  # Anzahl der Spalten für die Suchfelder
        for i, col in enumerate(self.df.columns):
            search_label = ttk.Label(self.search_entries_frame, text=f"Search {col}:")
            search_label.grid(row=i // num_cols, column=i % num_cols * 2, sticky="e", padx=(10, 5), pady=5)
            search_entry = ttk.Entry(self.search_entries_frame)
            search_entry.grid(row=i // num_cols, column=i % num_cols * 2 + 1, sticky="we", padx=(0, 10), pady=5)
            self.search_entries[col] = search_entry

        self.search_canvas.create_window((0, 0), window=self.search_entries_frame, anchor="nw")
        self.search_entries_frame.update_idletasks()  # Für die Berechnung der Größe des Canvas-Widgets
        self.search_canvas.config(scrollregion=self.search_canvas.bbox("all"))

    def create_input_fields(self):
        num_cols = 4  # Anzahl der Spalten für die Eingabefelder
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
        # Suchfelder packen
        self.search_frame.pack_forget()

        # Eingabefelder packen
        self.input_frame.pack_forget()

    def show_search_fields(self):
        self.go_button.configure(command=self.execute_search)
        self.input_frame.pack_forget()
        self.create_search_fields()
        self.search_frame.pack(side="top", fill="x", padx=10, pady=10)

    def execute_search(self):
        # Suchfunktion ausführen
        search_df = self.original_df.copy()  # Kopie der ursprünglichen Tabelle erstellen
        for column, entry in self.search_entries.items():
            word = entry.get()
            if column in self.string_columns:
                if len(word)!=0: 
                    search_df = self.filter_String(self.df, word, column)
            elif column in self.integer_columns:
                if len(word)!=0: 
                    search_df = self.filter_Integer(self.df, word, column)
            elif column in self.float_columns:
                if len(word)!=0:
                    search_df = self.filter_Float(self.df, word, column)        

        self.df = search_df
        self.update_table()

    def execute_input(self):
        # Eingabefunktion ausführen
        df = self.df.copy()
        input_df = pd.DataFrame(columns=df.columns)
        for column, entry in self.input_entries.items():
            word = entry.get()
            if column in self.string_columns:
                if len(word)!=0:
                    input_df.loc[0, column]=word
                else:
                    input_df.loc[0, column] = np.NaN
            elif column in self.integer_columns:
                if len(word)!=0: 
                    input_df.loc[0, column]=int(word)
                else:
                    input_df.loc[0, column] = np.NaN
            elif column in self.float_columns:
                if len(word)!=0:
                    input_df.loc[0, column]=float(word)
                else:
                    input_df.loc[0, column] = np.NaN

        print(input_df)

        self.df = pd.concat([df, input_df])
        self.undo_df = self.df
        self.update_table()       

    def show_input_fields(self):
        self.go_button.configure(command=self.execute_input)
        self.search_frame.pack_forget()
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



def readData():
    # silent warnings
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


def main():
    root = tk.Tk()
    app = TableGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
