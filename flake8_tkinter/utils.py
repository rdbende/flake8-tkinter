from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass
class Error:
    line: int
    col: int
    msg: str


@dataclass
class _Settings:
    mainloop_already_called: bool = False
    tkinter_used: bool = False
    tkinter_as: str = ""
    ttk_as: str = ""


Settings = _Settings()


def is_tkinter_namespace(thing: str) -> bool:
    return thing in {Settings.tkinter_as, Settings.ttk_as}


def is_functools_partial(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in {"partial", "partialmethod"}
    elif isinstance(func, ast.Attribute):
        return f"{func.value.id}.{func.attr}" in {
            "functools.partial",
            "functools.partialmethod",
        }

    return False


def get_func_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    elif isinstance(func, ast.Attribute):
        return f"{func.value.id}.{func.attr}"
    elif isinstance(func, ast.Lambda):
        return "<lambda>"


def is_call_attr(node: ast.Assign | ast.Expr) -> bool:
    return isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute)


def is_func(node: ast.Assign | ast.Expr, funcname: str) -> bool:
    return node.value.func.attr == funcname
