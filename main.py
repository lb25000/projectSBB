"""
This module initializes the application and starts the main loop.
"""
import tkinter as tk
from library.table_gui import TableGUI

def on_closing(root):
    """
    The program is exited if tkinter window will be closed.
    """
    root.destroy()
    exit(0)

def main():
    """
    Initialize the application and starts the main loop.
    """
    root = tk.Tk()
    app = TableGUI(root) #pylint: unused variable, but the Gui display does not work without the app
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

if __name__ == "__main__":
    main()
