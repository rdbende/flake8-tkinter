from base import lint


def test_bind_add_equals_plus():
    code = "widget.bind('<Button-1>', print, add='+')"
    assert lint(code) == {"1:34 TK304 Value for `add` should be a boolean."}
