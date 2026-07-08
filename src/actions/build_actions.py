# src/actions/build_actions.py
"""
Pure action functions that invoke external processes (npm). No LLM involved.
Shared by Package Manager Agent (npm install) and Reviewer Agent (npm run build)
so subprocess logic isn't duplicated across agent files.
"""

import os
import subprocess
from typing import Tuple


def run_npm_install(root: str, timeout: int = 300) -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            ["npm", "install"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stderr
    except FileNotFoundError:
        return False, "npm not found on this machine — is Node.js installed and on PATH?"
    except subprocess.TimeoutExpired:
        return False, f"npm install timed out after {timeout} seconds"


def run_npm_build(root: str, timeout: int = 300) -> Tuple[bool, str]:
    if not os.path.isdir(root):
        return False, f"Output directory '{root}' does not exist — nothing to build."
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stderr
    except FileNotFoundError:
        return False, "npm not found on this machine — is Node.js installed and on PATH?"
    except subprocess.TimeoutExpired:
        return False, f"npm run build timed out after {timeout} seconds"