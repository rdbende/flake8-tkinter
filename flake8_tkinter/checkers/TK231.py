from __future__ import annotations

import ast

from .base import CheckerBase
from .data import Settings

BIND_METHODS = {"bind", "bind_all", "bind_class"}
BIND_METHODS.add("bind_with_data")  # For Porcupine


class TK231(CheckerBase):
    message = "Using {bind_method} without `add=True` will overwrite any existing bindings to this sequence on this widget. Either overwrite them explicitly with `add=False` or use `add=True` to keep existing bindings."

    @staticmethod
    def detect(node: ast.Call) -> bool:
        return (
            node.func.attr in BIND_METHODS
            and len(node.args) >= (3 if node.func.attr == "bind_class" else 2)
            and "add" not in {keyword.arg for keyword in node.keywords}
        )

    @staticmethod
    def get_data(node: ast.Attribute) -> dict[str, str]:
        return {"bind_method": node.func.attr}
