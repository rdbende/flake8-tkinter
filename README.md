# flake8-tkinter

Flake8 plugin to detect (too) common bad practices in Tkinter projects

## Rules

### `TK001`
Don't use `from tkinter import *`

```diff
- from tkinter import *
+ import tkinter
# OR
+ import tkinter as tk
```

### `TK002`
Don't use `from tkinter.ttk import *`


```diff
- from tkinter.ttk import *
+ from tkinter import ttk
```

### `TK010`
`import tkinter.ttk as ttk` is pointless

```diff
- import tkinter.ttk as ttk
+ from tkinter import ttk
```

### `TK020`

Calling a function instead of passing the reference for `command` argument

```diff
- ttk.Button(command=handler())
+ ttk.Button(command=handler)
```

### `TK030`

Don't use `time.sleep` in Tkinter code

```diff
- import time
- def foo():
-     time.sleep(2)
-     print("bar")
- foo()
+ def foo():
+     print("bar")
+ w.after(2000, foo)
```

### `TK040`

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

## Planned rules

- Common mistakes
  - [ ] Warn when assigning to result of `w.pack()` | `w.grid()` | `w.place()` call (`None`)
  - [ ] Warn when using more than one`Tk` instance: child windows must be created from `Toplevel` class (**TK050**)
  - [ ] Warn when using more than one `mainloop()` call (**TK051**)
  - [x] Suggest using `w.after(ms)` instead of `time.sleep(s)` (**TK030**) (current implementation is kind of dumb)
  - [ ] Suggest keeping reference of local `PhotoImage` instance to avoid GC
  - [ ] Warn when using `w.update`, as [Update is considered harmful](https://wiki.tcl-lang.org/page/Update+considered+harmful)
  - [ ] Warn when using a float as `Text` widget index
  - [ ] Infinite loop in a handler - propose to use recursive function with `w.after` (**TK031**)
  - [ ] Event and callback handlers (I can't remember what I meant by this sentence, lol)
  - [x] Warn when calling the function inline, instead of just referencing it (**TK020**)
  - [ ] Suggest using a lambda function when args are passed to inline calls (**TK021**)

- Common best practices
  - [x] Warn on `from tkinter import *`, suggest using `import tkinter` or `import tkinter as tk` instead (**TK001**)
  - [x] Warn on `import tkinter.ttk as ttk`, as `from tkinter import ttk` is simpler (**TK010**)
  - [ ] Prefer to use more readable `widget.config(property=value)` instead of `widget["property"] = value`
  - [x] Suggest changing `tk.TRUE` and `tk.FALSE` to `True` and `False`, as there's really no reason for using these constants instead of booleans (**TK040**)
  - [ ] Suggest using `tk.NSEW` instead of `tk.N+tk.S+tk.E+tk.W`, and other combinations (**TK041**)
  - [ ] A widget is created without a parent container specified, and there is a container in the same scope (`tk.Toplevel` or `tk.Frame`), or the widget is created in a method a subclass of `tk.Tk`, `tk.Toplevel` or `tk.Frame`
  - [ ] Warn when a huge app isn't OO (?)
  - [ ] Warn when not using `add=True` in bindings

- Opinionated suggestions
  - [ ] Suggest changing things like `root.wm_title()` to `root.title()` (tho I use `wm_` quite often)
  - [ ] Warn when calling `mainloop()` on something other than the root window (**TK052**)
  - [ ] Suggest using more clear binding sequences, like `<Button-1>` instead of `<1>` and `<Key-a>` instead of `<a>`
  - [ ] Warn if a parent is not specified (?)
  - [ ] Suggest changing tkinter constants to string literals (this option should be disabled by default) (**TK042**)
  - [ ] Warn when using `add="+"` in bindings, use a boolean instead

## Development

1. Clone the repo
2. Set up a virtual environment, activate, and install `flake8` and `pytest` in it
3. Run `pip install -e .` to install `flake8-tkinter` in editable format (re-run this command, when you made changes)
4. Run `python3 -m pytest`


## Credits
The idea of this project is by [**@insolor**](https://github.com/insolor)
