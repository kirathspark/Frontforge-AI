# src/agents/scaffold_agent.py
"""
Action Agent — no LLM call, no text generation. Consumes the folder_structure
already produced by the UI Architect agent and materializes a real, working
project skeleton on disk:
  1. wipes/recreates the output directory
  2. writes the Vite + Tailwind scaffold files
  3. creates every folder in the plan
  4. writes a stub file for every planned component

This is what turns the pipeline into an agent system rather than a text
generator: this node's success is verified by the filesystem, not by JSON
parsing succeeding.
"""

from src.agents.state import AgentState
from src.actions.filesystem_actions import (
    OUTPUT_DIR,
    reset_output_dir,
    scaffold_base_project,
    create_folders,
    write_stub_files,
)


def scaffold_node(state: AgentState) -> AgentState:
    folder_structure = state.get("folder_structure") or {}
    folders = folder_structure.get("folders", [])
    files = folder_structure.get("files", [])

    try:
        reset_output_dir(OUTPUT_DIR)
        scaffold_base_project(OUTPUT_DIR)
        create_folders(OUTPUT_DIR, folders)
        write_stub_files(OUTPUT_DIR, files)
    except OSError as e:
        state["errors"].append(f"Scaffold agent failed: {str(e)}")

    return state