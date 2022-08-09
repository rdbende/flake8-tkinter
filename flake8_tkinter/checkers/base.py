from __future__ import annotations

from typing import Protocol


class CheckerBase(Protocol):
    message: str

    @staticmethod
    def detect(*args) -> bool:
        ...

    @staticmethod
    def get_data(data_source) -> dict[str, str]:
        return {}

    @classmethod
    def get_message(cls, **kwargs) -> str:
        return f"{cls.__mro__[0].__name__} {cls.message.format(**kwargs)}"
