from base import lint
from flake8_tkinter.constants import DUMB_CONSTANTS


def test_dumb_boolean_constants():
    for constant in DUMB_CONSTANTS:
        code = f"import tkinter\ntkinter.{constant}"
        assert lint(code) == {
            f"2:1 TK221 Using tkinter.{constant} is pointless. Use an appropriate Python boolean instead."
        }
