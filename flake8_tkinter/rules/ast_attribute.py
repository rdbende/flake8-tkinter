from __future__ import annotations

import ast

from flake8_tkinter.constants import DUMB_CONSTANTS
from flake8_tkinter.utils import Error, Settings

TK221 = "TK221 Using tkinter.{constant} is pointless. Use an appropriate Python boolean instead."


def detect_use_of_dumb_constant(node: ast.Call) -> list[Error] | None:
    if not isinstance(node.value, ast.Name):
        return None

    if node.value.id == Settings.tkinter_as and node.attr in DUMB_CONSTANTS:
        return [Error(node.lineno, node.col_offset, TK221.format(constant=node.attr))]
