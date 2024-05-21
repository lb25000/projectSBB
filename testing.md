# Units Tests

## Testing parts of the TableGUI Class

### Function: execute_search

- **Description:**
  The execute_search method is designed to filter the DataFrame based on user inputs in the search fields. It iterates through each search entry, applies the appropriate filter based on the data type, and updates the DataFrame displayed in the GUI.

- **Potential Issue:**
  The method might produce unexpected results if the user inputs invalid search terms, such as a non-numeric string for a numeric column, or leaves all search fields empty. This can cause errors or return an empty DataFrame without an appropriate message, misleading the user. Additionally, a past issue prevented the function from being called more than once, highlighting the need for a corresponding test case to detect if this bug reappears.

- **Test Cases:**
  1. **Input:** "Mou" in the "Abkuerzung Bahnhof" column. (Valid input)
     - **Expected Output:** A DataFrame with one row where "Abkuerzung Bahnhof" is "MOU".
  2. **Input:** "0 km" in the "KM" column.
     - **Expected Output:** Feedback window with informative error message
  3. **Input:** "Ziegelbrucke" in the "Haltestellen Name" column, twice!
     - **Expected Output:** No error and two times the same (filtered) df.
  4. **Input:** Leave all search fields empty. (Invalid input)
     - **Expected Output:** A feedback message indicating that at least one value should be entered.

**Note:** In this test case, `pd.testing.assert_frame_equal` is preferred over `self.assertEqual` for comparing DataFrames due to its ability to handle comparison of DataFrames with NaN values correctly.

### Function: execute_input

- **Description:**
  This function adds a new row to the DataFrame based on the user input in the input fields.

- **Potential Issue:**
  The method might produce unexpected results. For instance, entering a non-numeric string for a numeric column or providing data in an incorrect format could lead to errors or unexpected behavior. This could result in the addition of incorrect data to the DataFrame or failure to add data altogether, affecting the integrity of the application's data handling.

- **Test Cases:**
  1. **Input:** New row of valid input data provided.
     - **Expected Output:** The function correctly adds a new row to the DataFrame.
  2. **Input:** Invalid input provided ('0 km' instead of 'km')
     - **Expected Output:** The function handles invalid float input and provides feedback to the user.
  3. **Input:** Empty input provided.
     - **Expected Output:** A feedback message indicating that values for at least one column should be entered.

**Note:** In this test case, `pd.testing.assert_frame_equal` is preferred over `self.assertEqual` for comparing DataFrames due to its ability to handle comparison of DataFrames with NaN values correctly.

## Testing parts of the FilterFunction Class

### Function: filter_string

- **Description:**
  The filter_string function filters the DataFrame based on a string value provided for a specific column. It performs a case-insensitive search to match the string with the values in the specified column.

- **Potential Issue:**
  The function might produce incorrect results if the string search is not handled properly, especially in terms of case sensitivity and partial matches.

- **Test Cases:**
  1. **Input:** "Z" for the "Haltestellen Name" column. (Valid input, case-insensitive)
     - **Expected Output:** A DataFrame with all rows where "Haltestellen Name" contains "z", regardless of case (2 rows).
  2. **Input:** "mou" for the "Abkuerzung Bahnhof" column. (Valid input, case-insensitive)
     - **Expected Output:** A DataFrame with rows where "Abkuerzung Bahnhof" contains "MOU", regardless of case.
  3. **Input:** "Xyz" for the "Haltestellen Name" column. (No matches)
     - **Expected Output:** An empty DataFrame.
  4. **Input:** "" (empty string) for the "Haltestellen Name" column. (Empty input)
     - **Expected Output:** The original DataFrame without any filtering applied.

**Note:** In this test case, `pd.testing.assert_frame_equal` is preferred over `self.assertEqual` for comparing DataFrames due to its ability to handle comparison of DataFrames with NaN values correctly.

### Function: filter_integer

- **Description:**
  The filter_integer function filters the DataFrame based on an integer value provided for a specific column. It matches the exact integer value with the values in the specified column.

- **Potential Issue:**
  The function might produce incorrect results if non-integer strings are provided, or if the integer value does not exist in the column.

- **Test Cases:**
  1. **Input:** "890" for the "Linie" column. (Valid input)
     - **Expected Output:** A DataFrame with rows where "Linie" is 890.
  2. **Input:** "22" for the "Linie" column. (No matches)
     - **Expected Output:** An empty DataFrame (no entry for line 226!)
  3. **Input:** "890.0" for the "Linie" column. (Invalid input, non-integer string)
     - **Expected Output:** Value Error

**Note:** In this test case, `pd.testing.assert_frame_equal` is preferred over `self.assertEqual` for comparing DataFrames due to its ability to handle comparison of DataFrames with NaN values correctly.

## Conclusion

These unit tests help ensure that the functions `filter_string()`, `filter_integer()`, `execute_search()`, and `execute_input()` handle various input scenarios correctly and provide appropriate feedback or results for invalid inputs. By covering these test cases, we can catch potential issues early and improve the robustness of the code.

**Note:** In order to keep the effort proportionate for this project, mocking is not used.
