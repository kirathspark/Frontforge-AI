from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.agents.state import AgentState
import json
import os
import re

# llm = ChatOllama(model="qwen3:4b", temperature=0.2, keep_alive="5m")
# styling_agent.py
llm = ChatOllama(model="qwen3:4b", temperature=0.2, keep_alive="5m", num_predict=1200)

STYLING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a frontend styling specialist. You are given the existing JSX code for
one component, along with the project's styling library and theme. Rewrite the SAME component,
keeping its structure, logic, and props exactly the same, but ensure its styling is:
- Consistent with the given theme (light/dark/colorful)
- Using idiomatic Tailwind CSS utility classes if styling is "Tailwind" (spacing, colors,
  typography, responsive prefixes like sm:/md:/lg:), or clean plain CSS class names otherwise
- Visually consistent with a professional, modern layout (proper spacing, alignment, contrast)

Do NOT change component logic, state, props, or JSX structure — only touch className/style values.
Output ONLY the raw JSX/TSX code for this one file. No explanation. No markdown code fences."""),
    ("user", """Component code:
{component_code}

Styling library: {styling}
Theme: {theme}""")
])

GLOBAL_STYLE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a frontend styling specialist writing the global stylesheet for a React
project. Given the styling library and theme, output a single global CSS file that defines base
styles, theme colors (as CSS variables), and typography defaults.

Output ONLY raw CSS. No explanation. No markdown code fences."""),
    ("user", "Styling library: {styling}\nTheme: {theme}")
])

OUTPUT_DIR = "generated_project"


def _strip_code_fences(raw: str) -> str:
    """Removes ```jsx / ```css / ``` fences if the model adds them despite instructions."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def _write_file(relative_path: str, content: str):
    full_path = os.path.join(OUTPUT_DIR, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)


def styling_node(state: AgentState) -> AgentState:
    component_chain = STYLING_PROMPT | llm
    global_chain = GLOBAL_STYLE_PROMPT | llm

    spec = state.get("spec") or {}
    styling = spec.get("styling", "Tailwind")
    theme = spec.get("theme", "light")
    generated_files = state.get("generated_files") or {}

    updated_files = {}

    # Re-style every existing component file
    for file_path, code in generated_files.items():
        print(f">>> Styling agent styling: {file_path}", flush=True)
        try:
            result = component_chain.invoke({
                "component_code": code,
                "styling": styling,
                "theme": theme
            })
            styled_code = _strip_code_fences(result.content)
            _write_file(file_path, styled_code)
            updated_files[file_path] = styled_code

        except Exception as e:
            state["errors"].append(f"Styling agent failed on {file_path}: {str(e)}")
            updated_files[file_path] = code  # keep the unstyled version rather than lose it

    # Write one global stylesheet shared by the whole app
    try:
        global_result = global_chain.invoke({"styling": styling, "theme": theme})
        global_css = _strip_code_fences(global_result.content)
        global_path = "src/styles/global.css"
        _write_file(global_path, global_css)
        updated_files[global_path] = global_css

    except Exception as e:
        state["errors"].append(f"Styling agent failed on global stylesheet: {str(e)}")

    state["generated_files"] = updated_files
    state["styling_applied"] = True

    return state