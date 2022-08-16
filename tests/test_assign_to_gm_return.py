from base import lint


def test_assign_to_gm_call_result():
    code = "import tkinter;a = tkinter.Button().pack()"
    assert lint(code) == {"1:16 TK131 Assigning result of .pack() call to a variable. pack() returns None, not the widget object itself."}

    code = "import tkinter;a, b = 1, tkinter.Button().grid()"
    assert lint(code) == {"1:16 TK131 Assigning result of .grid() call to a variable. grid() returns None, not the widget object itself."}


def test_assign_to_gm_call_result_but_its_not_a_tkinter_widget():
    code = "import tkinter;a = w.pack()"
    assert lint(code) == set()
