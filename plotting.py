"""
Handles plotting functions.
"""
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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