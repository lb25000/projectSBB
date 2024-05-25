"""
Handles plotting functions.
"""
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.cm import viridis

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

def plot_correlation(self, selected_relation):
        """
        Plots the correlation between two variables.
        """
        if selected_relation == "Perronkantenlänge - Perrontyp":
            plot_pieplot_perronlänge(self, "Perrontyp")
        elif selected_relation == "Perronkantenlänge - Material":
            plot_pieplot_perronlänge(self, "Material")
        elif selected_relation == "Perronkantenlänge - Anzahl Linien pro Haltestelle":
            plot_pieplot_perronlänge(self, "Number of Lines per Station")
        elif selected_relation == "Material - Hilfstritt":
            plot_barplot(self)
        elif selected_relation == "Perronkantenlänge - KM":
            plot_scatterplot(self, "KM", "Perronkantenlänge")

def plot_histogram(self, column_name):
    """
    Plots a histogram in a specific column.
    :param column_name: name of specific column to get the histogram
    """
    column_data = self.df[column_name]
    plt.figure(figsize=(8, 6))
    plt.hist(column_data, bins=50, color='skyblue', edgecolor='black')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.title(f'Histogram for {column_name}')
    plt.grid(True)
    fig = plt.gcf()
    # Create a new window
    hist_window = tk.Toplevel(self.master)
    hist_window.title(column_name)
    # Convert to Tkinter Widget
    canvas = FigureCanvasTkAgg(fig, master=hist_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def plot_barplot(self):
    """
    Plots a bar plot showing the number of 'vorhanden' entries in 'Hilfstritt' for each material.
    """
    # Filter the dataframe for rows where 'Hilfstritt' is 'vorhanden'
    filtered_df = self.df[self.df['Hilfstritt'] == 'vorhanden']
    # Group by 'Material' and count the occurrences of 'vorhanden' in 'Hilfstritt'
    material_counts = filtered_df.groupby('Material').size().reset_index(name='Count')
    # Create the bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Material', y='Count', data=material_counts, palette='viridis')
    plt.title('Number of "vorhanden" Entries in Hilfstritt for Each Material')
    plt.xlabel('Material')
    plt.ylabel('Count of "vorhanden"')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig = plt.gcf()
    # Create a new Toplevel window for the bar plot
    barplot_window = tk.Toplevel(self.master)
    barplot_window.title('Bar Plot - Hilfstritt Entries per Material')
    # Create a canvas for the figure
    canvas = FigureCanvasTkAgg(fig, master=barplot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def plot_pieplot_perronlänge(self, var):
    """
    Plots a pie plot showing the average perronkantenlänge for each entry in var.
    """
    # Add a temporary column to calculate the number of different lines per station
    if var == "Number of Lines per Station":
        # Calculate the number of different lines per station
        num_lines_per_station = self.df.groupby('Abkuerzung Bahnhof')['Linie'].nunique()
        # Add the temporary column to the DataFrame
        self.df['Number of Lines per Station'] = self.df['Abkuerzung Bahnhof'].map(num_lines_per_station)
    # Group by the number of lines per station and calculate the average 'Perronkantenlänge'
    perrontyp_avg_length = self.df.groupby(var)['Perronkantenlänge'].mean().reset_index()
    # Create the pie plot
    plt.figure(figsize=(8, 8))
    # Function to display the average Perronkantenlänge
    def average_format(value):
        return f'{value:.2f} m'
    plt.pie(perrontyp_avg_length['Perronkantenlänge'], 
            labels=perrontyp_avg_length[var], 
            autopct=average_format, 
            colors=sns.color_palette('viridis', len(perrontyp_avg_length)))
    plt.title(f'Average Perronkantenlänge per {var}')
    plt.tight_layout()
    fig = plt.gcf()
    # Create a window for the pie plot
    pieplot_window = tk.Toplevel(self.master)
    pieplot_window.title(f'Pie Plot - Average Perronkantenlänge per {var}')
    canvas = FigureCanvasTkAgg(fig, master=pieplot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def plot_scatterplot(self, var1, var2):
    """
    Plots a scatter plot showing the correlation between var1 and var2.
    """
    # Extract the relevant data
    x = self.df[var1]
    y = self.df[var2]
    # Create a figure and axis
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c=viridis(0.8))
    # Set the title and labels
    plt.title(f'Scatter Plot of {var1} vs {var2}')
    plt.xlabel(f'{var1}')
    plt.ylabel(f'{var2}')
    plt.grid(True)
    plt.tight_layout()
    # Get the current figure
    fig = plt.gcf()
    # Create a new Toplevel window for the bar plot
    scatterplot_window = tk.Toplevel(self.master)
    scatterplot_window.title(f'Scatter Plot - {var1} vs {var2}')
    # convert to Tkinter Widget
    canvas = FigureCanvasTkAgg(fig, master=scatterplot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    