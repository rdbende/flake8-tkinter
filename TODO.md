- [x] Warn on `from tkinter import *`, suggest using `import tkinter` or `import tkinter as tk` instead
- [ ] Prefer to use more readable `widget.config(property=value)` instead of `widget["property"] = value`
- [ ] Warn when assigning to result of `.pack()|.grid()|.place()` call (`None`)
- [ ] Warn when using more than one`Tk` instance: child windows must be created from `Toplevel` class
- [ ] Warn when using more than one `mainloop()` call
- Event and callback handlers

  - [x] Warn when calling the function inline, instead of just passing in the name
  - [ ] Suggest using a lambda function when args are passed to inline calls

- Constants

  Imo tkinter's constants are dumb. They doesn't make the code more readable, and provide no performance improvement over using string literals. However some people prefer using it, so it could be useful here.
  My ideas are
  - [ ] Always suggest changing `tk.TRUE` and `tk.FALSE` to `True` and `False`, as there are really no reason for using these constants instead of booleans
  - [ ] Always suggest using `tk.NSEW` instead of `tk.N+tk.S+tk.E+tk.W`, and other combinations
  - [ ] Optionally suggest changing string literals to tkinter constants, but this option is disabled by default 

- [ ] Suggest using `widget.after` instead of `time.sleep`
- [ ] Suggest keeping reference of local `PhotoImage` instance, to avoid GC
- [ ] Warn when using `root.update`, as [Update is considered harmful](https://wiki.tcl-lang.org/page/Update+considered+harmful)
- [ ] Infinite loop in a handler (not sure yet how to identify an infinite loop) - propose to use root.after
- [ ] A widget is created without a parent container specified, and there is a container in the same scope (`tk.Toplevel` or `tk.Frame`), or the widget is created in a method a subclass of `tk.Tk`, `tk.Toplevel` or `tk.Frame`.

  - [ ] Strict variant: always warn if a parent is not specified.

