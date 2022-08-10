from __future__ import annotations

import ast

from .base import CheckerBase
from .data import Settings


class TK102(CheckerBase):
    message = (
        "Using multiple `mainloop` calls is totally unnecessary. One call is perfectly enough."
    )

    @staticmethod
    def detect(node: ast.Call) -> bool:
        if (isinstance(node.func, ast.Name) and node.func.id == "mainloop") or (
            isinstance(node.func, ast.Attribute) and node.func.attr == "mainloop"
        ):
            if Settings.mainloop_already_called:
                return True
            else:
                Settings.mainloop_already_called = True
