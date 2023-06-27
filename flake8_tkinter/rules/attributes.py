from __future__ import annotations

import ast
from tkinter import constants

from flake8_tkinter.api import State, is_from_tkinter, register
from flake8_tkinter.constants import DUMB_CONSTANTS
from flake8_tkinter.messages import Error

TKINTER_CONSTANTS = {x for x in dir(constants) if x.isupper()}


@register(ast.Attribute)
def detect_use_of_dumb_constant(node: ast.Attribute) -> list[Error] | None:
    assert is_from_tkinter(node.value)
    assert node.attr in DUMB_CONSTANTS

    return [Error(221, node.lineno, node.col_offset, constant=node.attr)]


@register(ast.Attribute)
def detect_use_of_tkinter_dot_message(node: ast.Attribute) -> list[Error] | None:
    assert is_from_tkinter(node.value)
    assert node.attr == "Message"

    return [Error(251, node.lineno, node.col_offset, constant=node.attr)]


@register(ast.Attribute)
def detect_use_of_tkinter_constant(node: ast.Attribute) -> list[Error] | None:
    assert is_from_tkinter(node.value)
    assert node.attr in TKINTER_CONSTANTS - DUMB_CONSTANTS

    return [Error(504, node.lineno, node.col_offset, value=getattr(constants, node.attr))]
