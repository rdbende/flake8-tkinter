from base import lint


def test_command_arg_function_call_with_args_with_plain_tkinter():
    code = "import tkinter as tk;tk.Button(command=foo(bar, baz))"
    assert lint(code) == {
        "1:40 TK112 Calling `foo()` with arguments instead of referencing it for `command`. If you need to call `foo` with arguments, use lambda or functools.partial."
    }


def test_command_arg_function_call_with_args_with_ttk():
    code = "from tkinter import ttk;ttk.Button(command=foo(bar, baz))"
    assert lint(code) == {
        "1:44 TK112 Calling `foo()` with arguments instead of referencing it for `command`. If you need to call `foo` with arguments, use lambda or functools.partial."
    }


def test_command_arg_function_call_with_args_in_config():
    code = "import tkinter;w.config(command=foo(bar, baz))"
    assert lint(code) == {
        "1:33 TK112 Calling `foo()` with arguments instead of referencing it for `command`. If you need to call `foo` with arguments, use lambda or functools.partial."
    }


def test_bind_function_call_with_args():
    code = "import tkinter;w.bind('<Button-1>', foo(bar, baz), add=True)"
    assert lint(code) == {
        "1:37 TK112 Calling `foo()` with arguments instead of referencing it for `bind`. If you need to call `foo` with arguments, use lambda or functools.partial."
    }
