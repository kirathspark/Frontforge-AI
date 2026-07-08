# src/actions/filesystem_actions.py
"""
Pure action functions — filesystem operations only, no LLM involved.
Called by action agents (e.g. scaffold_agent) to perform real, verifiable
side effects on disk. These functions are the "hands" of the system.
"""

import os
import shutil
from typing import List, Dict

OUTPUT_DIR = "generated_project"

VITE_CONFIG = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
"""

INDEX_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>FrontForge Generated App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

MAIN_JSX = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""

APP_JSX_STUB = """export default function App() {
  return <div>App placeholder — overwritten by Component Agent</div>;
}
"""

TAILWIND_CONFIG = """/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""

POSTCSS_CONFIG = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""


def reset_output_dir(root: str = OUTPUT_DIR) -> None:
    """Wipes any previous generation so every run starts from a clean, known state."""
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root, exist_ok=True)


def write_file(root: str, relative_path: str, content: str) -> str:
    full_path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path


def create_folders(root: str, folders: List[str]) -> List[str]:
    created = []
    for folder in folders:
        full_path = os.path.join(root, folder)
        os.makedirs(full_path, exist_ok=True)
        created.append(full_path)
    return created


def scaffold_base_project(root: str = OUTPUT_DIR) -> None:
    """
    Deterministically writes the minimal Vite + React + Tailwind scaffold
    (index.html, vite.config.js, tailwind config, main.jsx, global.css).

    We do NOT shell out to `npm create vite` here — that command is interactive
    and unreliable inside an unattended pipeline. Everything it would produce
    for a bare React template is a small, fixed set of files, so we write them
    ourselves. This keeps scaffold_node fully deterministic and testable.
    """
    write_file(root, "index.html", INDEX_HTML)
    write_file(root, "vite.config.js", VITE_CONFIG)
    write_file(root, "tailwind.config.js", TAILWIND_CONFIG)
    write_file(root, "postcss.config.js", POSTCSS_CONFIG)
    write_file(root, "src/main.jsx", MAIN_JSX)
    write_file(root, "src/App.jsx", APP_JSX_STUB)
    write_file(
        root,
        "src/styles/global.css",
        "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n"
    )


def write_stub_files(root: str, files: List[Dict]) -> List[str]:
    """
    Writes a placeholder file for every entry in the UI Architect's plan.
    This means Component Agent never has to guess a path or call makedirs
    itself — it only ever opens an existing file and overwrites it.
    """
    written = []
    for file_entry in files:
        path = file_entry.get("path")
        if not path:
            continue
        component = file_entry.get("component", "Component")
        stub = (
            f"export default function {component}() {{\n"
            f"  return <div>{component} placeholder</div>;\n"
            f"}}\n"
        )
        write_file(root, path, stub)
        written.append(path)
    return written