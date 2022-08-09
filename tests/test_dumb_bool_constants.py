from base import _results
from flake8_tkinter.checkers.TK221 import DUMB_CONSTANTS


def test_dumb_boolean_constants():
    for constant in DUMB_CONSTANTS:
        code = f"import tkinter as tk\ntk.{constant}"
        assert _results(code) == {
            f"2:1 TK221 Using tkinter.{constant} is pointless. Use an appropriate Python boolean instead."
        }
