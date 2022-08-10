from base import lint
from flake8_tkinter.checkers.data import Settings


def test_import_tkinter():
    lint("import tkinter")
    assert Settings.tkinter_as == "tkinter"


def test_import_tkinter_as_foo():
    lint("import tkinter as foo")
    assert Settings.tkinter_as == "foo"


def test_import_tkinter_dot_ttk_as_baz():
    lint("import tkinter.ttk as baz")
    assert Settings.ttk_as == "baz"


def test_from_tkinter_import_ttk():
    lint("from tkinter import ttk")
    assert Settings.ttk_as == "ttk"


def test_from_tkinter_import_ttk_as_bar():
    lint("from tkinter import ttk as bar")
    assert Settings.ttk_as == "bar"
