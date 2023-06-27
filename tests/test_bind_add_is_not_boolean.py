import sys


def test_bind_add_equals_plus(lint):
    code = "import tkinter;w.bind('<Button-1>', foo, add='+')"
    assert lint(code) == {f"1:{42 if sys.version_info >= (3, 9) else 16} TK304 Value for `add` should be a boolean."}
