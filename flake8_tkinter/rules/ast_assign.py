from __future__ import annotations

import ast

from flake8_tkinter.constants import GM_METHODS
from flake8_tkinter.utils import Error, is_call_attr

TK131 = "TK131 Assigning result of .{func}() call to a variable. {func}() returns None, not the widget object itself."


def detect_assign_to_gm_return(node: ast.Assign) -> list[Error] | None:
    if is_call_attr(node) and node.value.func.attr in GM_METHODS:
        return [Error(node.lineno, node.col_offset, TK131.format(func=node.value.func.attr))]
    elif isinstance(node.value, ast.Tuple):
        for element in node.value.elts:
            if (
                isinstance(element, ast.Call)
                and isinstance(element.func, ast.Attribute)
                and element.func.attr in GM_METHODS
            ):
                return [Error(node.lineno, node.col_offset, TK131.format(func=element.func.attr))]
