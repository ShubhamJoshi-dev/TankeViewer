from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.app import AppConfig


# Light theme so keys/values and type colors stay readable
BG_WINDOW = "#f5f5f5"
BG_TOOLBAR = "#e8e8e8"
BG_TREE = "#ffffff"
BG_HEADER = "#e0e0e0"
BG_STATUS = "#eaeaea"
FG_LABEL = "#333333"


def _tree_font() -> tuple[str, int]:
 
    try:
        families = list(tk.font.families())
        for name in ("SF Mono", "Menlo", "Consolas", "Monaco", "DejaVu Sans Mono"):
            if name in families:
                return (name, 12)
    except Exception:
        pass
    return ("TkDefaultFont", 11)


class JsonViewer:


    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._root = tk.Tk()
        self._root.title(config.title)
        self._root.geometry(f"{config.width}x{config.height}")
        self._root.minsize(500, 400)
        self._root.configure(bg=BG_WINDOW)
        self._tree: ttk.Treeview | None = None
        self._build_ui()

    def _build_ui(self) -> None:
       
        main = tk.Frame(self._root, bg=BG_WINDOW, padx=12, pady=12)
        main.pack(fill=tk.BOTH, expand=True)

        toolbar = tk.Frame(main, bg=BG_TOOLBAR, pady=10, padx=12)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        btn_open = tk.Button(
            toolbar,
            text="Open",
            command=self._on_open,
            font=_tree_font(),
            relief=tk.FLAT,
            bg=BG_TOOLBAR,
            fg=FG_LABEL,
            activebackground=BG_TREE,
            activeforeground=FG_LABEL,
            cursor="hand2",
            padx=14,
            pady=6,
        )
        btn_open.pack(side=tk.LEFT, padx=(0, 6))
        btn_expand = tk.Button(
            toolbar,
            text="Expand All",
            command=self._on_expand_all,
            font=_tree_font(),
            relief=tk.FLAT,
            bg=BG_TOOLBAR,
            fg=FG_LABEL,
            activebackground=BG_TREE,
            activeforeground=FG_LABEL,
            cursor="hand2",
            padx=14,
            pady=6,
        )
        btn_expand.pack(side=tk.LEFT, padx=(0, 6))
        btn_collapse = tk.Button(
            toolbar,
            text="Collapse All",
            command=self._on_collapse_all,
            font=_tree_font(),
            relief=tk.FLAT,
            bg=BG_TOOLBAR,
            fg=FG_LABEL,
            activebackground=BG_TREE,
            activeforeground=FG_LABEL,
            cursor="hand2",
            padx=14,
            pady=6,
        )
        btn_collapse.pack(side=tk.LEFT)

        tree_container = tk.Frame(main, bg=BG_WINDOW)
        tree_container.pack(fill=tk.BOTH, expand=True)

        tree_frame = tk.Frame(tree_container, bg=BG_TREE)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(tree_frame, bg=BG_TREE)
        scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, bg=BG_TREE)

        self._tree = ttk.Treeview(
            tree_frame,
            columns=("value",),
            show="tree headings",
            height=22,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode="browse",
        )
        self._tree.heading("#0", text="Key")
        self._tree.heading("value", text="Value")
        self._tree.column("#0", minwidth=260, width=320)
        self._tree.column("value", minwidth=200, width=320)
        self._configure_style()
        self._configure_tags()

        scroll_y.config(command=self._tree.yview)
        scroll_x.config(command=self._tree.xview)

        self._tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        status_frame = tk.Frame(main, bg=BG_STATUS, pady=8, padx=12)
        status_frame.pack(fill=tk.X, pady=(8, 0))
        self._status = tk.Label(
            status_frame,
            text="Open a JSON file to start.",
            font=_tree_font(),
            bg=BG_STATUS,
            fg="#666666",
            anchor=tk.W,
        )
        self._status.pack(fill=tk.X)

    def _configure_style(self) -> None:
      
        style = ttk.Style()
        style.configure(
            "Json.Treeview",
            background=BG_TREE,
            foreground=FG_LABEL,
            fieldbackground=BG_TREE,
            rowheight=24,
            font=_tree_font(),
        )
        style.configure(
            "Json.Treeview.Heading",
            background=BG_HEADER,
            foreground=FG_LABEL,
            font=_tree_font(),
        )
        style.map(
            "Json.Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "#ffffff")],
        )
        self._tree.configure(style="Json.Treeview")

    def _configure_tags(self) -> None:
      
        if self._tree is None:
            return
        self._tree.tag_configure("object", foreground="#1d4ed8")
        self._tree.tag_configure("array", foreground="#15803d")
        self._tree.tag_configure("string", foreground="#1f2937")
        self._tree.tag_configure("number", foreground="#c2410c")
        self._tree.tag_configure("boolean", foreground="#7c3aed")
        self._tree.tag_configure("null", foreground="#6b7280")

    def _on_open(self) -> None:

        path = filedialog.askopenfilename(
            title="Open JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        self._load_file(Path(path))

    def _load_file(self, path: Path) -> None:

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
       
        if self._tree is None:
            return
        def expand(item: str) -> None:
            self._tree.item(item, open=True)
            for child in self._tree.get_children(item):
                expand(child)
        for item in self._tree.get_children():
            expand(item)

    def _on_collapse_all(self) -> None:
  
        if self._tree is None:
            return
        def collapse(item: str) -> None:
            self._tree.item(item, open=False)
            for child in self._tree.get_children(item):
                collapse(child)
        for item in self._tree.get_children():
            collapse(item)

    def run(self) -> None:
       
        self._root.mainloop()
