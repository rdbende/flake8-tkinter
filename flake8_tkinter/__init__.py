from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Generator

from .visitor import Visitor

__version__ = "0.2.1"


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
