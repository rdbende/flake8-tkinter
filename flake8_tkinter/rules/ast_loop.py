from __future__ import annotations

import ast

from flake8_tkinter.utils import Error, is_call_attr, is_func

TK232 = (
    "TK232 "
    "Creating tag bindings in a loop can lead to memory leaks. "
    "Store the returned command names in a list to clean them up later."
)


def detect_tag_bind_in_loop_badly(node: ast.For | ast.While) -> list[Error] | None:
    tag_bind = False
    appended = False
    tag_bind_pos = (0, 0)

    elems = [el for el in node.body if isinstance(el, (ast.Assign, ast.Expr)) and is_call_attr(el)]

    for expr in elems:
        if is_func(expr, "tag_bind"):
            tag_bind = True
            tag_bind_pos = (expr.value.lineno, expr.value.col_offset)
            variable = expr.targets[0].id if isinstance(expr, ast.Assign) else None
        elif tag_bind and is_func(expr, "append"):
            arg = expr.value.args[0] if len(expr.value.args) != 0 else None
            appended = isinstance(arg, ast.Name) and arg.id == variable

    if tag_bind and not appended:
        return [Error(*tag_bind_pos, TK232)]
