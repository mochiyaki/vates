from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseAgent(ABC, Generic[InputT, OutputT]):
    """Abstract base class for pipeline agents."""

    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def run(self, payload: InputT) -> OutputT:
        """Execute the agent on the provided payload."""

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"{self.__class__.__name__}(name={self.name!r})"

