from base import _results


def test_inline_call_as_command_argument_value_tkinter():
    code = "import tkinter as tk\ntk.Button(command=handler())"
    assert _results(code) == {
        "2:19 TK111 Calling 'handler' instead of referencing it for 'command' argument. Perhaps you meant 'command=handler' (without the parentheses)?"
    }

    code = "from tkinter import ttk\nttk.Button(command=handler())"
    assert _results(code) == {
        "2:20 TK111 Calling 'handler' instead of referencing it for 'command' argument. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_inline_call_as_command_argument_value_widget_config():
    code = "from tkinter import ttk\nbutton = ttk.Button()\nbutton.config(command=handler())"
    assert _results(code) == {
        "3:23 TK111 Calling 'handler' instead of referencing it for 'command' argument. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_inline_call_as_command_argument_value_not_tk():
    code = "Checkbutton(command=handler())"
    assert _results(code) == set()
