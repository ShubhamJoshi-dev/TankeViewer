"""Main application window."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.app import AppConfig


class MainWindow:
    """Main window of the desktop application."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._root = tk.Tk()
        self._root.title(config.title)
        self._root.geometry(f"{config.width}x{config.height}")
        self._root.minsize(320, 240)
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the window content."""
        main = ttk.Frame(self._root, padding=16)
        main.pack(fill=tk.BOTH, expand=True)

        label = ttk.Label(main, text="Welcome")
        label.pack(pady=(0, 8))

        self._entry = ttk.Entry(main, width=32)
        self._entry.pack(pady=(0, 8), ipady=4)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=8)

        ttk.Button(btn_frame, text="Submit", command=self._on_submit).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(btn_frame, text="Clear", command=self._on_clear).pack(side=tk.LEFT)

        self._status = ttk.Label(main, text="")
        self._status.pack(pady=(16, 0))

    def _on_submit(self) -> None:
        """Handle submit button click."""
        value = self._entry.get().strip()
        if value:
            self._status.config(text=f"Submitted: {value}")
        else:
            self._status.config(text="Enter something first.")

    def _on_clear(self) -> None:
        """Handle clear button click."""
        self._entry.delete(0, tk.END)
        self._status.config(text="")

    def run(self) -> None:
        """Start the main event loop."""
        self._root.mainloop()
