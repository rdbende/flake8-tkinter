from base import lint


def test_command_arg_function_call_with_args_with_plain_tkinter():
    code = "import tkinter as tk;tk.Button(command=handler(foo, bar))"
    assert lint(code) == {
        "1:40 TK112 Calling 'handler()' with arguments instead of referencing it for 'command'. If you need to call 'handler' with arguments, use lambda or functools.partial."
    }


def test_command_arg_function_call_with_args_with_ttk():
    code = "from tkinter import ttk;ttk.Button(command=handler(foo, bar))"
    assert lint(code) == {
        "1:44 TK112 Calling 'handler()' with arguments instead of referencing it for 'command'. If you need to call 'handler' with arguments, use lambda or functools.partial."
    }


def test_command_arg_function_call_with_args_in_config():
    code = "w.config(command=handler(foo, bar))"
    assert lint(code) == {
        "1:18 TK112 Calling 'handler()' with arguments instead of referencing it for 'command'. If you need to call 'handler' with arguments, use lambda or functools.partial."
    }


def test_bind_function_call_with_args():
    code = "w.bind('<Button-1>', handler(foo, bar), add=True)"
    assert lint(code) == {
        "1:22 TK112 Calling 'handler()' with arguments instead of referencing it for bind. If you need to call 'handler' with arguments, use lambda or functools.partial."
    }
