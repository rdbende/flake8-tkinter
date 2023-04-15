from base import lint


def test_command_arg_function_call_with_plain_tkinter():
    code = "import tkinter;tkinter.Button(command=foo())"
    assert lint(code) == {
        "1:39 TK111 Calling `foo()` instead of referencing it for `command`. Perhaps you meant `command=foo` (without the parentheses)?"
    }


def test_command_arg_function_call_with_ttk():
    code = "from tkinter import ttk;ttk.Button(command=foo())"
    assert lint(code) == {
        "1:44 TK111 Calling `foo()` instead of referencing it for `command`. Perhaps you meant `command=foo` (without the parentheses)?"
    }


def test_command_arg_function_call_in_config():
    code = "import tkinter;w.config(command=foo())"
    assert lint(code) == {
        "1:33 TK111 Calling `foo()` instead of referencing it for `command`. Perhaps you meant `command=foo` (without the parentheses)?"
    }


def test_bind_function_call():
    code = "import tkinter;w.bind('<Button-1>', foo(), add=True)"
    assert lint(code) == {
        "1:37 TK111 Calling `foo()` instead of referencing it for bind. Perhaps you meant `foo` (without the parentheses)?"
    }
