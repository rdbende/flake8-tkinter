from __future__ import annotations

import ast

from .base import CheckerBase


class TK232(CheckerBase):
    message = "Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later."

    @staticmethod
    def detect(node: ast.For | ast.While) -> bool:
        tag_bind = appended = False
        for expr in node.body:
            if (
                isinstance(expr, ast.Assign)
                and isinstance(expr.value, ast.Call)
                and isinstance(expr.value.func, ast.Attribute)
                and expr.value.func.attr == "tag_bind"
            ):
                tag_bind = True
                variable = expr.targets[0].id

            if (
                isinstance(expr, ast.Expr)
                and isinstance(expr.value, ast.Call)
                and isinstance(expr.value.func, ast.Attribute)
            ):
                if tag_bind and expr.value.func.attr == "append":
                    arg = expr.value.args[0] if len(expr.value.args) != 0 else None
                    appended = isinstance(arg, ast.Name) and arg.id == variable
                elif expr.value.func.attr == "tag_bind":
                    tag_bind = True
                    variable = None

        return tag_bind and not appended

    @staticmethod
    def get_pos(node: ast.For | ast.While) -> tuple[int, int]:
        for expr in node.body:
            if (
                isinstance(expr, (ast.Assign, ast.Expr))
                and isinstance(expr.value, ast.Call)
                and isinstance(expr.value.func, ast.Attribute)
                and expr.value.func.attr == "tag_bind"
            ):
                return expr.value.lineno, expr.value.col_offset
