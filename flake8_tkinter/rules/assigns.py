from __future__ import annotations

import ast

from flake8_tkinter.api import is_attr_call, is_from_tkinter, register
from flake8_tkinter.constants import GM_METHODS
from flake8_tkinter.messages import Error


@register(ast.Assign)
def detect_assign_to_gm_return(node: ast.Assign) -> list[Error] | None:
    for element in node.value.elts if isinstance(node.value, ast.Tuple) else [node.value]:
        if (
            is_attr_call(element)
            and is_attr_call(element.func.value)
            and is_from_tkinter(element.func.value.func.value)
            and element.func.attr in GM_METHODS
        ):
            return [Error(131, node.lineno, node.col_offset, func=element.func.attr)]
