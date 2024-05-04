import tkinter as tk
from tkinter import ttk
import pandas as pd



class TableGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Table GUI")
        self.master.geometry("800x400")  # Größe der GUI anpassen

        # DataFrame einlesen
        self.df = readData()

        #copy original df, to habe a backup
        self.original_df = self.df.copy()
        #definition of numeric and string columns
        self.numeric_columns = ["Linie", "KM"]
        self.string_columns = ["Abkuerzung Bahnhof", "Haltestellen Name"]

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


        # Scrollbars für die Tabelle hinzufügen
        yscrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        yscrollbar.pack(side="right", fill="y")
        xscrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.table.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.table.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        # Zeilen in der Tabelle einfügen
        self.insert_table_rows()

        # Suchfelder Frame mit Canvas für Scrollbar
        self.search_frame = ttk.Frame(master)

        self.search_canvas = tk.Canvas(self.search_frame)
        self.search_canvas.pack(side="left", fill="both", expand=True)

        self.search_entries_frame = ttk.Frame(self.search_canvas)
        self.search_vscrollbar = ttk.Scrollbar(self.search_frame, orient="vertical", command=self.search_canvas.yview)
        self.search_vscrollbar.pack(side="right", fill="y")
        self.input_hscrollbar = ttk.Scrollbar(self.search_frame, orient="horizontal", command=self.search_canvas.xview)
        self.input_hscrollbar.pack(side="bottom", fill="x")
        self.search_canvas.configure(xscrollcommand=self.input_hscrollbar.set, yscrollcommand=self.search_vscrollbar.set)

        self.search_entries = {}  # Initialisierung des search_entries-Attributs

        # Eingabefelder Frame mit Canvas für Scrollbar
        self.input_frame = ttk.Frame(master)

        self.input_canvas = tk.Canvas(self.input_frame)
        self.input_canvas.pack(side="left", fill="both", expand=True)

        self.input_entries_frame = ttk.Frame(self.input_canvas)
        self.input_vscrollbar = ttk.Scrollbar(self.input_frame, orient="vertical", command=self.input_canvas.yview)
        self.input_vscrollbar.pack(side="right", fill="y")
        self.input_hscrollbar = ttk.Scrollbar(self.input_frame, orient="horizontal", command=self.input_canvas.xview)
        self.input_hscrollbar.pack(side="bottom", fill="x", expand=True)
        self.input_canvas.configure(xscrollcommand=self.input_hscrollbar.set, yscrollcommand=self.input_vscrollbar.set)

        self.input_entries = {}  # Initialisierung des input_entries-Attributs

        # Buttons
        button_frame = ttk.Frame(master)
        button_frame.pack()
        search_button = ttk.Button(button_frame, text="Search", command=self.show_search_fields)
        search_button.pack(side="left", padx=5)
        add_button = ttk.Button(button_frame, text="Add", command=self.show_input_fields)
        add_button.pack(side="left", padx=5)
        go_button = ttk.Button(button_frame, text="Go", command=self.execute_search)
        go_button.pack(side="left", padx=5)

        # Packen der Suchfelder und Eingabefelder
        self.pack_search_and_input()



    def apply_string_search_filter(self, event, column):
        print("Apply string search filter called")
        word = self.search_entries[column].get()
        self.df = self.filter_String(self.df, word, column)
        self.update_table()

    def update_table(self):
        # Entfernen aller Zeilen aus der Tabelle
        for row in self.table.get_children():
            self.table.delete(row)

        # Wieder einfügen der Zeilen entsprechend des aktualisierten DataFrames
        self.insert_table_rows()

    def insert_table_rows(self):
        for i, row in self.df.iterrows():
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
        self.input_frame.pack_forget()
        self.create_search_fields()
        self.search_frame.pack(side="top", fill="x", padx=10, pady=10)

    def execute_search(self):
        # Suchfunktion ausführen
        search_df = self.original_df.copy()  # Kopie der ursprünglichen Tabelle erstellen
        for column, entry in self.search_entries.items():
            word = entry.get()
            if column in self.string_columns:
                search_df = self.filter_String(self.df, word, column)
        self.df = search_df
        self.update_table()

    def show_input_fields(self):
        self.search_frame.pack_forget()
        self.create_input_fields()
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

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
