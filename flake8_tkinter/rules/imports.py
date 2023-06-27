from __future__ import annotations

import ast

from flake8_tkinter.api import State, register
from flake8_tkinter.messages import Error


@register(ast.Import)
def detect_import_tkinter_dot_ttk_as_ttk(node: ast.Import) -> list[Error] | None:
    for name in node.names:
        if name.name == "tkinter.ttk" and State.ttk_as == "ttk":
            return [Error(211, node.lineno, node.col_offset)]


@register(ast.ImportFrom)
def detect_from_tkinter_import_star(node: ast.ImportFrom) -> list[Error] | None:
    if node.module == "tkinter" and node.names[0].name == "*":
        return [Error(201, node.lineno, node.col_offset)]


@register(ast.ImportFrom)
def detect_from_tkinter_dot_ttk_import_star(node: ast.ImportFrom) -> list[Error] | None:
    if node.module == "tkinter.ttk" and node.names[0].name == "*":
        return [Error(202, node.lineno, node.col_offset)]
