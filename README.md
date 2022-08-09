# flake8-tkinter

Flake8 plugin to detect (too) common mistakes and bad practices in Tkinter projects


## List of warnings


### `TK111`
Calling a function instead of passing the reference for `command` argument

```diff
- ttk.Button(command=foo())
+ ttk.Button(command=foo)
```

### `TK201`
Don't use `from tkinter import *`

```diff
- from tkinter import *
+ import tkinter
# OR
+ import tkinter as tk
```

### `TK202`
Don't use `from tkinter.ttk import *`


```diff
- from tkinter.ttk import *
+ from tkinter import ttk
```

### `TK211`
`import tkinter.ttk as ttk` is pointless

```diff
- import tkinter.ttk as ttk
+ from tkinter import ttk
```

### `TK221`
Don't use dumb tkinter constants, use booleans instead

```diff
- w.pack(expand=tk.TRUE)
+ w.pack(expand=True)

- w.pack(expand=tk.FALSE)
+ w.pack(expand=False)

- w.pack(expand=tk.YES)
+ w.pack(expand=True)

- w.pack(expand=tk.NO)
+ w.pack(expand=False)

- w.pack(expand=tk.ON)
+ w.pack(expand=True)

- w.pack(expand=tk.OFF)
+ w.pack(expand=False)
```

### `TK231`
Use `add=True` or explicit `add=False` in bindings

```diff
- w.bind("<Button-1>, foo)
+ w.bind("<Button-1>, foo, add=True)
# OR
+ w.bind("<Button-1>, foo, add=False)
```

### `TK232`
Creating tag bindings in a loop can lead to memory leaks, because the created Tcl commands won't be cleaned up when deleting the tag

```diff
for index, foo in enumerate(foos):
-     w.tag_bind(f"bar_{index}", "<Button-1>, baz)
+     tcl_command = w.tag_bind(f"bar_{index}", "<Button-1>, baz)
+     bindings.append(tcl_command)  # Clean them up later with `.deletecommand()`
```

## More planned warnings

- Common mistakes
  - [ ] Warn when assigning to result of `w.pack()` | `w.grid()` | `w.place()` call (`None`) (**TK131**)
  - [ ] Warn when using more than one`Tk` instance: child windows must be created from `Toplevel` class (**TK101**)
  - [ ] Warn when using more than one `mainloop()` call (**TK102**)
  - [ ] Suggest using `w.after(ms)` instead of `time.sleep(s)` (**TK121**) (current implementation is kind of dumb)
  - [ ] Suggest keeping reference of local `PhotoImage` instance to avoid GC (**TK141**)
  - [ ] Suggest refactoring code that uses `w.update`, as it's usually pointless, [potentially harmful](https://wiki.tcl-lang.org/page/Update+considered+harmful), and considered a code smell (**TK103**)
  - [ ] Warn when using a float as `Text` widget index (**TK132**)
  - [ ] Infinite loop in a handler - propose to use recursive function with `w.after` (**TK122**)
  - [ ] Event and callback handlers (I can't remember what I meant by this sentence, lol)
  - [x] Warn when calling the function inline, instead of just referencing it (**TK111**)
  - [ ] Suggest using a lambda function when args are passed to inline calls (**TK112**)

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
  - [ ] Suggest changing things like `root.wm_title()` to `root.title()` (tho I use `wm_` quite often) (**TK305**)
  - [ ] Warn when calling `mainloop()` on something other than the root window  (**TK303**)
  - [ ] Suggest using more clear binding sequences, like `<Button-1>` instead of `<1>` and `<Key-a>` instead of `<a>` (**TK301**)
  - [ ] Warn if a parent is not specified (?) (**TK306**)
  - [ ] Prefer to use more readable `widget.config(property=value)` instead of `widget["property"] = value` (**TK302**)
  - [ ] Suggest changing tkinter constants to string literals (this option should be disabled by default) (**TK307**)
  - [ ] Warn when using `add="+"` in bindings, use a boolean instead (**TK304**)


## Development
1. Clone the repo
2. Set up a virtual environment, activate, and install `flake8` and `pytest` in it
3. Run `pip install -e .` to install `flake8-tkinter` in editable format
4. Run `python3 -m pytest` to test your changes


## Credits
The idea of this project is by [**@insolor**](https://github.com/insolor)
