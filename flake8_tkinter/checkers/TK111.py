from __future__ import annotations

import ast

from .base import CheckerBase
from .data import Settings
from .TK231 import BIND_METHODS

COMMAND_ARGS = {"command", "xscrollcommand", "yscrollcommand", "postcommand"}
CONFIG_METHODS = {"config", "configure"}


class TK111(CheckerBase):
    message = ""
    message_on_command_arg = "Calling '{handler}()' instead of referencing it for '{argument}'. Perhaps you meant '{argument}={handler}' (without the parentheses)?"
    message_on_bind = "Calling '{handler}()' instead of referencing it for bind. Perhaps you meant '{handler}' (without the parentheses)?"

    @staticmethod
    def detect(node: ast.Call) -> bool:
        if isinstance(node.func.value, ast.Name):
            if (
                node.func.value.id in {Settings.tkinter_as, Settings.ttk_as}
                or node.func.attr in CONFIG_METHODS
            ):
                for keyword in node.keywords:
                    return (
                        keyword.arg in COMMAND_ARGS
                        and isinstance(keyword.value, ast.Call)
                        and not keyword.value.args
                        and not keyword.value.keywords
                    )
            elif node.func.attr in BIND_METHODS and len(node.args) >= 2:
                return isinstance(node.args[1], ast.Call)

    @classmethod
    def get_message(cls, handler: str | None, argument: str | None = None) -> str:
        if argument is None:
            msg = cls.message_on_bind
        else:
            msg = cls.message_on_command_arg

        return f"{cls.__mro__[0].__name__} {msg.format(handler=handler, argument=argument)}"

    @staticmethod
    def get_data(node: ast.Call) -> dict[str, str]:
        if node.func.value.id in {Settings.tkinter_as, Settings.ttk_as} or node.func.attr in CONFIG_METHODS:
            keyword, *_ = [kw for kw in node.keywords if kw.arg in COMMAND_ARGS]
            func = keyword.value.func

            if isinstance(func, ast.Name):
                return {"handler": func.id, "argument": keyword.arg}
            elif isinstance(func, ast.Attribute):
                return {
                    "handler": ".".join([func.value.id, func.attr]),
                    "argument": keyword.arg,
                }
        elif node.func.attr in BIND_METHODS:
            func = node.args[1].func

            if isinstance(func, ast.Name):
                return {"handler": func.id}
            elif isinstance(func, ast.Attribute):
                return {"handler": ".".join([func.value.id, func.attr])}

        raise NotImplementedError(
            "Oh, crap! This is an error with flake8-tkinter.\n\
                     Please report this error here: https://github.com/rdbende/flake8-tkinter/issues/new"
        )

    @staticmethod
    def get_pos(node: ast.Call) -> tuple[int, int]:
        if node.func.value.id in {Settings.tkinter_as, Settings.ttk_as} or node.func.attr in CONFIG_METHODS:
            keyword, *_ = [kw for kw in node.keywords if kw.arg in COMMAND_ARGS]
            return keyword.value.lineno, keyword.value.col_offset
        elif node.func.attr in BIND_METHODS:
            return node.args[1].func.lineno, node.args[1].func.col_offset
