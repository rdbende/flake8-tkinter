import tkinter.constants as cst

from flake8_tkinter.constants import DUMB_CONSTANTS
from flake8_tkinter.rules.attributes import TKINTER_CONSTANTS


def test_use_of_tkinter_constant(lint):
    for name in TKINTER_CONSTANTS - DUMB_CONSTANTS:
        code = f"import tkinter\ntkinter.{name}"
        assert lint(code) == {
            f"2:1 TK504 Do not use tkinter constants. Use a string literal instead ('{getattr(cst, name)}')."
        }
