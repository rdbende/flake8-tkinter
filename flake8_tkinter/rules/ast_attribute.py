from __future__ import annotations

import ast
import tkinter.constants as cst

from flake8_tkinter.constants import DUMB_CONSTANTS
from flake8_tkinter.utils import State
from flake8_tkinter.messages import Error


TKINTER_CONSTANTS = {x for x in dir(cst) if x.isupper()}


def detect_use_of_dumb_constant(node: ast.Attribute) -> list[Error] | None:
    if isinstance(node.value, ast.Name) and node.value.id == State.tkinter_as and node.attr in DUMB_CONSTANTS:
        return [Error(221, node.lineno, node.col_offset, constant=node.attr)]


def detect_use_of_tkinter_dot_message(node: ast.Attribute) -> list[Error] | None:
    if isinstance(node.value, ast.Name) and node.value.id == State.tkinter_as and node.attr == "Message":
        return [Error(251, node.lineno, node.col_offset, constant=node.attr)]


def detect_use_of_tkinter_constant(node: ast.Attribute) -> list[Error] | None:
    if (
        isinstance(node.value, ast.Name)
        and node.value.id == State.tkinter_as
        and node.attr in TKINTER_CONSTANTS - DUMB_CONSTANTS
    ):
        return [Error(504, node.lineno, node.col_offset, value=getattr(cst, node.attr))]
