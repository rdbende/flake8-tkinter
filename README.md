# flake8-tkinter
Not a plugin yet, but some ideas on the possible future flake8 plugin for tkinter projects

- Prefer to use `import tkinter` or `import tkinter as tk` instead of asterisk import: `from tkinter import *`
- Prefer to use `widget.config(property=value)` instead of `widget["property"] = value`
- Prefer to use constants from tkinter instead of text values: `button.config(state=tk.DISABLED)` instead of `button.config(state="disabled")`
- Warn if result of `.pack()`/`.grid()`/`.place()` call (`None`) is stored in a variable
- More then one `Tk` object: child windows must be created from `Toplevel` class
- More then one `mainloop` call
- Possible problem: a function called, it's result is passed as an event handler or a command handler:  
  `tk.Button(text="Button", command=handler())` or `label.bind("<1>", handler())`
- Using of `time.sleep` - propose to use `root.after` instead
- Infinite loop in a handler (not sure yet how to identify an infinite loop) - propose to use `root.after`
- `PhotoImage` object stored only in a local variable (will be removed by the garbage collector)
- ...
