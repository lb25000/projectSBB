# Units Tests

## Testing parts of the TableGUI Class

### Function: execute_search

- **Description:**
  The execute_search method is designed to filter the DataFrame based on user inputs in the search fields. It iterates through each search entry, applies the appropriate filter based on the data type, and updates the DataFrame displayed in the GUI.

- **Potential Issue:**
  The method might produce unexpected results if the user inputs invalid search terms, such as a non-numeric string for a numeric column, or leaves all search fields empty. This can cause errors or return an empty DataFrame without an appropriate message, misleading the user. Additionally, a past issue prevented the function from being called more than once, highlighting the need for a corresponding test case to detect if this bug reappears.

- **Test Cases:**
  1. **Input:** "Zurich" in the "Haltestellen Name" column. (Valid input)
     - **Expected Output:** A DataFrame with one row where "Haltestellen Name" is "Zurich".
  2. **Input:** "1" in the "Linie" column. (Valid input)
     - **Expected Output:** A DataFrame with one row where "Linie" is 1.
  3. **Input:** "0.5" in the "KM" column. (Valid input)
     - **Expected Output:** A DataFrame with one row where "KM" is 0.5.
  4. **Input:** Leave all search fields empty. (Invalid input)
     - **Expected Output:** A feedback message indicating that at least one value should be entered.

### Function: execute_input

- **Description:**
  This function adds a new row to the DataFrame based on the user input in the input fields.

- **Potential Issue:**
  The method might produce unexpected results. For instance, entering a non-numeric string for a numeric column or providing data in an incorrect format could lead to errors or unexpected behavior. This could result in the addition of incorrect data to the DataFrame or failure to add data altogether, affecting the integrity of the application's data handling.

- **Test Cases:**
  1. **Input:** Valid input data provided.
     - **Expected Output:** The function correctly adds a new row to the DataFrame.
  2. **Input:** Invalid integer input provided.
     - **Expected Output:** The function handles invalid integer input and provides feedback to the user.
  3. **Input:** Invalid float input provided.
     - **Expected Output:** The function handles invalid float input and provides feedback to the user.
  4. **Input:** Empty input provided.
     - **Expected Output:** A feedback message indicating that values for at least one column should be entered.

## Testing parts of the FilterFunction Class

### Function: filter_string

- **Description:**
  The filter_string function filters the DataFrame based on a string value provided for a specific column. It performs a case-insensitive search to match the string with the values in the specified column.

- **Potential Issue:**
  The function might produce incorrect results if the string search is not handled properly, especially in terms of case sensitivity and partial matches.

- **Test Cases:**
  1. **Input:** "zu" for the "Haltestellen Name" column. (Valid input, case-insensitive)
     - **Expected Output:** A DataFrame with rows where "Haltestellen Name" contains "ZU", regardless of case.
  2. **Input:** "mou" for the "Haltestellen Name" column. (Valid input, case-insensitive)
     - **Expected Output:** A DataFrame with rows where "Haltestellen Name" contains "MOU", regardless of case.
  3. **Input:** "xyz" for the "Haltestellen Name" column. (No matches)
     - **Expected Output:** An empty DataFrame.
  4. **Input:** "" (empty string) for the "Haltestellen Name" column. (Empty input)
     - **Expected Output:** The original DataFrame without any filtering applied.

### Function: filter_integer

- **Description:**
  The filter_integer function filters the DataFrame based on an integer value provided for a specific column. It matches the exact integer value with the values in the specified column.

- **Potential Issue:**
  The function might produce incorrect results if non-integer strings are provided, or if the integer value does not exist in the column.

- **Test Cases:**
  1. **Input:** "890" for the "Linie" column. (Valid input)
     - **Expected Output:** A DataFrame with rows where "Linie" is 890.
  2. **Input:** "999" for the "Linie" column. (No matches)
     - **Expected Output:** An empty DataFrame.
  3. **Input:** "abc" for the "Linie" column. (Invalid input, non-integer string)
     - **Expected Output:** An error or exception indicating invalid input.
  4. **Input:** "" (empty string) for the "Linie" column. (Empty input)
     - **Expected Output:** The original DataFrame without any filtering applied.

## Conclusion

These unit tests help ensure that the functions `filter_string()`, `filter_integer()`, `execute_search()` and `execute_input()` handle various input scenarios correctly and provide appropriate feedback or results for invalid inputs. By covering these test cases, we can catch potential issues early and improve the robustness of the code.
