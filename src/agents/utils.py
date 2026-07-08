# src/agents/utils.py
"""
Shared helpers for cleaning raw LLM output before parsing/writing.
"""

import re


def strip_think_tags(raw: str) -> str:
    """Removes Qwen3's optional <think>...</think> reasoning block, if present."""
    return re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()


def strip_code_fences(raw: str) -> str:
    """Removes ```jsx / ```json / ``` fences if the model adds them despite instructions."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def clean_llm_output(raw: str) -> str:
    """Full cleanup pipeline: strip <think> block, then strip code fences."""
    return strip_code_fences(strip_think_tags(raw))