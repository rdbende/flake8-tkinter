from __future__ import annotations

import ast

from flake8_tkinter.messages import Error


def detect_from_tkinter_import_star(node: ast.ImportFrom) -> list[Error] | None:
    if node.module == "tkinter" and node.names[0].name == "*":
        return [Error(201, node.lineno, node.col_offset)]


def detect_from_tkinter_dot_ttk_import_star(node: ast.ImportFrom) -> list[Error] | None:
    if node.module == "tkinter.ttk" and node.names[0].name == "*":
        print("error")
        return [Error(202, node.lineno, node.col_offset)]
