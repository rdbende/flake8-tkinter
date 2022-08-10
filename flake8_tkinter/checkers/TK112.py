from __future__ import annotations

import ast

from .data import is_from_tkinter
from .TK111 import TK111
from .TK231 import BIND_METHODS

COMMAND_ARGS = {"command", "xscrollcommand", "yscrollcommand", "postcommand"}
CONFIG_METHODS = {"config", "configure"}


def is_partial(func: ast.Name | ast.Attribute) -> bool:
    if isinstance(func, ast.Name):
        return func.id in ("partial", "partialmethod")
    elif isinstance(func, ast.Attribute):
        return f"{func.value.id}.{func.attr}" in (
            "functools.partial",
            "functools.partialmethod",
        )

    return False


class TK112(TK111):
    message = " If you need to call '{handler}' with arguments, use lambda or functools.partial."
    message_on_command_arg = (
        "Calling '{handler}()' with arguments instead of referencing it for '{argument}'."
    )
    message_on_bind = "Calling '{handler}()' with arguments instead of referencing it for bind."

    @staticmethod
    def detect(node: ast.Call) -> bool:
        if not isinstance(node.func.value, ast.Name):
            return

        if is_from_tkinter(node.func.value.id) or node.func.attr in CONFIG_METHODS:
            for keyword in node.keywords:
                func = keyword.value
                return (
                    keyword.arg in COMMAND_ARGS
                    and isinstance(func, ast.Call)
                    and (func.args or func.keywords)
                    and not is_partial(func.func)
                )
        elif node.func.attr in BIND_METHODS and len(node.args) >= 2:
            func = node.args[1]
            return (
                isinstance(func, ast.Call)
                and (func.args or func.keywords)
                and not is_partial(func.func)
            )
