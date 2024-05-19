"""
Contains utility functions such as feedback window display.
"""
import tkinter as tk
from tkinter import ttk

def show_feedback_window(self, message):
    """
    opens a feedback window which shows the user what is incorrect about the input
    :param message: indicates the type and nature of the error
    """
    feedback_window = tk.Toplevel(self.master)
    feedback_window.title("Feedback")
    feedback_label = ttk.Label(feedback_window, text=message)
    feedback_label.pack(padx=10, pady=10)
    