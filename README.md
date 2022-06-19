# flake8-tkinter
Not a plugin yet, but some ideas on the possible future flake8 plugin for tkinter projects

- Forbid asterisk import: `from tkinter import *`
- Prefer to use `widget.config(property=value)` instead of `widget["property"] = value`
- Prefer to use constants from tkinter instead of text values: `button.config(state=tk.DISABLED)` instead of `button.config(state="disabled")`
- ...
