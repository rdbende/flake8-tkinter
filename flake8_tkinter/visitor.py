from __future__ import annotations

import ast
from collections import defaultdict
from typing import TypeVar

from flake8_tkinter.messages import Error
from flake8_tkinter.utils import State


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[Error] = []


data = defaultdict(list)


def visitor_method(self, node) -> None:
    for func in data[type(node)]:
        error = func(node)
        if error and State.tkinter_used:
            self.errors += error

    self.generic_visit(node)


T = TypeVar("T")


def register(ast_node_type: T, does_setup=False):
    def decorator(func):
        def wrapper(node: T):
            try:
                return func(node)
            except AssertionError:
                return []

        if does_setup:
            data[ast_node_type].insert(0, wrapper)
        else:
            data[ast_node_type].append(wrapper)
        if not hasattr(Visitor, f"visit_{ast_node_type.__name__}"):
            setattr(Visitor, f"visit_{ast_node_type.__name__}", visitor_method)
        wrapper.func = func
        return wrapper

    return decorator
