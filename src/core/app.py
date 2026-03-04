"""Application lifecycle and configuration."""

from __future__ import annotations


class AppConfig:
    """Holds application configuration."""

    def __init__(
        self,
        title: str = "Desktop App",
        width: int = 480,
        height: int = 320,
    ) -> None:
        self.title = title
        self.width = width
        self.height = height
