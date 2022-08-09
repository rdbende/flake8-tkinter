from __future__ import annotations

import ast

from .base import CheckerBase
from .data import Settings

DUMB_CONSTANTS = {"TRUE", "FALSE", "YES", "NO", "ON", "OFF"}


class TK221(CheckerBase):
    message = "Using tkinter.{constant} is pointless. Use an appropriate Python boolean instead."

    @staticmethod
    def detect(node: ast.Attribute) -> bool:
        return (
            isinstance(node.value, ast.Name)
            and node.value.id == Settings.tkinter_as
            and node.attr in DUMB_CONSTANTS
        )

    @staticmethod
    def get_data(node: ast.Attribute) -> dict[str, str]:
        return {"constant": node.attr}
