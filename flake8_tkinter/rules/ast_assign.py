from __future__ import annotations

import ast

from flake8_tkinter.constants import GM_METHODS
from flake8_tkinter.utils import is_attr_call, is_tkinter_namespace
from flake8_tkinter.messages import Error


def detect_assign_to_gm_return(node: ast.Assign) -> list[Error] | None:
    for element in node.value.elts if isinstance(node.value, ast.Tuple) else [node.value]:
        if (
            is_attr_call(element)
            and is_attr_call(element.func.value)
            and isinstance(element.func.value.func.value, ast.Name)
            and is_tkinter_namespace(element.func.value.func.value.id)
            and element.func.attr in GM_METHODS
        ):
            return [Error(131, node.lineno, node.col_offset, func=element.func.attr)]
