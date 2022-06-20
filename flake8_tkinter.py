from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Generator

__version__ = "0.0.1"


TK001 = "TK001 'from tkinter import *' used; consider using 'import tkinter as tk' or simply 'import tkinter'"
TK002 = (
    "TK002 'from tkinter.ttk import *' used; consider using 'from tkinter import ttk'"
)
# place for more * import warnings
TK010 = "TK010 'import tkinter.ttk as ttk' used; could be simplified to 'from tkinter import ttk'"
TK020 = "TK020 Inline call to '{func}' for 'command' argument in {widget}. Perhaps you meant 'command={func}' (without the parentheses)?"


tkinter_imported_as = None
ttk_imported_as = None
has_command_arg = {"Button", "Checkbutton", "Radiobutton", "Scale", "Scrollbar"}


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: list[tuple[int, int, str]] = []

    def is_from_tkinter(self, id_: str) -> bool:
        """Checks whether a name is from the tkinter namespace"""
        return id_ in {tkinter_imported_as, ttk_imported_as}

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            id_ = node.func.value.id  # type: ignore

            if self.is_from_tkinter(id_) and attr in has_command_arg:
                for keyword in node.keywords:
                    if keyword.arg == "command" and isinstance(keyword.value, ast.Call):
                        self.problems.append(
                            (
                                node.lineno,
                                node.col_offset,
                                TK020.format(
                                    func=keyword.value.func.id,  # type: ignore
                                    widget=".".join([id_, attr]),
                                ),
                            )
                        )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "tkinter":
            if node.names[0].name == "ttk":
                global ttk_imported_as
                ttk_imported_as = (
                    node.names[0].asname if node.names[0].asname else "ttk"
                )

            if node.names[0].name == "*":
                self.problems.append(
                    (
                        node.lineno,
                        node.col_offset,
                        TK001,
                    )
                )

        if node.module == "tkinter.ttk" and node.names[0].name == "*":
            self.problems.append(
                (
                    node.lineno,
                    node.col_offset,
                    TK002,
                )
            )

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        if node.names[0].name == "tkinter":
            global tkinter_imported_as
            tkinter_imported_as = (
                node.names[0].asname if node.names[0].asname else "tkinter"
            )

        if node.names[0].name == "tkinter.ttk":
            global ttk_imported_as
            ttk_imported_as = (
                node.names[0].asname if node.names[0].asname else "tkinter.ttk"
            )

            if node.names[0].asname == "ttk":
                self.problems.append(
                    (
                        node.lineno,
                        node.col_offset,
                        TK010,
                    )
                )

        self.generic_visit(node)


@dataclass(frozen=True)
class Plugin:
    name = __name__
    version = __version__
    tree: ast.AST

    def run(self) -> Generator[tuple[int, int, str, None], None, None]:
        visitor = Visitor()
        visitor.visit(self.tree)

        for line, col, msg in visitor.problems:
            yield line, col, msg, None
