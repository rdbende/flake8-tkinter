from __future__ import annotations

import ast

from flake8_tkinter import Plugin
from flake8_tkinter.utils import State


def lint(code_string: str) -> set[str]:
    State.reset()
    tree = ast.parse(code_string)
    plugin = Plugin(tree)

    return {f"{line}:{col+1} {msg}" for line, col, msg, _ in plugin.run()}
