from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Generator

__version__ = "0.0.1"


TK001 = "TK001 'from tkinter import *' used; consider using 'import tkinter as tk' or simply 'import tkinter'"
TK002 = "TK002 'from tkinter.ttk import *' used; consider using 'from tkinter import ttk'"
# place for more * import warnings
TK010 = "TK010 'import tkinter.ttk as ttk' used; could be simplified to 'from tkinter import ttk'"
TK020 = "TK020 Inline call to '{func}' for 'command' argument at '{widget}'. Perhaps you meant 'command={func}' (without the parentheses)?"
TK030 = "TK030 'time.sleep({seconds})' used, since it blocks the thread and the GUI will freeze. Use the '.after(milliseconds)' method instead, which isavailable on every Tkinter widget"
TK040 = "TK040 tkinter.{name} used; use an appropriate built-in boolean instead"


data_dict = {}
has_command_arg = {"Button", "Checkbutton", "Radiobutton", "Scale", "Scrollbar"}


class ProblemParser:
    @staticmethod
    def is_from_tkinter(namespace: str) -> bool:
        return namespace in {
            data_dict.get("tkinter_imported_as", False),
            data_dict.get("ttk_imported_as", False),
        }

    @staticmethod
    def process_time_sleep(node: ast.Call, problems_list: list[tuple[int, int, str]]) -> None:
        if (
            (
                isinstance(node.func, ast.Attribute)
                and ".".join([node.func.value.id, node.func.attr]) == "time.sleep"
            )
            or (
                isinstance(node.func, ast.Name)
                and node.func.id == "sleep"
                and data_dict.get("sleep_from_time", False)
            )
            and data_dict.get("tkinter_used", False)  # don't warn if tkinter isn't imported
        ):

            problems_list.append(
                (node.lineno, node.col_offset, TK030.format(seconds=node.args[0].value))
            )

    @staticmethod
    def process_command_handler_call(
        node: ast.Call, problems_list: list[tuple[int, int, str]]
    ) -> None:
        if not isinstance(node.func, ast.Attribute):
            return

        attr = node.func.attr
        namespace = node.func.value.id  # type: ignore

        if ProblemParser.is_from_tkinter(namespace) and attr in has_command_arg:
            for keyword in node.keywords:
                if keyword.arg == "command" and isinstance(keyword.value, ast.Call):
                    return problems_list.append(
                        (
                            node.lineno,
                            node.col_offset,
                            TK020.format(
                                func=keyword.value.func.id,  # type: ignore
                                widget=".".join([namespace, attr]),
                            ),
                        ),
                    )

    @staticmethod
    def process_from_time_import(node: ast.ImportFrom) -> None:
        if any([x.name == "sleep" for x in node.names]):
            data_dict["sleep_from_time"] = node.level == 0

    @staticmethod
    def process_from_tkinter_import(
        node: ast.ImportFrom, problems_list: list[tuple[int, int, str]]
    ) -> None:
        for name in node.names:
            if name.name == "ttk":
                data_dict["tkinter_used"] = True
                data_dict["ttk_imported_as"] = name.asname or "ttk"

            if name.name == "*":
                data_dict["tkinter_used"] = True
                problems_list.append((node.lineno, node.col_offset, TK001))

    @staticmethod
    def process_from_tkinter_ttk_import(
        node: ast.ImportFrom, problems_list: list[tuple[int, int, str]]
    ) -> None:
        if node.names[0].name == "*":
            data_dict["tkinter_used"] = True
            problems_list.append((node.lineno, node.col_offset, TK002))

    @staticmethod
    def process_tkinter_dot_TRUE_FALSE(
        node: ast.ImportFrom, problems_list: list[tuple[int, int, str]]
    ) -> None:
        if node.names[0].name == "*":
            data_dict["tkinter_used"] = True
            problems_list.append((node.lineno, node.col_offset, TK002))


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.problems: list[tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        ProblemParser.process_time_sleep(node, self.problems)
        ProblemParser.process_command_handler_call(node, self.problems)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "time":
            ProblemParser.process_from_time_import(node)
        elif node.module == "tkinter":
            ProblemParser.process_from_tkinter_import(node, self.problems)
        elif node.module == "tkinter.ttk":
            ProblemParser.process_from_tkinter_ttk_import(node, self.problems)

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            if name.name == "tkinter":
                data_dict["tkinter_used"] = True
                data_dict["tkinter_imported_as"] = name.asname or "tkinter"

            if name.name == "tkinter.ttk":
                data_dict["tkinter_used"] = True
                data_dict["ttk_imported_as"] = name.asname or "tkinter.ttk"

                if name.asname == "ttk":
                    self.problems.append((node.lineno, node.col_offset, TK010))

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.Import) -> None:
        if node.name == "sleep":
            data_dict["sleep_from_time"] = False

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Import) -> None:
        if node.value.id == data_dict.get("tkinter_imported_as") and node.attr in {
            "TRUE",
            "FALSE",
            "YES",
            "NO",
            "ON",
            "OFF",
        }:
            self.problems.append((node.lineno, node.col_offset, TK040.format(name=node.attr)))

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
