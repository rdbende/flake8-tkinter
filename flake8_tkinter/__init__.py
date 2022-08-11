from __future__ import annotations

import ast
from collections.abc import Generator
from dataclasses import dataclass

from .visitor import Visitor

__version__ = "0.5.0"


@dataclass(frozen=True)
class Plugin:
    name = __name__
    version = __version__
    tree: ast.AST

    def run(self) -> Generator[tuple[int, int, str, None], None, None]:
        visitor = Visitor()
        visitor.visit(self.tree)

        for error in visitor.errors:
            yield error.line, error.col, error.msg, None
