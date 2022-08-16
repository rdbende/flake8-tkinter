from __future__ import annotations

import ast

from flake8_tkinter.constants import DUMB_CONSTANTS
from flake8_tkinter.utils import Error, Settings

TK221 = "TK221 Using tkinter.{constant} is pointless. Use an appropriate Python boolean instead."
TK251 = "TK251 Using `tkinter.Message` widget. It's redundant since `tkinter.Label` provides the same functionality."


def detect_use_of_dumb_constant(node: ast.Call) -> list[Error] | None:
    if (
        isinstance(node.value, ast.Name)
        and node.value.id == Settings.tkinter_as
        and node.attr in DUMB_CONSTANTS
    ):
        return [Error(node.lineno, node.col_offset, TK221.format(constant=node.attr))]


def detect_use_of_tkinter_dot_message(node: ast.Call) -> list[Error] | None:
    if (
        isinstance(node.value, ast.Name)
        and node.value.id == Settings.tkinter_as
        and node.attr == "Message"
    ):
        return [Error(node.lineno, node.col_offset, TK251.format(constant=node.attr))]
