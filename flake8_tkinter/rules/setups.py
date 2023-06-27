from __future__ import annotations

import ast

from flake8_tkinter.utils import State
from flake8_tkinter.visitor import register


@register(ast.ImportFrom, True)
def setup_from_imports(node: ast.ImportFrom) -> None:
    if node.module in ("tkinter", "tkinter.ttk"):
        State.tkinter_used = True
        for name in node.names:
            if name.name == "ttk":
                State.ttk_as = name.asname or name.name


@register(ast.Import, True)
def setup_imports(node: ast.Import) -> None:
    for name in node.names:
        if name.name == "tkinter":
            State.tkinter_used = True
            State.tkinter_as = name.asname or name.name
        elif name.name == "tkinter.ttk":
            State.tkinter_used = True
            State.ttk_as = name.asname or name.name


@register(ast.Call, True)
def setup_wait_visibility_called(node: ast.Call) -> None:
    if isinstance(node.func, ast.Attribute) and node.func.attr == "wait_visibility":
        State.wait_visibility_already_called = True
