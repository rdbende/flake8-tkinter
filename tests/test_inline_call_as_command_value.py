from base import _results


def test_inline_call_as_command_argument_value_for_Button():
    code = "import tkinter as tk\ntk.Button(command=handler())"
    assert _results(code) == {
        "2:1 TK020 Inline call to 'handler' for 'command' argument at 'tk.Button'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_inline_call_as_command_argument_value_for_Checkbutton():
    code = "import tkinter as tk\ntk.Checkbutton(command=handler())"
    assert _results(code) == {
        "2:1 TK020 Inline call to 'handler' for 'command' argument at 'tk.Checkbutton'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_inline_call_as_command_argument_value_for_Radiobutton():
    code = "import tkinter as tk\ntk.Radiobutton(command=handler())"
    assert _results(code) == {
        "2:1 TK020 Inline call to 'handler' for 'command' argument at 'tk.Radiobutton'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_inline_call_as_command_argument_value_for_Scale():
    code = "import tkinter as tk\ntk.Scale(command=handler())"
    assert _results(code) == {
        "2:1 TK020 Inline call to 'handler' for 'command' argument at 'tk.Scale'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }


def test_inline_call_as_command_argument_value_for_Scrollbar():
    code = "import tkinter as tk\ntk.Scrollbar(command=handler())"
    assert _results(code) == {
        "2:1 TK020 Inline call to 'handler' for 'command' argument at 'tk.Scrollbar'. Perhaps you meant 'command=handler' (without the parentheses)?"
    }
