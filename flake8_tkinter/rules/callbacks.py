from __future__ import annotations

import ast

from flake8_tkinter.api import (
    State,
    get_ancestors,
    get_func_name,
    is_attr_call,
    is_func,
    is_functools_partial,
    is_if_name_equals_main,
    is_tkinter_namespace,
    register,
)
from flake8_tkinter.constants import BIND_METHODS, COMMAND_ARGS, CONFIG_METHODS
from flake8_tkinter.messages import Error


@register(ast.Call)
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


@register(ast.Call)
def detect_called_func_bind(node: ast.Call) -> list[Error] | None:
    assert isinstance(node.func, ast.Attribute)
    assert node.func.attr in BIND_METHODS - {"tag_bind"}
    assert len(node.args) >= (2 if node.func.attr != "bind_class" else 3)
    func = node.args[1 if node.func.attr != "bind_class" else 2]
    assert isinstance(func, ast.Call)

    if not (func.args or func.keywords):
        msg_id = 111
    elif not is_functools_partial(func):
        msg_id = 112
    else:
        msg_id = None

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


@register(ast.Call)
def detect_multiple_mainloop_calls(node: ast.Call) -> list[Error] | None:
    if isinstance(node.func, ast.Attribute) and node.func.attr == "mainloop" and not (node.args or node.keywords):
        if State.mainloop_already_called:
            if hasattr(node.parent, "parent") and not (
                isinstance(node.parent.parent, ast.If) and not is_if_name_equals_main(node.parent.parent)
            ):
                return [Error(102, node.lineno, node.col_offset)]
        else:
            State.mainloop_already_called = True


@register(ast.For)
@register(ast.While)
@register(ast.If)
@register(ast.With)
@register(ast.Try)
def detect_tag_bind_in_loop_badly(node: ast.For | ast.While | ast.If | ast.With | ast.Try) -> list[Error] | None:
    if not isinstance(node, (ast.For, ast.While)):
        ancestors = get_ancestors(node)
        assert ast.For in ancestors or ast.While in ancestors

    appended = tag_bind = False
    line = col = 0
    elems = [x for x in node.body if isinstance(x, (ast.Assign, ast.Expr)) and is_attr_call(x.value)]

    for expr in elems:
        if is_func(expr, "tag_bind"):
            tag_bind = True
            line, col = expr.value.lineno, expr.value.col_offset
            variable = expr.targets[0].id if isinstance(expr, ast.Assign) else None
        elif tag_bind and is_func(expr, "append"):
            arg = expr.value.args[0] if len(expr.value.args) != 0 else None
            appended = isinstance(arg, ast.Name) and arg.id == variable

    if tag_bind and not appended:
        return [Error(142, line, col)]
