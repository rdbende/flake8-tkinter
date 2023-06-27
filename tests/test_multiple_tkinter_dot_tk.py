def test_multiple_tkinter_dot_tk(lint):
    code = "import tkinter\ndef foo():\n\ttkinter.Tk()\ntkinter.Tk()"
    assert lint(code) == {"4:1 TK101 Using multiple `tkinter.Tk` instances. Child windows must be created from `tkinter.Toplevel`."}


def test_second_tkinter_dot_tk_is_inside_name_equals_main_or_is_not_from_tkinter(lint):
    code = "import tkinter;tkinter.Tk\nif __name__ == '__main__':tkinter.Tk()"
    assert not lint(code)

    code = "import tkinter;foo.Tk;foo.Tk()"
    assert not lint(code)
