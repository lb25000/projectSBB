import unittest
import pandas as pd
from filter_functions import FilterFunctions

class TestFilterFunctions(unittest.TestCase):

    def setUp(self):
        """
        Set up a sample dataframe for testing.
        """
        self.sample_data = {
            "Linie": [890, 226, 330],
            'Abkuerzung Bahnhof': ['ZB', 'MOU', 'ZU'],
            'Haltestellen Name': ['Ziegelbrucke', 'Moutier', 'Zuerich'],
            'KM': [33.511, 0.208, 1.123],
            'start_long': [9.061, 7.378, 8.541],
            'start_lat': [47.1356, 47.279, 47.377],
            'end_long': [9.060, 7.382, 8.543],
            'end_lat': [47.1359, 47.382, 47.380]
        }
        self.df = pd.DataFrame(self.sample_data)

    def test_filter_string(self):
        """
        Test the filter_string function.
        """
        result = FilterFunctions.filter_string(self.df, 'zu', 'Haltestellen Name')
        expected_result = self.df[self.df['Haltestellen Name'].str.upper().str.contains('ZU')]
        pd.testing.assert_frame_equal(result, expected_result)

    def test_filter_string_case_insensitive(self):
        """
        Test the filter_string function with case insensitivity.
        """
        result = FilterFunctions.filter_string(self.df, 'mou', 'Haltestellen Name')
        expected_result = self.df[self.df['Haltestellen Name'].str.upper().str.contains('MOU')]
        pd.testing.assert_frame_equal(result, expected_result)

    def test_filter_string_no_matches(self):
        """
        Test the filter_string function with no matches.
        """
        result = FilterFunctions.filter_string(self.df, 'xyz', 'Haltestellen Name')
        expected_result = self.df[self.df['Haltestellen Name'].str.upper().str.contains('XYZ')]
        self.assertTrue(expected_result.empty)
        self.assertTrue(result.empty)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_filter_integer(self):
        """
        Test the filter_integer function.
        """
        result = FilterFunctions.filter_integer(self.df, '890', 'Linie')
        expected_result = self.df[self.df['Linie'] == 890]
        pd.testing.assert_frame_equal(result, expected_result)

    def test_filter_integer_no_matches(self):
        """
        Test the filter_integer function with no matches.
        """
        result = FilterFunctions.filter_integer(self.df, '999', 'Linie')
        expected_result = self.df[self.df['Linie'] == 999]
        self.assertTrue(expected_result.empty)
        self.assertTrue(result.empty)
        pd.testing.assert_frame_equal(result, expected_result)

if __name__ == "__main__":
    unittest.main()
