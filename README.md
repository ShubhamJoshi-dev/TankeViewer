# Python Desktop App

A simple desktop application with a JSON viewer. Open JSON files and browse them in an organized tree view.

## Features

- Open JSON files via File dialog
- Tree view with expand/collapse (click the arrows)
- Expand All / Collapse All buttons
- Key and value columns; types shown with different colors (object, array, string, number, boolean, null)
- Status bar shows the path of the loaded file

## Structure

```
PythonDesktopApp/
  main.py              # Entry point
  requirements.txt
  src/
    core/
      app.py           # Config
    ui/
      json_viewer.py   # JSON tree viewer window
      main_window.py   # (optional) original sample window
```

## Run

From the project root:

```bash
python main.py
```

## Requirements

- Python 3.8+
- Tkinter (included with standard Python on most systems)
