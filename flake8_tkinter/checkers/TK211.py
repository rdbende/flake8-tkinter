from __future__ import annotations

from .base import CheckerBase
from .data import Settings


class TK211(CheckerBase):
    message = "Using `import tkinter.ttk as ttk` is pointless. Use `from tkinter import ttk` instead."

    @staticmethod
    def detect() -> bool:
        return Settings.ttk_as == "ttk"
