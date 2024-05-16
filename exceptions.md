Since we process user input, we have decided to check the user input and,
if it is not valid, to give the user feedback.
We have introduced a feedback window for this purpose, which pops up if the user input is invalid.
If the user input is not valid, the function is cancelled and the user is prompted to enter a new value.
In many cases, a certain error is to be expected, e.g. wrong data type or empty input. In these cases, we use `if` statments.
If the errors are less predictable or if various errors are to be intercepted, we use `try except`.


Check for empty input and unexcepted input in `execute_search()`
````python
        all_empty = all(not entry.get() for entry in self.search_entries.values())
        if all_empty:
            self.show_feedback_window("Please enter at least one value.")
            return
````
````python
try:
except:
    self.show_feedback_window("Invalid search entry: An error occurred during search. "
                                      "Please check your input")
````

Since we allow the user to enter new data without necessarily specifying coordinates,
we check whether the coordinates are empty and also for invalide Station name in `filter_coordinates()`
````python
if filtered_df.empty:
    self.show_feedback_window("No matching stations found.")
    return
if filtered_df[['start_long', 'start_lat', 'end_long', 'end_lat']].isna().all().any():
    self.show_feedback_window("This station has no coordinates to plot.")
    return
````

Check for valide input in ` execute_input()`
````python
self.show_feedback_window(f"Invalid input for column '{column}'. Please enter an integer value.")

self.show_feedback_window(f"Invalid input for column '{column}'. Please enter a float value.")

self.show_feedback_window("Please enter values for at least one column.")
````