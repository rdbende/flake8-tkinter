from base import lint


def test_command_arg_function_call_with_plain_tkinter():
    code = "import tkinter as tk;tk.Button(command=handler())"
    assert lint(code) == {
        "1:40 TK111 Calling 'handler()' instead of referencing it for 'command'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_command_arg_function_call_with_ttk():
    code = "from tkinter import ttk;ttk.Button(command=handler())"
    assert lint(code) == {
        "1:44 TK111 Calling 'handler()' instead of referencing it for 'command'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_command_arg_function_call_in_config():
    code = "w.config(command=handler())"
    assert lint(code) == {
        "1:18 TK111 Calling 'handler()' instead of referencing it for 'command'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_bind_function_call():
    code = "w.bind('<Button-1>', handler(), add=True)"
    assert lint(code) == {
        "1:22 TK111 Calling 'handler()' instead of referencing it for bind. Perhaps you meant 'handler' (without the parentheses)?"
    }
