# flake8-tkinter

A flake8 plugin that helps you detect (too) common mistakes and bad practices in you Tkinter project

_Project idea by [@insolor](https://github.com/insolor)_


## Installation

```
pip install flake8-tkinter
```


## List of warnings

Common mistakes
- **`TK102`**: Using multiple mainloop calls is unnecessary. One call is perfectly enough. ([example](#tk102))
- **`TK111`**: Calling `callback_handler()` instead of passing the reference for on-click or binding callback. ([example](#tk111))
- **`TK112`**: Calling `callback_handler()` with arguments instead of passing the reference for on-click or binding callback. If you need to call `callback_handler` with arguments, use lambda or functools.partial. ([example](#tk112))
- **`TK131`**: Assigning result of geometry manager call to a variable. ([example](#tk131))

Best practices
- **`TK201`**: Using `from tkinter import *` is generally a bad practice and discouraged. Use `import tkinter as tk` or simply `import tkinter` instead. ([example](#tk201))
- **`TK202`**: Using `from tkinter.ttk import *` is generally a bad practice and discouraged. Use `from tkinter import ttk` instead. ([example](#tk202))
- **`TK211`**: Using `import tkinter.ttk as ttk` is pointless. Use `from tkinter import ttk` instead. ([example](#tk211))
- **`TK221`**: Using tkinter.TRUE, tkinter.FALSE, etc. is pointless. Use an appropriate Python boolean instead. ([example](#tk221))
- **`TK231`**: Using bind without `add=True` will overwrite any existing bindings to this sequence on this widget. Either overwrite them explicitly with `add=False` or use `add=True` to keep existing bindings. ([example](#tk231))
- **`TK232`**: Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later. ([example](#tk232))

Opinionated warnings
- **`TK304`**: Value for `add` should be a boolean. ([example](#tk304))

## Examples

### TK102
```python
# Bad
def foo():
    top = tk.Toplevel()
    ...
    top.mainloop()

root.mainloop()

# Good
def foo():
    top = tk.Toplevel()
    ...
    
root.mainloop()
```

### TK111
```python
# Bad
tk.Button(..., command=foo())
button.config(command=bar())
button.bind("<Button-3>", baz())

# Good
tk.Button(..., command=foo)
button.config(command=bar)
button.bind("<Button-3>", baz)
```

### TK112
```python
# Bad
tk.Button(..., command=foo(arg, kwarg=...))
button.config(command=bar(arg, kwarg=...))
button.bind("<Button-3>", baz(arg, kwarg=...))

# Good
tk.Button(..., command=lambda: foo(arg, kwarg=...))
button.config(command=lambda: bar(arg, kwarg=...))
button.bind("<Button-3>", lambda e: baz(arg, kwarg=...))
```

### TK131
```python
# Bad
btn = tk.Button().grid()

# Good
btn = tk.Button()
btn.grid()
```

### TK201
```python
# Bad
from tkinter import *

# Good
import tkinter
# OR
import tkinter as tk
```

### TK202
```python
# Bad
from tkinter.ttk import *

# Good
from tkinter import ttk
```

### TK211
```python
# Bad
import tkinter.ttk as ttk

# Good
from tkinter import ttk
```

### TK221
```python
# Bad
w.pack(expand=tk.TRUE)
w.pack(expand=tk.FALSE)
w.pack(expand=tk.YES)
w.pack(expand=tk.NO)
w.pack(expand=tk.ON)
w.pack(expand=tk.OFF)

# Good
w.pack(expand=True)
w.pack(expand=False)
```

### TK231
_Will be renamed to TK141 in v1.0.0_
```python
# Bad
w.bind("<Button-1>", foo)

# Good
w.bind("<Button-1>", foo, add=True)
# OR
w.bind("<Button-1>", foo, add=False)
```

### TK232
_Will be renamed to TK142 in v1.0.0_
```python
# Bad
for index, foo in enumerate(foos):
    w.tag_bind(f"bar_{index}", "<Button-1>", baz)
    
# Good
for index, foo in enumerate(foos):
    tcl_command = w.tag_bind(f"bar_{index}", "<Button-1>", baz)
    bindings.append(tcl_command)  # Clean them up later with `.deletecommand()`
```

### TK304
```python
# Bad
w.bind("<Button-1>", foo, add="+")

# Good
w.bind("<Button-1>", foo, add=True)
```

## Planned warnings

- Common mistakes (TK101-TK179)
    - `TK101`: Using multiple `tkinter.Tk` instances. Child windows must be created from `tkinter.Toplevel`.
    - `TK103`: Suggest refactoring code that uses `.update()`, as it's usually pointless, [potentially harmful](https://wiki.tcl-lang.org/page/Update+considered+harmful), and considered a code smell.
    - `TK113`: Callback handler should be a callable ([lol](https://www.reddit.com/r/Tkinter/comments/w84lt0/does_tkinter_button_command_only_accept_functions))
    - `TK121`: Using `time.sleep()` in tkinter code. Use `.after()` in some form instead.
    - `TK122`: Using an infinite loop in callback handler. Propose to use recursive function with `.after()`.
    - `TK141`: Suggest keeping reference of local `PhotoImage` instance to avoid GC.

- Cross platform (TK181-TK199)
    - `TK181`: Using `<Shift-Tab>` binding. It doesn't work on Linux.

- Best practices (TK201-TK299)
    - `TK222`: Using `tk.N+tk.S+tk.E+tk.W` and combinations like that. Use `tk.NSEW`, or some other constant instead.
    - `TK241`: Creating a widget without parent specified, and there is a container in the same scope.
    - `TK251`Using `tkinter.Message` widget. It's redundant since `tkinter.Label` provides the same functionality.
    - `TK261`Using subsequent `wm_attributes` calls. It can take value pairs.

- Code quality (TK301-TK399)
    - `TK301`: Suggest using more clear binding sequences, like `<Button-1>` instead of `<1>` and `<Key-a>` instead of `<a>`.
    - `TK302`: Suggest using more clear `tkinter.Text` indexes, like `end - 1 chars` instead of `end-1c`.
    - `TK303`: Using a float as `tkinter.Text` index. It works because how Tkinter translates Python objects to Tcl, but it shouldn't.

- OO (TK401-TK499)
    - `TK401`: Consider refactoring a huge app with OOP.
    - `TK402`: Consider refactoring widget into separate class.
    
- Opinionated rules (TK501-TK599)
    - `TK501`: Calling `mainloop()` on something other than the root window.
    - `TK502`: Using things like `root.wm_title()`. Use `root.title()`. (But there should be exceptions, like `wm_attributes`)
    - `TK503`: Using subscripting for widget cget and configure. Use `.cget()` and `.configure()` instead.
    - `TK504`: Using a tkinter constant. Use a string literal instead (should disabled by default)    


## Development
1. Clone the repo
2. Set up a virtual environment, activate, and install `flake8` and `pytest` in it
3. Run `pip install -e .` to install `flake8-tkinter` in editable format
4. Run `python3 -m pytest` to test your changes
