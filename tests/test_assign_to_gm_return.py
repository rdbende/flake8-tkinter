def test_assign_to_gm_call_result(lint):
    expected = {"1:16 TK131 Do not assign `.pack()` to a variable. Since `pack` has no return value, the variable will be None, not the widget object itself."}
    code = "import tkinter;a = tkinter.Button().pack()"
    assert lint(code) == expected

    code = "import tkinter;a, b = 1, tkinter.Button().pack()"
    assert lint(code) == expected


def test_assign_to_gm_call_result_but_it_is_already_created(lint):
    code = "import tkinter;a = w.pack()"
    assert not lint(code)
