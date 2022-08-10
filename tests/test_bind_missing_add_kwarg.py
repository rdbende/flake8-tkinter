from base import lint

from flake8_tkinter.checkers.TK231 import BIND_METHODS


def test_bind_add_true():
    for method in BIND_METHODS:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>', print, add=True)"
        else:
            code = f"widget.{method}('<Button-1>', print, add=True)"
        assert lint(code) == set()


def test_bind_add_false():
    for method in BIND_METHODS:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>', print, add=False)"
        else:
            code = f"widget.{method}('<Button-1>', print, add=False)"
        assert lint(code) == set()


def test_bind_add_missing():
    for method in BIND_METHODS:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>', print)"
        else:
            code = f"widget.{method}('<Button-1>', print)"
        assert lint(code) == {f"1:1 TK231 Using {method} without `add=True` will overwrite any existing bindings to this sequence on this widget. Either overwrite them explicitly with `add=False` or use `add=True` to keep existing bindings."}


def test_bind_method_without_handler_passed():
    for method in BIND_METHODS:
        if method == "bind_class":
            code = f"widget.{method}('Button', '<Button-1>')"
        else:
            code = f"widget.{method}('<Button-1>')"
        assert lint(code) == set()
