from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import ast

from .base import CheckerBase


class TK202(CheckerBase):
    message = "Using `from tkinter.ttk import *` is generally a bad practice and discouraged. Use `from tkinter import ttk` instead."

    @staticmethod
    def detect(node: ast.ImportFrom) -> bool:
        return node.names[0].name == "*"
