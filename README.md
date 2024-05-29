# SBB Railway Network Reporting Tool

## What

This project is a reporting tool created to analyze the platform edges around the SBB railway network.
The data are provided by SBB and can be downloaded [here](https://data.sbb.ch/explore/dataset/perronkante/export/) .

The tool allows users to perform data manipulation, input new information, and visualize the dataset.

## For Whom and Why

This reporting tool is designed for all stakeholders who need to analyze and understand the data related
to platform edges around the SBB railway network. By providing a user-friendly interface for data manipulation
and visualization, this tool aims to make the analysis process more efficient and insightful.

## What Makes This Project Special

- **Visualisation:** The tool provides a good visualisation to enhance the understanding of the data.
- **Dynamic Visualization:** Users can dynamically select the information they want to visualize, making the analysis process more flexible and interactive.

## Prerequisites
Please consult the [requirements.txt](requirements.txt). 
If you are using a python version older than version 3, please install Tkinter first.

````python
pip install tk
````

To install the necessary dependencies, run:

```python
pip install -r requirements.txt
```

or for newer versions:

```python
pip3 install -r requirements.txt
```

## How to Get Started

To start the application, run:

```python
python main.py
```

or for newer versions:

```python
python3 main.py
```

The main application window will appear, displaying the table with the data.
Use the provided buttons to interact with the data.
Move the mouse over the column headings, if the mouse becomes an index finger,
the column can be clicked on.

If a virtual environment is used, create one with the following command:

```python
python -m venv venv
```

Then activate this:

- macOS/Linux:

```python
source venv/bin/activate
```

- windows:

```python
venv\Scripts\activate
```

## How to run the tests

Stay in the root directory and run:

```python
python -m tests.filter_functions_test
```

or

```python
python -m tests.table_gui_test
```

accordingly. Change `python` to `python3` if needed.

## Further reading

For more information on how to make use of this reporting tool, see also [manual](manual.md).

## Version Control

### Coming soon

- Allow the user to edit or even delete the data
- Restrictive control over data added by users (allow only fully completed entries)
- Newly entered values are saved permanently
- Optimize the code, especially for plotting, to make it run faster.

### Version 1.1.2 - May 30, 2024
Last version of the first version. In this version, only the necessary buttons are
displayed to the user, which makes interaction easier. By clicking on the corresponding button you will land on the search, input or plot screen.
The Hide button takes you back to the start page. 
Note that if the table is filtered first and further functions are called in this state,
these refer to the filtered data set. If this is not desired, first press the undo filters button.

#### The important Features of the first version are:
#### 1. Interactive Table:
Column headers can be clicked:
If the cursor is moved over the column heading, it becomes a hand if the column can be clicked.
By clicking on the corresponding column, minimum, maximum and the average are displayed for columns with numerical values
and the distribution is shown in a histogram. For columns with categorical values, the frequency per value is displayed.
Two different hand symbols are used for these two column types. 
The "lod" column is a hyperlink. This is emphasised by the hyperlink symbol in the header on the one hand,
and on the other hand the cursor becomes an exchange symbol when it comes to the entries in this column.

#### 2. Search Function:
Pressing the search button takes you to the search view.
A separate search field is displayed for each column. The search supports search operators
such as ==, >, <. Several fields can be searched for simultaneously.
If an invalid value is entered in a search field, e.g. if a string is searched for in a numeric column,
the user is informed of the invalid value and the type of error. For more information on how to use the search function, consult [manual](manual.md).

#### 3. Add Function:
The Add button takes you to the input view.
The user can enter new stations. The values entered must correspond to the expected data type.
Incorrect entries are not recorded. The user is prompted to enter a valid data type.
The only restriction in the current version is that
no empty entries may be entered. It is therefore sufficient to fill in a single input field to
create a new entry. Later versions will only allow fully completed entries. 

#### 4. Plot Function:
The plot button displays the plot view. There are two plot options.
You can search for a "Haltestellen Name". The corresponding station is displayed on a map
of Switzerland by pressing the Go button. This may take a moment. Please be patient.
By repeating this process, several stops can be displayed on the map.
Or you can select from various charts using the drop-down menu.
These are displayed by clicking the Go button.


### Version 1.1.1 - May 23, 2024

- Improved control over data flow
- Divided the code into several classes for better clarity and maintainability
- the program terminates as soon as the tkinter window is closed
- Feature 1: columns with categorical values can be clicked on and the number per characteristic is displayed
- Feature 2: The column "lod" is now a hyperlink
- Feature 3: Cursor logic improved so that it is more intuitive what can be clicked on.

### Version 1.1.0 - May 16, 2024

- Feature 1: Display the coordinates of the stations on a map
- Feature 2: For all numerical values, the column can be clicked on and the statistics minimum, maximum and mean are displayed
- Feature 3: Control of user interaction: The user can be given feedback about incorrect information
- Feature 4: The search supports operands such as <, >, ==

### Version 1.0.0 - May 2, 2024

- Feature 1: Display the table in a GUI
- Feature 2: Search fields to search for data in the table
- Feature 3: Input fields for adding data
- Feature 4: the updated table is displayed after a search or input

### Version 0.0.0 - April 25, 2024

- initialisation of the project

## Where to find Key Resources

Data provided by SBB: <a href="https://data.sbb.ch/explore/dataset/perronkante/export/" target="_blank">https://data.sbb.ch/explore/dataset/perronkante/export/ </a>

## Licence

This project is licensed under the [MIT licence](LICENSE). Details can be found in the [LICENSE](LICENSE) file.
