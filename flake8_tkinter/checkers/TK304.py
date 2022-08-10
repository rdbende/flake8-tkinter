from __future__ import annotations

import ast

from .base import CheckerBase
from .TK231 import BIND_METHODS


class TK304(CheckerBase):
    message = "Value for `add` should be a boolean."

    @staticmethod
    def detect(node: ast.Call) -> bool:
        return node.func.attr in BIND_METHODS and {
            keyword
            for keyword in node.keywords
            if keyword.arg == "add"
            and isinstance(keyword.value, ast.Constant)
            and not isinstance(keyword.value.value, bool)
        }

    @staticmethod
    def get_pos(node: ast.Call) -> tuple[int, int]:
        for keyword in node.keywords:
            if keyword.arg == "add":
                return keyword.lineno, keyword.col_offset
