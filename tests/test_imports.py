def test_from_tkinter_import_star(lint):
    code = "import tkinter\nfrom tkinter import *"
    assert lint(code) == {
        "2:1 TK201 Using `from tkinter import *` is a bad practice. Use `import tkinter as tk` or simply `import tkinter` instead."
    }


def test_from_tkinter_dot_ttk_import_star(lint):
    code = "from tkinter.ttk import Button\nfrom tkinter.ttk import *"
    assert lint(code) == {
        "2:1 TK202 Using `from tkinter.ttk import *` is a bad practice. Use `from tkinter import ttk` instead."
    }


def test_import_tkinter_dot_ttk_as_ttk(lint):
    code = "from tkinter import ttk\nimport tkinter.ttk as ttk"
    assert lint(code) == {
        "2:1 TK211 Using `import tkinter.ttk as ttk` is pointless. Use `from tkinter import ttk` instead."
    }
