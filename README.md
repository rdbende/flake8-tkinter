# flake8-tkinter
Not a plugin yet, but some ideas on the possible future flake8 plugin for tkinter projects

- Prefer to use `import tkinter` or `import tkinter as tk` instead of asterisk import: `from tkinter import *`
- Prefer to use `widget.config(property=value)` instead of `widget["property"] = value`
- Prefer to use constants from tkinter instead of text values: `button.config(state=tk.DISABLED)` instead of `button.config(state="disabled")`
- Warn if result of `.pack()`/`.grid()`/`.place()` call (`None`) is stored in a variable
- ...
