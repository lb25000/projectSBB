"""
This module initializes the application and starts the main loop.
"""
import tkinter as tk
from table_gui import TableGUI


def main():
    """
    Initialize the application and starts the main loop.
    """
    root = tk.Tk()
    TableGUI(root) #pylint: unused variable, but the Gui display does not work without the app
    root.mainloop()


if __name__ == "__main__":
    main()
