from base import lint


def test_bind_add_equals_plus():
    code = "import tkinter;w.bind('<Button-1>', foo, add='+')"
    assert lint(code) == {"1:42 TK304 Value for `add` should be a boolean."}
