from __future__ import annotations

import ast

from flake8_tkinter.utils import Error

TK201 = (
    "TK201 "
    "Using `from tkinter import *` is generally a bad practice and discouraged. "
    "Use `import tkinter as tk` or simply `import tkinter` instead."
)

TK202 = (
    "TK202 "
    "Using `from tkinter.ttk import *` is generally a bad practice and discouraged. "
    "Use `from tkinter import ttk` instead."
)


def detect_from_tkinter_import_star(node: ast.ImportFrom) -> list[Error] | None:
    if node.module == "tkinter" and node.names[0].name == "*":
        return [Error(node.lineno, node.col_offset, TK201)]


def detect_from_tkinter_dot_ttk_import_star(node: ast.ImportFrom) -> list[Error] | None:
    if node.module == "tkinter.ttk" and node.names[0].name == "*":
        return [Error(node.lineno, node.col_offset, TK202)]
