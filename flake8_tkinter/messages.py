messages = {
    102: "Calling mainloop multiple times. Calling it once is enough.",
    111: "Calling `{handler}()` instead of passing the reference to `{argument}`. Perhaps you meant `{meant}` (without the parentheses)?",
    112: "Calling `{handler}()` with arguments instead of referencing it for `{argument}`. Use a lambda or functools.partial to pass arguments to the handler.",
    131: "Do not assign `.{func}()` to a variable. Since `{func}` has no return value, the variable will be None, not the widget object itself.",
    141: "Using {bind_method} without `add=True` will overwrite any existing bindings to this sequence on this widget. Either overwrite them explicitly with `add=False` or use `add=True` to keep existing bindings.",
    142: "Creating bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later.",
    201: "Using `from tkinter import *` is a bad practice. Use `import tkinter as tk` or simply `import tkinter` instead.",
    202: "Using `from tkinter.ttk import *` is a bad practice. Use `from tkinter import ttk` instead.",
    211: "Using `import tkinter.ttk as ttk` is pointless. Use `from tkinter import ttk` instead.",
    221: "Using `tkinter.{constant}` is pointless. Use an appropriate Python boolean instead.",
    251: "Using `tkinter.Message` widget. It's redundant since `tkinter.Label` provides the same functionality.",
    304: "Value for `add` should be a boolean.",
    504: "Do not use tkinter constants. Use a string literal instead ('{value}').",
}


class Error:
    def __init__(self, id: int, line: int, col: int, **kwargs):
        self.line = line
        self.col = col
        self.msg = f"TK{id} {messages[id].format(**kwargs)}"
