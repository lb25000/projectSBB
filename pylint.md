## Pylint Status am 11. May 2024
```
***- main.py:32:0: C0301: Line too long (103/100) (line-too-long)***
***- main.py:33:0: C0301: Line too long (102/100) (line-too-long)***
***- main.py:34:0: C0301: Line too long (117/100) (line-too-long)***
```
````python
self.string_columns = ["Abkuerzung Bahnhof", "Haltestellen Name", "Perrontyp", "Perron Nummer",
                               "Kundengleisnummer", "Perronkantenhöhe", "Bemerkung Höhe", "Hilfstritt"
                                                                                          "Höhenverlauf", "Material",
                               "Bemerkung Material", "Kantenart",
                               "Bemerkung Kantenkrone", "Auftritt", "lod", "start_lon", "start_lat",
                               "end_lon", "end_lat"]

````
changed to:
```python
self.string_columns = ["Abkuerzung Bahnhof", "Haltestellen Name", "Perrontyp",
                               "Perron Nummer", "Kundengleisnummer", "Perronkantenhöhe",
                               "Bemerkung Höhe", "Hilfstritt", "Höhenverlauf", "Material",
                               "Bemerkung Material", "Kantenart", "Bemerkung Kantenkrone",
                               "Auftritt", "lod", "start_lon", "start_lat",
                               "end_lon", "end_lat"]

```

- **main.py:45:0**: C0301: Line too long (113/100) (line-too-long)
- **main.py:46:0**: C0301: Line too long (109/100) (line-too-long)
- **main.py:64:0**: C0301: Line too long (121/100) (line-too-long)
- **main.py:65:0**: C0301: Line too long (122/100) (line-too-long)
- **main.py:66:0**: C0301: Line too long (136/100) (line-too-long)
- **main.py:89:0**: C0301: Line too long (101/100) (line-too-long)

***- main.py:115:0: C0303: Trailing whitespace (trailing-whitespace)***

````python
  elif frame == self.coordinate_frame:
            self.coordinate_entries_frame = ttk.Frame(canvas)
        
        entries_frame = ttk.Frame(canvas)
````
changed to
````python
   elif frame == self.coordinate_frame:
            self.coordinate_entries_frame = ttk.Frame(canvas)
        entries_frame = ttk.Frame(canvas)
````
- **main.py:153:0**: C0301: Line too long (102/100) (line-too-long)
- **main.py:164:0**: C0301: Line too long (120/100) (line-too-long)
- **main.py:199:0**: C0301: Line too long (107/100) (line-too-long)
- **main.py:201:0**: C0301: Line too long (112/100) (line-too-long)
- **main.py:216:0**: C0301: Line too long (110/100) (line-too-long)
- **main.py:218:0**: C0301: Line too long (115/100) (line-too-long)
- **main.py:222:0**: C0301: Line too long (102/100) (line-too-long)
- **main.py:237:0**: C0301: Line too long (103/100) (line-too-long)
- **main.py:413:0**: C0301: Line too long (117/100) (line-too-long)
- **main.py:416:0**: C0301: Line too long (113/100) (line-too-long)
- **main.py:421:0**: C0301: Line too long (114/100) (line-too-long)

***- main.py:448:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)***
***- main.py:462:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)***
***- main.py:476:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)***

```python
if(word != None):
```
changed to
```python
if word is not None:
```


***- main.py:521:0: C0304: Final newline missing (missing-final-newline***
```
added new line
```


***- **main.py:1:0**: C0114: Missing module docstring (missing-module-docstring)***
inserted
```python
"""
This module implements a GUI application for interacting with tabular data.
"""
```
- **main.py:10:0**: R0902: Too many instance attributes (22/7) (too-many-instance-attributes)
- **main.py:166:12**: W0612: Unused variable 'i' (unused-variable)
- **main.py:230:12**: W0612: Unused variable 'i' (unused-variable)
- **main.py:249:4**: C0116: Missing function or method docstring (missing-function-docstring)
- **main.py:250:8**: W0612: Unused variable 'change_cursor' (unused-variable)
- **main.py:265:4**: C0116: Missing function or method docstring (missing-function-docstring)
- **main.py:272:4**: C0116: Missing function or method docstring (missing-function-docstring)
- **main.py:279:4**: C0116: Missing function or method docstring (missing-function-docstring)
- **main.py:335:4**: R0913: Too many arguments (6/5) (too-many-arguments)
- **main.py:335:4**: R0914: Too many local variables (16/15) (too-many-locals)
- **main.py:392:4**: R0912: Too many branches (13/12) (too-many-branches)
- **main.py:435:4**: C0116: Missing function or method docstring (missing-function-docstring)
- **main.py:440:4**: C0103: Method name "filter_String" doesn't conform to snake_case naming style (invalid-name)
- **main.py:440:37**: C0103: Argument name "columnName" doesn't conform to snake_case naming style (invalid-name)
- 

***- main.py:448:12: C0121: Comparison 'word != None' should be 'word is not None' (singleton-comparison)***
```python
if (word != None):
```
````python
if word is not None:
````

- **main.py:454:4**: C0103: Method name "filter_Integer" doesn't conform to snake_case naming style (invalid-name)
- **main.py:454:38**: C0103: Argument name "columnName" doesn't conform to snake_case naming style (invalid-name)
- **main.py:462:12**: C0121: Comparison 'word != None' should be 'word is not None' (singleton-comparison)
- **main.py:468:4**: C0103: Method name "filter_Float" doesn't conform to snake_case naming style (invalid-name)
- **main.py:468:36**: C0103: Argument name "columnName" doesn't conform to snake_case naming style (invalid-name)
- **main.py:476:12**: C0121: Comparison 'word != None' should be 'word is not None' (singleton-comparison)
- **main.py:10:0**: R0904: Too many public methods (25/20) (too-many-public-methods)
- **main.py:493:0**: C0116: Missing function or method docstring (missing-function-docstring)
- **main.py:493:0**: C0103: Function name "readData" doesn't conform to snake_case naming style (invalid-name)
- **main.py:514:0**: C0116: Missing function or method docstring (missing-function-docstring)
- **main.py:516:4**: W0612: Unused variable 'app' (unused-variable)


-----------------------------------
Your code has been rated at 7.99/10

