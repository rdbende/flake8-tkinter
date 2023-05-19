from __future__ import annotations

import ast

from flake8_tkinter.utils import State
from flake8_tkinter.messages import Error


def detect_import_tkinter_dot_ttk_as_ttk(node: ast.Import) -> list[Error] | None:
    for name in node.names:
        if name.name == "tkinter.ttk" and State.ttk_as == "ttk":
            return [Error(211, node.lineno, node.col_offset)]
