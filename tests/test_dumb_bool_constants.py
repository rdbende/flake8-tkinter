from base import _results


def test_dumb_boolean_constants():
    code = "import tkinter as tk\ntk.TRUE"
    assert _results(code) == {
        "2:1 TK040 tkinter.TRUE used; use an appropriate built-in boolean instead"
    }
