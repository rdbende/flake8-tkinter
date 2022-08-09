from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import ast

from .base import CheckerBase


class TK201(CheckerBase):
    message = "Using `from tkinter import *` is generally a bad practice and discouraged. Use `import tkinter as tk` or simply `import tkinter` instead."

    @staticmethod
    def detect(node: ast.ImportFrom) -> bool:
        return node.names[0].name == "*"
