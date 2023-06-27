from __future__ import annotations

import ast

import pytest

from flake8_tkinter import Plugin
from flake8_tkinter.api import State


def do_lint(code_string: str) -> set[str]:
    plugin = Plugin(ast.parse(code_string))
    return {f"{line}:{col+1} {msg}" for line, col, msg, _ in plugin.run()}


@pytest.fixture()
def lint():
    yield do_lint
    State.reset()
