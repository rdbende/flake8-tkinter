from base import lint


def test_assign_to_gm_call_result():
    code = "import tkinter;a = tkinter.Button().pack()"
    assert lint(code) == {"1:16 TK131 Do not assign `.pack()` to a variable. Since `pack` has no return value, the variable will be None, not the widget object itself."}

    code = "import tkinter;a, b = 1, tkinter.Button().grid()"
    assert lint(code) == {"1:16 TK131 Do not assign `.grid()` to a variable. Since `grid` has no return value, the variable will be None, not the widget object itself."}


def test_assign_to_gm_call_result_but_its_not_a_tkinter_widget():
    code = "import tkinter;a = w.pack()"
    assert lint(code) == set()
