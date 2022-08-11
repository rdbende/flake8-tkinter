from __future__ import annotations

import ast

from flake8_tkinter.constants import BIND_METHODS, COMMAND_ARGS, CONFIG_METHODS
from flake8_tkinter.utils import (
    Error,
    Settings,
    get_func_name,
    is_functools_partial,
    is_tkinter_namespace,
)

TK102 = "TK102 Using multiple mainloop calls is unnecessary. One call is perfectly enough."
TK111_command = (
    "TK111 "
    "Calling `{handler}()` instead of referencing it for `{argument}`. "
    "Perhaps you meant `{argument}={handler}` (without the parentheses)?"
)
TK111_bind = (
    "TK111 "
    "Calling `{handler}()` instead of referencing it for bind. "
    "Perhaps you meant `{handler}` (without the parentheses)?"
)
TK112_command = (
    "TK112 "
    "Calling `{handler}()` with arguments instead of referencing it for `{argument}`. "
    "If you need to call `{handler}` with arguments, use lambda or functools.partial."
)
TK112_bind = (
    "TK112 "
    "Calling `{handler}()` with arguments instead of referencing it for bind. "
    "If you need to call `{handler}` with arguments, use lambda or functools.partial."
)
TK231 = (
    "TK231 "
    "Using {bind_method} without `add=True` will overwrite any existing bindings "
    "to this sequence on this widget. Either overwrite them explicitly "
    "with `add=False` or use `add=True` to keep existing bindings."
)
TK304 = "TK304 Value for `add` should be a boolean."


def detect_called_func_command_arg(node: ast.Call) -> list[Error] | None:
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and (is_tkinter_namespace(node.func.value.id) or node.func.attr in CONFIG_METHODS)
    ):
        for keyword in node.keywords:
            func = keyword.value
            if isinstance(func, ast.Call) and keyword.arg in COMMAND_ARGS:
                msg = ""

                if not (func.args or func.keywords):
                    msg = TK111_command
                elif not is_functools_partial(func):
                    msg = TK112_command

                if msg:
                    return [
                        Error(
                            keyword.value.lineno,
                            keyword.value.col_offset,
                            msg.format(handler=get_func_name(func), argument=keyword.arg),
                        )
                    ]


def detect_called_func_bind(node: ast.Call) -> list[Error] | None:
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.attr in BIND_METHODS
        and len(node.args) >= 2
    ):
        func = node.args[1]
        if isinstance(func, ast.Call):
            msg = ""

            if not (func.args or func.keywords):
                msg = TK111_bind
            elif not is_functools_partial(func):
                msg = TK112_bind

            if msg:
                return [
                    Error(
                        func.func.lineno,
                        func.func.col_offset,
                        msg.format(handler=func.func.id),
                    )
                ]


def detect_multiple_mainloop_calls(node: ast.Call) -> list[Error] | None:
    if (isinstance(node.func, ast.Name) and node.func.id == "mainloop") or (
        isinstance(node.func, ast.Attribute) and node.func.attr == "mainloop"
    ):
        if Settings.mainloop_already_called:
            return [Error(node.lineno, node.col_offset, TK102)]
        else:
            Settings.mainloop_already_called = True


def detect_bind_add_missing(node: ast.Call) -> list[Error] | None:
    if isinstance(node.func, ast.Attribute) and node.func.attr in BIND_METHODS:
        if len(node.args) >= (3 if node.func.attr == "bind_class" else 2) and "add" not in {
            keyword.arg for keyword in node.keywords
        }:
            return [Error(node.lineno, node.col_offset, TK231.format(bind_method=node.func.attr))]


def detect_bind_add_is_not_boolean(node: ast.Call) -> list[Error] | None:
    if isinstance(node.func, ast.Attribute) and node.func.attr in BIND_METHODS | {"tag_bind"}:
        for keyword in node.keywords:
            if (
                keyword.arg == "add"
                and isinstance(keyword.value, ast.Constant)
                and not isinstance(keyword.value.value, bool)
            ):
                return [Error(keyword.lineno, keyword.col_offset, TK304)]
