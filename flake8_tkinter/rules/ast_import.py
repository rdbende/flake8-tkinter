from __future__ import annotations

import ast

from flake8_tkinter.utils import Error, Settings

TK211 = (
    "TK211 Using `import tkinter.ttk as ttk` is pointless. Use `from tkinter import ttk` instead."
)


def detect_import_tkinter_dot_ttk_as_ttk(node: ast.Import) -> list[Error] | None:
    for name in node.names:
        if name.name == "tkinter.ttk" and Settings.ttk_as == "ttk":
            return [Error(node.lineno, node.col_offset, TK211)]
