from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _Settings:
    tkinter_used: bool = False
    tkinter_as: str = ""
    ttk_as: str = ""
    mainloop_already_called: bool = False


Settings = _Settings()


def is_from_tkinter(thing: str) -> bool:
    return thing in {Settings.tkinter_as, Settings.ttk_as}
