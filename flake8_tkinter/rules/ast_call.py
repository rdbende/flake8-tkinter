from __future__ import annotations

import ast

from flake8_tkinter.constants import BIND_METHODS, COMMAND_ARGS, CONFIG_METHODS
from flake8_tkinter.utils import (
    State,
    get_func_name,
    is_functools_partial,
    is_if_name_equals_main,
    is_tkinter_namespace,
)
from flake8_tkinter.messages import Error


def detect_called_func_command_arg(node: ast.Call) -> list[Error] | None:
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and (is_tkinter_namespace(node.func.value.id) or node.func.attr in CONFIG_METHODS)
    ):
        for keyword in node.keywords:
            func = keyword.value
            if isinstance(func, ast.Call) and keyword.arg in COMMAND_ARGS:
                msg_id = 0

                if not (func.args or func.keywords):
                    msg_id = 111
                elif not is_functools_partial(func):
                    msg_id = 112

                if msg_id:
                    return [
                        Error(
                            msg_id,
                            keyword.value.lineno,
                            keyword.value.col_offset,
                            handler=get_func_name(func),
                            argument=keyword.arg,
                            meant=f"{keyword.arg}={get_func_name(func)}",
                        )
                    ]


def detect_called_func_bind(node: ast.Call) -> list[Error] | None:
    if node.func.attr != "tag_bind" and len(node.args) >= (2 if node.func.attr != "bind_class" else 3):
        func = node.args[1 if node.func.attr != "bind_class" else 2]
        if isinstance(func, ast.Call):
            msg_id = 0

            if not (func.args or func.keywords):
                msg_id = 111
            elif not is_functools_partial(func):
                msg_id = 112

            if msg_id:
                return [
                    Error(
                        msg_id,
                        func.func.lineno,
                        func.func.col_offset,
                        handler=get_func_name(func),
                        argument="bind()",
                        meant=get_func_name(func),
                    )
                ]


def detect_multiple_mainloop_calls(node: ast.Call) -> list[Error] | None:
    if isinstance(node.func, ast.Attribute) and node.func.attr == "mainloop" and not (node.args or node.keywords):
        if State.mainloop_already_called:
            if hasattr(node.parent, "parent") and not (
                isinstance(node.parent.parent, ast.If) and not is_if_name_equals_main(node.parent.parent)
            ):
                return [Error(102, node.lineno, node.col_offset)]
        else:
            State.mainloop_already_called = True


def detect_bind_add_missing(node: ast.Call) -> list[Error] | None:
    if (
        node.func.attr != "tag_bind"
        and len(node.args) >= (2 if node.func.attr != "bind_class" else 3)
        and "add" not in {keyword.arg for keyword in node.keywords}
    ):
        return [Error(141, node.lineno, node.col_offset, bind_method=node.func.attr)]


def detect_bind_add_is_not_boolean(node: ast.Call) -> list[Error] | None:
    for keyword in node.keywords:
        if (
            keyword.arg == "add"
            and isinstance(keyword.value, ast.Constant)
            and not isinstance(keyword.value.value, bool)
        ):
            return [Error(304, keyword.lineno, keyword.col_offset)]
