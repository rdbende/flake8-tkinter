from __future__ import annotations

import ast

from flake8_tkinter.constants import BIND_METHODS
from flake8_tkinter.messages import Error
from flake8_tkinter.utils import State
from flake8_tkinter.visitor import register


@register(ast.Call)
def detect_alpha_with_no_wait_visibility(node: ast.Call) -> list[Error] | None:
    assert isinstance(node.func, ast.Attribute)
    assert node.func.attr in ("attributes", "wm_attributes")
    assert "-alpha" in (arg.value for arg in node.args if isinstance(arg, ast.Constant))
    assert not State.wait_visibility_already_called

    return [Error(191, node.lineno, node.col_offset)]


@register(ast.Call)
def detect_bind_add_missing(node: ast.Call) -> list[Error] | None:
    assert isinstance(node.func, ast.Attribute)
    assert node.func.attr in BIND_METHODS - {"tag_bind"}
    assert len(node.args) >= (2 if node.func.attr != "bind_class" else 3)
    assert "add" not in {keyword.arg for keyword in node.keywords}

    return [Error(141, node.lineno, node.col_offset, bind_method=node.func.attr)]


@register(ast.Call)
def detect_bind_add_is_not_boolean(node: ast.Call) -> list[Error] | None:
    assert isinstance(node.func, ast.Attribute)
    assert node.func.attr in BIND_METHODS

    for kw in node.keywords:
        if kw.arg == "add" and isinstance(kw.value, ast.Constant) and not isinstance(kw.value.value, bool):
            return [Error(304, kw.lineno, kw.col_offset)]
