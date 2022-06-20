## Common mistakes
- [ ] Warn when assigning to result of `.pack()|.grid()|.place()` call (`None`)
- [ ] Warn when using more than one`Tk` instance: child windows must be created from `Toplevel` class (**TK050**)
- [ ] Warn when using more than one `mainloop()` call (**TK051**)
- [x] Suggest using `widget.after(ms)` instead of `time.sleep(s)` (**TK030**)
- [ ] Suggest keeping reference of local `PhotoImage` instance, to avoid GC
- [ ] Warn when using `root.update`, as [Update is considered harmful](https://wiki.tcl-lang.org/page/Update+considered+harmful)
- [ ] Warn when using a float as `Text` widget index
- [ ] Infinite loop in a handler - propose to use `widget.after` (**TK031**)
- [ ] Event and callback handlers
  - [x] Warn when calling the function inline, instead of just referencing it (**TK020**)
  - [ ] Suggest using a lambda function when args are passed to inline calls (**TK021**)

## Common best practices
- [x] Warn on `from tkinter import *`, suggest using `import tkinter` or `import tkinter as tk` instead (**TK001**)
- [x] Warn on `import tkinter.ttk as ttk`, as `from tkinter import ttk` is simpler (**TK010**)
- [ ] Prefer to use more readable `widget.config(property=value)` instead of `widget["property"] = value`
- [ ] Warn when calling `mainloop()` on something other than the root window (**TK052**)
- [x] Suggest changing `tk.TRUE` and `tk.FALSE` to `True` and `False`, as there are really no reason for using these constants instead of booleans (**TK040**)
- [ ] Suggest using `tk.NSEW` instead of `tk.N+tk.S+tk.E+tk.W`, and other combinations (**TK041**)
- [ ] A widget is created without a parent container specified, and there is a container in the same scope (`tk.Toplevel` or `tk.Frame`), or the widget is created in a method a subclass of `tk.Tk`, `tk.Toplevel` or `tk.Frame`
- [ ] Warn when a huge app isn't OO

## Opinionated suggestions
- [ ] Suggest changing things like `root.wm_title()` to `root.title()`
- [ ] Suggest using more clear binding sequences, like `<Button-1>` instead of `<1>` and `<Key-a>` instead of `<a>`
- [ ] Warn if a parent is not specified (?)
- [ ] Suggest changing string literals to tkinter constants, but this option is disabled by default (**TK042**)
