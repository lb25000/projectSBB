import unittest
import tkinter as tk
import pandas as pd
from library.table_gui import TableGUI

class TestTableGUI(unittest.TestCase):

    def setUp(self):
        """
        Set up a sample dataframe and a root window for testing.
        """
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the Tkinter window
        self.sample_data = {
            "Linie": [890, 226],
            'Abkuerzung Bahnhof': ['ZB', 'MOU'],
            'Haltestellen Name': ['Ziegelbrucke', 'Moutier'],
            'KM': [33.511, 0.208],
            'start_long': [9.061, 7.378],
            'start_lat': [47.1356, 47.279],
            'end_long': [9.060, 7.382],
            'end_lat': [47.1359, 47.382]
        }
        self.df = pd.DataFrame(self.sample_data)
        self.gui = TableGUI(self.root)
        self.gui.df = self.df
        self.gui.original_df = self.df.copy()
        self.gui.undo_df = self.df.copy()

    def tearDown(self):
        """
        Destroy the root window after each test.
        """
        self.root.destroy()

    # Test the execute_search method:

    def test_execute_search_valid_input(self):
        """
        Test the execute_search function with a valid input.
        """
         # Initialize input entries for testing execute_input methods
        self.gui.search_entries = {
            'Linie': tk.Entry(self.root),
            'Abkuerzung Bahnhof': tk.Entry(self.root),
            'Haltestellen Name': tk.Entry(self.root),
            'KM': tk.Entry(self.root),
            'start_long': tk.Entry(self.root),
            'start_lat': tk.Entry(self.root),
            'end_long': tk.Entry(self.root),
            'end_lat': tk.Entry(self.root)
        }
        self.gui.search_entries['Abkuerzung Bahnhof'].insert(0, 'Mou')
        self.assertEqual(len(self.gui.df), 2, 'Should be 2')
        self.gui.execute_search()

        # Check whether the df has the correct length after calling execute_search
        self.assertEqual(len(self.gui.df), 1, 'Should be 1')

        # Check whether the filted df has the correct content after calling execute_search
        self.assertEqual(self.gui.df['Abkuerzung Bahnhof'].iloc[0], 'MOU')

    def test_execute_search_invalid_input(self):
        """
        Test the execute_search function with an invalid input (correct type but inappropriate value).
        """
        self.gui.search_entries = {
            'Linie': tk.Entry(self.root),
            'Abkuerzung Bahnhof': tk.Entry(self.root),
            'Haltestellen Name': tk.Entry(self.root),
            'KM': tk.Entry(self.root),
            'start_long': tk.Entry(self.root),
            'start_lat': tk.Entry(self.root),
            'end_long': tk.Entry(self.root),
            'end_lat': tk.Entry(self.root)
        }
        self.gui.search_entries['KM'].insert(0, '0 km')
        self.gui.execute_search()
        
        # Assert that the feedback window was shown with the correct message to inform user about wrong entry
        feedback_window = self.gui.master.winfo_children()[-1]
        self.assertIn("Invalid search entry. Please check your input. Use numbers for numeric fields and letters for text fields.", 
                      feedback_window.winfo_children()[0].cget('text'))

    def test_execute_search_repeated_input(self):
        """
        Test executing the same search more than once results in the same output.
        """
        self.gui.search_entries = {
            'Linie': tk.Entry(self.root),
            'Abkuerzung Bahnhof': tk.Entry(self.root),
            'Haltestellen Name': tk.Entry(self.root),
            'KM': tk.Entry(self.root),
            'start_long': tk.Entry(self.root),
            'start_lat': tk.Entry(self.root),
            'end_long': tk.Entry(self.root),
            'end_lat': tk.Entry(self.root)
        }
        self.gui.search_entries['Haltestellen Name'].insert(0, 'Ziegelbrucke')
        self.gui.execute_search()
        result_first = self.gui.df.copy()

        self.gui.execute_search()
        result_second = self.gui.df.copy()

        pd.testing.assert_frame_equal(result_first, result_second)

    def test_search_no_entries(self):
        """
        Test the search functionality with no search entries.
        """
        self.gui.execute_search()
        
        feedback_window = self.gui.master.winfo_children()[-1]
        self.assertIn("Please enter at least one value.", feedback_window.winfo_children()[0].cget('text'))

    # Test the execute_input method:

    def test_execute_input_valid_input(self):
        """
        Test the execute_input function with valid input.
        """
        # Initialize input entries for testing execute_input methods
        self.gui.input_entries = {
            'Linie': tk.Entry(self.root),
            'Abkuerzung Bahnhof': tk.Entry(self.root),
            'Haltestellen Name': tk.Entry(self.root),
            'KM': tk.Entry(self.root),
            'start_long': tk.Entry(self.root),
            'start_lat': tk.Entry(self.root),
            'end_long': tk.Entry(self.root),
            'end_lat': tk.Entry(self.root)
        }
        self.gui.input_entries['Linie'].insert(0, '123')
        self.gui.input_entries['Abkuerzung Bahnhof'].insert(0, 'TEST')
        self.gui.input_entries['Haltestellen Name'].insert(0, 'Test Station')
        self.gui.input_entries['KM'].insert(0, '10.5')
        self.gui.input_entries['start_long'].insert(0, '8.55')
        self.gui.input_entries['start_lat'].insert(0, '47.3')
        self.gui.input_entries['end_long'].insert(0, '8.56')
        self.gui.input_entries['end_lat'].insert(0, '47.31')
        self.gui.execute_input()

        # Assert that the length of the df has updated to one more entry after execute_input was called
        self.assertEqual(len(self.gui.df), 3)
        self.assertEqual(self.gui.df['Haltestellen Name'].iloc[2], 'Test Station')

    def test_execute_input_invalid_input(self):
        """
        Test the execute_input function with invalid input.
        """
        # Initialize input entries for testing execute_input methods
        self.gui.input_entries = {
            'Linie': tk.Entry(self.root),
            'Abkuerzung Bahnhof': tk.Entry(self.root),
            'Haltestellen Name': tk.Entry(self.root),
            'KM': tk.Entry(self.root),
            'start_long': tk.Entry(self.root),
            'start_lat': tk.Entry(self.root),
            'end_long': tk.Entry(self.root),
            'end_lat': tk.Entry(self.root)
        }
        self.gui.input_entries['KM'].insert(1, '0 km')
        self.gui.execute_input()
        
        feedback_window = self.gui.master.winfo_children()[-1]
        self.assertIn("Invalid input for column 'KM'. Please enter a float value.", feedback_window.winfo_children()[0].cget('text'))

    def test_execute_input_empty_input(self):
        """
        Test the execute_input function with no input.
        """
        self.gui.execute_input()
        
        feedback_window = self.gui.master.winfo_children()[-1]
        self.assertIn("Please enter values for at least one column.", feedback_window.winfo_children()[0].cget('text'))

if __name__ == "__main__":
    unittest.main()
