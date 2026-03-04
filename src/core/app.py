
from __future__ import annotations


class AppConfig:


    def __init__(
        self,
        title: str = "Desktop App",
        width: int = 480,
        height: int = 320,
    ) -> None:
        self.title = title
        self.width = width
        self.height = height
