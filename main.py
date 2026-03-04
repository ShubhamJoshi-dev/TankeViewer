

from __future__ import annotations

import sys
from pathlib import Path


_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from src.core.app import AppConfig
from src.ui.json_viewer import JsonViewer


def main() -> None:

    config = AppConfig(title="JSON Viewer", width=720, height=500)
    window = JsonViewer(config)
    window.run()


if __name__ == "__main__":
    main()
