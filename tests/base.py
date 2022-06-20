import ast

from flake8_tkinter import Plugin


def _results(code_string):
    tree = ast.parse(code_string)
    plugin = Plugin(tree)

    return {f"{line}:{col+1} {msg}" for line, col, msg, _ in plugin.run()}
