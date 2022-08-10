from __future__ import annotations

import ast

from .base import CheckerBase
from .data import is_from_tkinter
from .TK231 import BIND_METHODS

COMMAND_ARGS = {"command", "xscrollcommand", "yscrollcommand", "postcommand"}
CONFIG_METHODS = {"config", "configure"}


class TK111(CheckerBase):
    message = " (without the parentheses)?"
    message_on_command_arg = "Calling '{handler}()' instead of referencing it for '{argument}'. Perhaps you meant '{argument}={handler}'"
    message_on_bind = (
        "Calling '{handler}()' instead of referencing it for bind. Perhaps you meant '{handler}'"
    )

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
                    and not (func.args or func.keywords)
                )
        elif node.func.attr in BIND_METHODS and len(node.args) >= 2:
            func = node.args[1]
            return isinstance(func, ast.Call) and not (func.args or func.keywords)

    @classmethod
    def get_message(cls, handler: str | None, argument: str | None = None) -> str:
        if argument is None:
            msg = cls.message_on_bind
        else:
            msg = cls.message_on_command_arg

        return f"{cls.__mro__[0].__name__} {(msg + cls.message).format(handler=handler, argument=argument)}"

    @staticmethod
    def get_data(node: ast.Call) -> dict[str, str]:
        if is_from_tkinter(node.func.value.id) or node.func.attr in CONFIG_METHODS:
            keyword, *_ = [kw for kw in node.keywords if kw.arg in COMMAND_ARGS]
            func = keyword.value.func

            if isinstance(func, ast.Name):
                return {"handler": func.id, "argument": keyword.arg}
            elif isinstance(func, ast.Attribute):
                return {
                    "handler": f"{func.value.id}.{func.attr}",
                    "argument": keyword.arg,
                }
            elif isinstance(func, ast.Lambda):
                return {"handler": "<lambda>"}

        elif node.func.attr in BIND_METHODS:
            func = node.args[1].func

            if isinstance(func, ast.Name):
                return {"handler": func.id}
            elif isinstance(func, ast.Attribute):
                return {"handler": f"{func.value.id}.{func.attr}"}
            elif isinstance(func, ast.Lambda):
                return {"handler": "<lambda>"}

        return {"handler": "", "argument": ""}

    @staticmethod
    def get_pos(node: ast.Call) -> tuple[int, int]:
        if is_from_tkinter(node.func.value.id) or node.func.attr in CONFIG_METHODS:
            keyword, *_ = [kw for kw in node.keywords if kw.arg in COMMAND_ARGS]
            return keyword.value.lineno, keyword.value.col_offset
        elif node.func.attr in BIND_METHODS:
            return node.args[1].func.lineno, node.args[1].func.col_offset
