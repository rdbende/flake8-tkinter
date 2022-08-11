from __future__ import annotations

import ast

from flake8_tkinter.rules.ast_assign import detect_assign_to_gm_return
from flake8_tkinter.rules.ast_attribute import detect_use_of_dumb_constant
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
from flake8_tkinter.utils import Error, Settings


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[Error] = []

    def visit_Assign(self, node: ast.Assign) -> None:
        self.extend(detect_assign_to_gm_return(node))

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        self.extend(detect_use_of_dumb_constant(node))

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.extend(detect_bind_add_is_not_boolean(node))
        self.extend(detect_bind_add_missing(node))
        self.extend(detect_called_func_bind(node))
        self.extend(detect_called_func_command_arg(node))
        self.extend(detect_multiple_mainloop_calls(node))

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            if name.name == "tkinter":
                Settings.tkinter_used = True
                Settings.tkinter_as = name.asname or name.name
            elif name.name == "tkinter.ttk":
                Settings.tkinter_used = True
                Settings.ttk_as = name.asname or name.name

        self.extend(detect_import_tkinter_dot_ttk_as_ttk(node))

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "tkinter":
            Settings.tkinter_used = True
            for name in node.names:
                if name.name == "ttk":
                    Settings.ttk_as = name.asname or name.name

        self.extend(detect_from_tkinter_dot_ttk_import_star(node))
        self.extend(detect_from_tkinter_import_star(node))

        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.extend(detect_tag_bind_in_loop_badly(node))

        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.extend(detect_tag_bind_in_loop_badly(node))

        self.generic_visit(node)

    def extend(self, error: list[Error] | None) -> None:
        if Settings.tkinter_used and error:
            self.errors += error
