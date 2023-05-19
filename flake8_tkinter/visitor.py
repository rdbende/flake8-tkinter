from __future__ import annotations

import ast

from flake8_tkinter.constants import BIND_METHODS
from flake8_tkinter.rules.ast_assign import detect_assign_to_gm_return
from flake8_tkinter.rules.ast_attribute import (
    detect_use_of_dumb_constant,
    detect_use_of_tkinter_constant,
    detect_use_of_tkinter_dot_message,
)
from flake8_tkinter.rules.ast_call import (
    detect_bind_add_is_not_boolean,
    detect_bind_add_missing,
    detect_called_func_bind,
    detect_called_func_command_arg,
    detect_multiple_mainloop_calls,
)
from flake8_tkinter.rules.ast_import import detect_import_tkinter_dot_ttk_as_ttk
from flake8_tkinter.rules.ast_import_from import (
    detect_from_tkinter_dot_ttk_import_star,
    detect_from_tkinter_import_star,
)
from flake8_tkinter.rules.ast_loop import detect_tag_bind_in_loop_badly
from flake8_tkinter.utils import State, get_ancestors
from flake8_tkinter.messages import Error


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[Error] = []

    def visit_Assign(self, node: ast.Assign) -> None:
        self.extend(detect_assign_to_gm_return(node))

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        self.extend(detect_use_of_dumb_constant(node))
        self.extend(detect_use_of_tkinter_constant(node))
        self.extend(detect_use_of_tkinter_dot_message(node))

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.extend(detect_called_func_command_arg(node))
        self.extend(detect_multiple_mainloop_calls(node))

        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)  # TODO: can it be something else?
            and node.func.attr in BIND_METHODS | {"tag_bind"}
        ):
            self.visit_tkinter_bind_method(node)

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            if name.name == "tkinter":
                State.tkinter_used = True
                State.tkinter_as = name.asname or name.name
            elif name.name == "tkinter.ttk":
                State.tkinter_used = True
                State.ttk_as = name.asname or name.name

        self.extend(detect_import_tkinter_dot_ttk_as_ttk(node))

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module in ("tkinter", "tkinter.ttk"):
            State.tkinter_used = True
            for name in node.names:
                if name.name == "ttk":
                    State.ttk_as = name.asname or name.name

        self.extend(detect_from_tkinter_dot_ttk_import_star(node))
        self.extend(detect_from_tkinter_import_star(node))

        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.extend(detect_tag_bind_in_loop_badly(node))

        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.extend(detect_tag_bind_in_loop_badly(node))

        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        ancestors = get_ancestors(node)
        if ast.For in ancestors or ast.While in ancestors:
            self.extend(detect_tag_bind_in_loop_badly(node))

        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        ancestors = get_ancestors(node)
        if ast.For in ancestors or ast.While in ancestors:
            self.extend(detect_tag_bind_in_loop_badly(node))

        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        ancestors = get_ancestors(node)
        if ast.For in ancestors or ast.While in ancestors:
            self.extend(detect_tag_bind_in_loop_badly(node))

        self.generic_visit(node)

    def visit_tkinter_bind_method(self, node: ast.Call) -> None:
        self.extend(detect_bind_add_is_not_boolean(node))
        self.extend(detect_bind_add_missing(node))
        self.extend(detect_called_func_bind(node))

    def extend(self, error: list[Error] | None) -> None:
        if State.tkinter_used and error:
            self.errors += error
