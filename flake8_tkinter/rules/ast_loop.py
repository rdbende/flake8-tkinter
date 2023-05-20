from __future__ import annotations

import ast

from flake8_tkinter.utils import is_attr_call, is_func
from flake8_tkinter.messages import Error


def detect_tag_bind_in_loop_badly(node: ast.For | ast.While) -> list[Error] | None:
    tag_bind = False
    appended = False
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
