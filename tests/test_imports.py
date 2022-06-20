from base import _results


def test_from_tkinter_import_star():
    code = "from abc import *\nfrom tkinter import *"
    assert _results(code) == {
        "2:1 TK001 'from tkinter import *' used; consider using 'import tkinter as tk' or simply 'import tkinter'"
    }


def test_from_tkinter_ttk_import_star():
    code = "from abc import *\nfrom tkinter.ttk import *"
    assert _results(code) == {
        "2:1 TK002 'from tkinter.ttk import *' used; consider using 'from tkinter import ttk'"
    }


def test_import_tkinter_ttk_as_ttk():
    code = "from abc import *\nimport tkinter.ttk as ttk"
    assert _results(code) == {
        "2:1 TK010 'import tkinter.ttk as ttk' used; could be simplified to 'from tkinter import ttk'"
    }
