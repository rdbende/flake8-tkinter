from base import lint

from flake8_tkinter.constants import BIND_METHODS


def test_bind_add_true():
    for method in BIND_METHODS - {"tag_bind"}:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>', foo, add=True)"
        else:
            code = f"widget.{method}('<Button-1>', foo, add=True)"
        assert lint("import tkinter;" + code) == set()


def test_bind_add_false():
    for method in BIND_METHODS - {"tag_bind"}:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>', foo, add=False)"
        else:
            code = f"widget.{method}('<Button-1>', foo, add=False)"
        assert lint("import tkinter;" + code) == set()


def test_bind_add_missing():
    for method in BIND_METHODS - {"tag_bind"}:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>', foo)"
        else:
            code = f"widget.{method}('<Button-1>', foo)"
        assert lint("import tkinter;" + code) == {f"1:16 TK231 Using {method} without `add=True` will overwrite any existing bindings to this sequence on this widget. Either overwrite them explicitly with `add=False` or use `add=True` to keep existing bindings."}


def test_bind_method_without_handler_passed():
    for method in BIND_METHODS - {"tag_bind"}:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>')"
        else:
            code = f"widget.{method}('<Button-1>')"
        assert lint("import tkinter;" + code) == set()
