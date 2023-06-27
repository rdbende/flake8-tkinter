from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import TYPE_CHECKING

from flake8_tkinter import rules
from flake8_tkinter.api import State, Visitor, generate_ancestry

if TYPE_CHECKING:
    from collections.abc import Generator

    from flake8.options.manager import OptionManager

__version__ = "0.6.0"


@dataclass(frozen=True)
class Plugin:
    name = __name__
    version = __version__
    tree: ast.AST

    def run(self) -> Generator[tuple[int, int, str, None], None, None]:
        generate_ancestry(self.tree)
        visitor = Visitor()
        visitor.visit(self.tree)

        for error in visitor.errors:
            yield error.line, error.col, error.msg, None

    @staticmethod
    def add_options(optmanager: OptionManager) -> None:
        optmanager.extend_default_ignore(["TK504"])
