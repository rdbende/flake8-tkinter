from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass
class _State:
    mainloop_already_called: bool = False
    tkinter_used: bool = False
    tkinter_as: str = ""
    ttk_as: str = ""

    def reset(self):
        for field in self.__dataclass_fields__.values():
            setattr(self, field.name, field.default)


State = _State()


def is_tkinter_namespace(thing: str) -> bool:
    return thing in {State.tkinter_as, State.ttk_as}


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


def get_func_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    elif isinstance(func, ast.Attribute):
        return f"{func.value.id}.{func.attr}"
    elif isinstance(func, ast.Lambda):
        return "<lambda>"
    return "<function>"


def is_attr_call(node: ast.stmt) -> bool:
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
    )  # doesn't check the '==', but it's good enough


def get_ancestors(node: ast.stmt) -> list[type[ast.stmt]]:
    result = []
    while True:
        if isinstance(node, ast.Module):
            break
        else:
            result.append(type(node.parent))
        node = node.parent

    return result
