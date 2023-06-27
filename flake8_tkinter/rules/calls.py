from __future__ import annotations

import ast
import sys

from flake8_tkinter.api import State, is_if_name_equals_main, register, is_from_tkinter
from flake8_tkinter.constants import BIND_METHODS
from flake8_tkinter.messages import Error


@register(ast.Call)
def detect_multiple_mainloop_calls(node: ast.Call) -> list[Error] | None:
    assert isinstance(node.func, ast.Attribute)
    assert is_from_tkinter(node.func.value)
    assert node.func.attr == "Tk"

    if not State.root_window_already_exists:
        State.root_window_already_exists = True
        return

    assert hasattr(node.parent, "parent")
    assert not (isinstance(node.parent.parent, ast.If) and is_if_name_equals_main(node.parent.parent))

    return [Error(101, node.lineno, node.col_offset)]


@register(ast.Call)
def detect_multiple_mainloop_calls(node: ast.Call) -> list[Error] | None:
    assert isinstance(node.func, ast.Attribute)
    assert node.func.attr == "mainloop"
    assert not (node.args or node.keywords)  # actually, this isn't quite correct

    if not State.mainloop_already_called:
        State.mainloop_already_called = True
        return

    assert hasattr(node.parent, "parent")
    assert not (isinstance(node.parent.parent, ast.If) and is_if_name_equals_main(node.parent.parent))

    return [Error(102, node.lineno, node.col_offset)]


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
            if sys.version_info >= (3, 9):
                return [Error(304, kw.lineno, kw.col_offset)]
            else:
                return [Error(304, node.lineno, node.col_offset)]
