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
- **`TK112`**: Calling `callback_handler()` instead of passing the reference for on-click or binding callback. If you need to call `callback_handler` with arguments, use lambda or functools.partial. ([example](#tk112))
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
```python
# Bad
w.bind("<Button-1>", foo)

# Good
w.bind("<Button-1>", foo, add=True)
# OR
w.bind("<Button-1>", foo, add=False)
```

### TK232
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

## More planned warnings

- Common mistakes
  - [x] Warn when assigning to result of `w.pack()` | `w.grid()` | `w.place()` call (`None`) (**TK131**)
  - [ ] Warn when using more than one`Tk` instance: child windows must be created from `Toplevel` class (**TK101**)
  - [x] Warn when using more than one `mainloop()` call (**TK102**)
  - [ ] Suggest using `w.after(ms)` instead of `time.sleep(s)` (**TK121**)
  - [ ] Suggest keeping reference of local `PhotoImage` instance to avoid GC (**TK141**)
  - [ ] Suggest refactoring code that uses `w.update`, as it's usually pointless, [potentially harmful](https://wiki.tcl-lang.org/page/Update+considered+harmful), and considered a code smell (**TK103**)
  - [ ] Warn when using a float as `Text` widget index (**TK132**)
  - [ ] Infinite loop in a handler - propose to use recursive function with `w.after` (**TK122**)
  - [x] Warn when calling the function inline, instead of just referencing it (**TK111**)
  - [x] Suggest using a lambda function when args are passed to inline calls (**TK112**)

- Common best practices
  - [x] Warn on `from tkinter import *`, suggest using `import tkinter` or `import tkinter as tk` instead (**TK201**)
  - [x] Warn on `from tkinter.ttk import *`, suggest using `from tkinter import ttk` instead (**TK202**)
  - [x] Warn on `import tkinter.ttk as ttk`, as `from tkinter import ttk` is simpler (**TK211**)
  - [x] Suggest changing `tk.TRUE` and `tk.FALSE` to `True` and `False`, as there's really no reason for using these constants instead of booleans (**TK221**)
  - [ ] Suggest using `tk.NSEW` instead of `tk.N+tk.S+tk.E+tk.W`, and other combinations (**TK222**)
  - [ ] A widget is created without a parent container specified, and there is a container in the same scope (`tk.Toplevel` or `tk.Frame`), or the widget is created in a method a subclass of `tk.Tk`, `tk.Toplevel` or `tk.Frame` (**TK232**)
  - [ ] Warn when a huge app isn't OO (?)
  - [x] Warn when not using `add=True` or explicit `add=False` in bindings (**TK231**)
  - [x] Warn when using `tag_bind` inside a loop, but not storing the Tcl command (can cause memory leaks later) (**TK232**)

- Opinionated suggestions
  - [ ] Suggest changing things like `root.wm_title()` to `root.title()` (tho I use `wm_attributes` quite often, probably that should be an exception) (**TK305**)
  - [ ] Warn when calling `mainloop()` on something other than the root window  (**TK303**)
  - [ ] Suggest using more clear binding sequences, like `<Button-1>` instead of `<1>` and `<Key-a>` instead of `<a>` (**TK301**)
  - [ ] Warn if a parent is not specified (?) (**TK306**)
  - [ ] Prefer to use more readable `widget.config(property=value)` instead of `widget["property"] = value` (**TK302**)
  - [ ] Suggest changing tkinter constants to string literals (this option should be disabled by default) (**TK307**)
  - [x] Warn when using `add="+"` in bindings, use a boolean instead (**TK304**)
  - [ ] Warn when using things like `end-1c`, `end - 1 chars` is much clearer
  - [ ] Report use of `tkinter.Message`


## Development
1. Clone the repo
2. Set up a virtual environment, activate, and install `flake8` and `pytest` in it
3. Run `pip install -e .` to install `flake8-tkinter` in editable format
4. Run `python3 -m pytest` to test your changes
