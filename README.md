# flake8-tkinter

Flake8 plugin for Tkinter projects


## Error codes
| Error code | Description |
|:-:|:-:|
| TK001 | `from tkinter import *` used; consider using `import tkinter as tk` or simply `import tkinter` |
| TK002 | `from tkinter.ttk import *` used; consider using `from tkinter import ttk` |
| TK010 | `import tkinter.ttk as ttk` used; could be simplified to `from tkinter import ttk` |
| TK020 | Inline call to `funcname` for 'command' argument at `widget`. Perhaps you meant `command=funcname` (without the parentheses)? |
| TK030 | `time.sleep(seconds)` used, since it blocks the thread and the GUI will freeze. Use the `.after(milliseconds)` method instead, which isavailable on every Tkinter widget |
| TK040 | `tkinter.DUMB_CONSTANT` used; use an appropriate built-in boolean instead |


## Development

1. Set up a virtual environment, activate, and install `flake8` and `pytest` in it
2. Run `pip install -e .` to install flake8-tkinter in an editable format
3. Run `pytest`


## Credits
The idea of this project is by [insolor](https://github.com/insolor)