"""JSON viewer window with tree view."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.app import AppConfig


class JsonViewer:
    """Window that displays JSON in an organized tree view."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._root = tk.Tk()
        self._root.title(config.title)
        self._root.geometry(f"{config.width}x{config.height}")
        self._root.minsize(400, 300)
        self._tree: ttk.Treeview | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Build toolbar and tree view."""
        main = ttk.Frame(self._root, padding=8)
        main.pack(fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(main)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(toolbar, text="Open", command=self._on_open).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(toolbar, text="Expand All", command=self._on_expand_all).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(toolbar, text="Collapse All", command=self._on_collapse_all).pack(
            side=tk.LEFT
        )

        tree_frame = ttk.Frame(main)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self._tree = ttk.Treeview(
            tree_frame,
            columns=("value",),
            show="tree headings",
            height=20,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode="browse",
        )
        self._tree.heading("#0", text="Key")
        self._tree.heading("value", text="Value")
        self._tree.column("#0", minwidth=200, width=280)
        self._tree.column("value", minwidth=150, width=200)

        self._configure_tags()

        scroll_y.config(command=self._tree.yview)
        scroll_x.config(command=self._tree.xview)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self._status = ttk.Label(main, text="Open a JSON file to start.")
        self._status.pack(pady=(8, 0), anchor=tk.W)

    def _configure_tags(self) -> None:
        """Set colors for value types in the tree."""
        if self._tree is None:
            return
        self._tree.tag_configure("object", foreground="#0550ae")
        self._tree.tag_configure("array", foreground="#0e6f42")
        self._tree.tag_configure("string", foreground="#0a3069")
        self._tree.tag_configure("number", foreground="#953800")
        self._tree.tag_configure("boolean", foreground="#6e40c9")
        self._tree.tag_configure("null", foreground="#6e7681")

    def _on_open(self) -> None:
        """Open file dialog and load JSON."""
        path = filedialog.askopenfilename(
            title="Open JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        self._load_file(Path(path))

    def _load_file(self, path: Path) -> None:
        """Load and display JSON from file."""
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self._display(data, path.name)
            self._status.config(text=str(path))
        except json.JSONDecodeError as e:
            messagebox.showerror("Invalid JSON", str(e))
        except OSError as e:
            messagebox.showerror("Open failed", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _display(self, data: Any, root_label: str = "JSON") -> None:
        """Clear tree and fill with JSON data."""
        if self._tree is None:
            return
        for item in self._tree.get_children():
            self._tree.delete(item)
        root_id = self._insert_value("", root_label, data)
        if root_id:
            self._tree.item(root_id, open=True)
        self._tree.see(root_id)
        self._tree.focus_set()
        self._tree.update_idletasks()

    def _insert_value(
        self,
        parent: str,
        key: str,
        value: Any,
    ) -> str:
        """Insert a value into the tree; return the new item id."""
        if self._tree is None:
            return ""

        if isinstance(value, dict):
            display_key = key if key else "(root)"
            item_id = self._tree.insert(
                parent,
                tk.END,
                text=display_key,
                values=("{}",),
                tags=("object",),
                open=False,
            )
            for k, v in value.items():
                self._insert_value(item_id, k, v)
            return item_id

        if isinstance(value, list):
            display_key = key if key else "(root)"
            item_id = self._tree.insert(
                parent,
                tk.END,
                text=display_key,
                values=(f"[{len(value)} items]",),
                tags=("array",),
                open=False,
            )
            for i, v in enumerate(value):
                self._insert_value(item_id, str(i), v)
            return item_id

        tag = "string"
        if value is None:
            display = "null"
            tag = "null"
        elif isinstance(value, bool):
            display = str(value).lower()
            tag = "boolean"
        elif isinstance(value, (int, float)):
            display = str(value)
            tag = "number"
        else:
            display = str(value)
            if len(display) > 60:
                display = display[:57] + "..."

        item_id = self._tree.insert(
            parent,
            tk.END,
            text=key,
            values=(display,),
            tags=(tag,),
        )
        return item_id

    def _on_expand_all(self) -> None:
        """Expand all tree nodes."""
        if self._tree is None:
            return
        def expand(item: str) -> None:
            self._tree.item(item, open=True)
            for child in self._tree.get_children(item):
                expand(child)
        for item in self._tree.get_children():
            expand(item)

    def _on_collapse_all(self) -> None:
        """Collapse all tree nodes."""
        if self._tree is None:
            return
        def collapse(item: str) -> None:
            self._tree.item(item, open=False)
            for child in self._tree.get_children(item):
                collapse(child)
        for item in self._tree.get_children():
            collapse(item)

    def run(self) -> None:
        """Start the main event loop."""
        self._root.mainloop()
