# flake8-tkinter

Flake8 plugin for Tkinter projects

## List of warnings
### TK001

Don't use `from tkinter import *`

```diff
- from tkinter import *
+ import tkinter
# OR
+ import tkinter as tk
```

### TK002

Don't use `from tkinter.ttk import *`

```diff
- from tkinter.ttk import *
+ from tkinter import ttk
```

### TK010

Doing `import tkinter.ttk as ttk` has no point

```diff
- import tkinter.ttk as ttk
+ from tkinter import ttk
```

### TK020

Calling a function instead of referencing it for `command` argument at some widgets

```diff
- ttk.Button(..., command=handler())
+ ttk.Button(..., command=handler)
```


### TK030

Don't use `time.sleep` in Tkinter code

```diff
- import time
- time.sleep(2)
+ tkinter.Tk().after(2000)
```

### TK040

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


## Development

1. Set up a virtual environment, activate, and install `flake8` and `pytest` in it
2. Run `pip install -e .` to install flake8-tkinter in an editable format
3. Run `pytest`


## Credits
The idea of this project is by [insolor](https://github.com/insolor)
