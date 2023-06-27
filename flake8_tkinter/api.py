from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import dataclass
from functools import wraps
from typing import Callable, TypeVar

from flake8_tkinter.messages import Error

T = TypeVar("T")


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[Error] = []


_registered_rules = defaultdict(list)


def visitor_method(visitor: ast.NodeVisitor, node: ast.AST) -> None:
    for func in _registered_rules[type(node)]:
        error = func(node)
        if error and State.tkinter_used:
            visitor.errors += error

    visitor.generic_visit(node)


def register(ast_node_type: T, important: bool = False) -> Callable[[T], list[Error] | None]:
    def decorator(func: T) -> Callable[[T], list[Error] | None]:
        @wraps(func)
        def wrapper(node: T) -> list[Error] | None:
            try:
                return func(node)
            except AssertionError:
                return None

        if important:
            _registered_rules[ast_node_type].insert(0, wrapper)
        else:
            _registered_rules[ast_node_type].append(wrapper)

        if not hasattr(Visitor, f"visit_{ast_node_type.__name__}"):
            setattr(Visitor, f"visit_{ast_node_type.__name__}", visitor_method)

        return wrapper

    return decorator


@dataclass
class _State:
    mainloop_already_called: bool = False
    wait_visibility_already_called: bool = False
    tkinter_used: bool = False
    tkinter_as: str = ""
    ttk_as: str = ""

    def reset(self):
        for field in self.__dataclass_fields__.values():
            setattr(self, field.name, field.default)


State = _State()


def generate_ancestry(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node


def is_from_tkinter(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id in {State.tkinter_as, State.ttk_as}


def is_functools_partial(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in {"partial", "partialmethod"}
    elif isinstance(func, ast.Attribute):
        return f"{func.value.id}.{func.attr}" in {
            "functools.partial",
            "functools.partialmethod",
        }

    return False


def is_attr_call(node: ast.AST) -> bool:
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)


def is_func(node: ast.Assign | ast.Expr, funcname: str) -> bool:
    return node.value.func.attr == funcname


def is_if_name_equals_main(node: ast.If) -> bool:
    return (
        isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "__name__"
        and isinstance(node.test.comparators[0], ast.Constant)
        and node.test.comparators[0].value == "__main__"
    )

def get_func_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    elif isinstance(func, ast.Attribute):
        return f"{func.value.id}.{func.attr}"
    elif isinstance(func, ast.Lambda):
        return "<lambda>"
    return "<function>"

def get_ancestors(node: ast.AST) -> list[type[ast.AST]]:
    result = []
    while True:
        if isinstance(node, ast.Module):
            break
        else:
            result.append(type(node.parent))
        node = node.parent

    return result
