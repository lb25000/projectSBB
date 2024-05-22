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

- python
- pandas
- matplotlib
- basemap
- basemap-data-hires
- tk

To install the necessary dependencies, run:

```python
pip install pandas numpy matplotlib basemap basemap-data-hires tk
```

or for newer versions:

```python
pip3 install pandas numpy matplotlib basemap basemap-data-hires tk
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

If a virtual environment is used, activate this:

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

## Version Control

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
