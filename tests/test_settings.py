from flake8_tkinter.api import State


def test_import_tkinter(lint):
    lint("import tkinter")
    assert State.tkinter_as == "tkinter"


def test_import_tkinter_as_foo(lint):
    lint("import tkinter as foo")
    assert State.tkinter_as == "foo"


def test_import_tkinter_dot_ttk_as_bar(lint):
    lint("import tkinter.ttk as bar")
    assert State.ttk_as == "bar"


def test_from_tkinter_import_ttk(lint):
    lint("from tkinter import ttk")
    assert State.ttk_as == "ttk"


def test_from_tkinter_import_ttk_as_baz(lint):
    lint("from tkinter import ttk as baz")
    assert State.ttk_as == "baz"
