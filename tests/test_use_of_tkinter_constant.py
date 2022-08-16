from base import lint


def test_use_of_tkinter_constant():
    code = "import tkinter\ntkinter.CHORD"
    assert lint(code) == {
        "2:1 TK504 Using a tkinter constant. Use a string literal instead ('chord')."
    }

    code = "import tkinter\ntkinter.SEL_LAST"
    assert lint(code) == {
        "2:1 TK504 Using a tkinter constant. Use a string literal instead ('sel.last')."
    }
