# Changes

Abstraction examples in code:

- The search function filter_general() accepts integers, floats with assignment operators like <= and also outputs a new dataframe. It doesnt matter if an integer, a different assignment operator or a float is given via a parameter.

- The function filter_direct() also accepts an integer or a float as a parameter and directly searches for these values depending on their types.

- The function \_calculate_column_stats() calculates statistics in the relevant integer or float column, irrespective of their types

- The function plot_map() filters the DataFrame for entries that are located in a specific geographical area, and displays the results graphically.

Decomposition:

- The function execute_search() checks the type of the user input, e.g. is it a string, float, float with assignment operator ect, and then calls subfunctions depending on the type.
  So the problem of searching for data got broken down into a type function and several search functions like filter_direct() if the word is a float or integer without assignment operators, filter_general() if it is a int or float with assignment operator and filter_string() if the word is a word(For example AD)

- instead if having one function for the Gui, we have create_table() function which creates the table, create_scrollbars_in_table() which creates the scrollbar on the table, create_buttons() which creates the buttons that we need for the user to interact with and many more.
  So we broke the whole Gui down into several small functions where each has its own tasks contributing to the whole Gui.
