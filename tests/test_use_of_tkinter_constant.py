from base import lint
import tkinter.constants as cst
from flake8_tkinter.rules.ast_attribute import TKINTER_CONSTANTS
from flake8_tkinter.constants import DUMB_CONSTANTS


def test_use_of_tkinter_constant():
    for name in TKINTER_CONSTANTS - DUMB_CONSTANTS:
        code = f"import tkinter\ntkinter.{name}"
        assert lint(code) == {
            f"2:1 TK504 Do not use tkinter constants. Use a string literal instead ('{getattr(cst, name)}')."
        }
