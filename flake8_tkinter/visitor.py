from __future__ import annotations

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .checkers.base import CheckerBase

from .checkers.data import Settings
from .checkers.TK111 import TK111
from .checkers.TK201 import TK201
from .checkers.TK202 import TK202
from .checkers.TK211 import TK211
from .checkers.TK221 import TK221
from .checkers.TK231 import TK231
from .checkers.TK232 import TK232


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: list[tuple[int, int, str]] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if node.module == "tkinter" and TK201.detect(node):
            self.append(node.lineno, node.col_offset, TK201)
        elif node.module == "tkinter.ttk" and TK202.detect(node):
            self.append(node.lineno, node.col_offset, TK202)

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for name in node.names:
            if name.name == "tkinter":
                Settings.tkinter_used = True
                Settings.tkinter_as = name.asname or "tkinter"

            if name.name == "tkinter.ttk":
                Settings.tkinter_used = True
                Settings.ttk_as = name.asname or "tkinter.ttk"

                if TK211.detect():
                    self.append(node.lineno, node.col_offset, TK211)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        # This is kind of dumb, but I don't want to keep track of every tkinter widget just for this
        if isinstance(node.func, ast.Attribute):
            if TK111.detect(node):
                self.append(*TK111.get_pos(node), TK111, node)
            elif TK231.detect(node):
                self.append(node.lineno, node.col_offset, TK231, node)

        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:  # noqa: N802
        if TK232.detect(node):
            self.append(*TK232.get_pos(node), TK232, node)

        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:  # noqa: N802
        if TK232.detect(node):
            self.append(*TK232.get_pos(node), TK232, node)

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        if TK221.detect(node):
            self.append(node.lineno, node.col_offset, TK221, node)

        self.generic_visit(node)

    def append(self, lineno: int, offset: int, rule: CheckerBase, data_source=None) -> None:
        self.problems.append((lineno, offset, rule.get_message(**rule.get_data(data_source))))
