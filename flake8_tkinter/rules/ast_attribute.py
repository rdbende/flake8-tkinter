from __future__ import annotations

import ast
import tkinter.constants as cst

from flake8_tkinter.constants import DUMB_CONSTANTS
from flake8_tkinter.utils import Error, Settings

TK221 = "TK221 Using tkinter.{constant} is pointless. Use an appropriate Python boolean instead."
TK251 = "TK251 Using `tkinter.Message` widget. It's redundant since `tkinter.Label` provides the same functionality."
TK504 = "TK504 Using a tkinter constant. Use a string literal instead ('{value}')."

TKINTER_CONSTANTS = {x for x in dir(cst) if x.isupper()}


def detect_use_of_dumb_constant(node: ast.Attribute) -> list[Error] | None:
    if (
        isinstance(node.value, ast.Name)
        and node.value.id == Settings.tkinter_as
        and node.attr in DUMB_CONSTANTS
    ):
        return [Error(node.lineno, node.col_offset, TK221.format(constant=node.attr))]


def detect_use_of_tkinter_dot_message(node: ast.Attribute) -> list[Error] | None:
    if (
        isinstance(node.value, ast.Name)
        and node.value.id == Settings.tkinter_as
        and node.attr == "Message"
    ):
        return [Error(node.lineno, node.col_offset, TK251.format(constant=node.attr))]


def detect_use_of_tkinter_constant(node: ast.Attribute) -> list[Error] | None:
    if (
        isinstance(node.value, ast.Name)
        and node.value.id == Settings.tkinter_as
        and node.attr in TKINTER_CONSTANTS - DUMB_CONSTANTS
    ):
        return [Error(node.lineno, node.col_offset, TK504.format(value=getattr(cst, node.attr)))]
