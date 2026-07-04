from langchain_ollama import ChatOllama # type: ignore
from langchain_core.prompts import ChatPromptTemplate
from src.agents.state import AgentState
import json
import os
import re
import subprocess

llm = ChatOllama(model="qwen3:4b", temperature=0.1, keep_alive=0)

PACKAGE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Node.js package manager for a React frontend project. Given the
project's spec, its planned dependencies, and previews of the generated component code (which
may import extra libraries the planner didn't originally list), determine the FINAL, complete
list of npm dependencies this project needs to build and run successfully.

Respond ONLY in valid JSON, no other text, in this exact format:
{{
  "dependencies": {{"react": "^18.2.0", "react-dom": "^18.2.0", "react-router-dom": "^6.22.0"}},
  "devDependencies": {{"vite": "^5.0.0", "tailwindcss": "^3.4.0", "autoprefixer": "^10.4.0", "postcss": "^8.4.0"}}
}}

Rules:
- Only include packages that are actually imported/used, or required for the chosen framework and styling library.
- Use realistic, commonly-used version ranges (e.g. "^18.2.0"), never "latest".
- Do not invent unrelated packages."""),
    ("user", """Spec: {spec}
Planned dependencies: {planned_dependencies}
Generated files (path -> code preview): {generated_files}""")
])

OUTPUT_DIR = "generated_project"


def _strip_code_fences(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def _write_package_json(dependencies: dict, dev_dependencies: dict):
    package_json = {
        "name": "frontforge-generated-app",
        "private": True,
        "version": "0.0.1",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "dependencies": dependencies,
        "devDependencies": dev_dependencies
    }
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_path = os.path.join(OUTPUT_DIR, "package.json")
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(package_json, f, indent=2)


def _run_npm_install() -> tuple[bool, str]:
    """Actually executes npm install inside the generated project folder.
    This is the action that makes this component an agent, not a generator."""
    try:
        result = subprocess.run(
            ["npm", "install"],
            cwd=OUTPUT_DIR,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stderr
    except FileNotFoundError:
        return False, "npm not found on this machine — is Node.js installed and on PATH?"
    except subprocess.TimeoutExpired:
        return False, "npm install timed out after 300 seconds"


def package_manager_node(state: AgentState) -> AgentState:
    chain = PACKAGE_PROMPT | llm

    spec = state.get("spec") or {}
    planned_dependencies = state.get("dependencies") or []
    generated_files = state.get("generated_files") or {}

    # Send only short previews of each file, not full code — keeps the prompt small
    file_previews = {path: code[:300] for path, code in generated_files.items()}

    try:
        result = chain.invoke({
            "spec": json.dumps(spec),
            "planned_dependencies": json.dumps(planned_dependencies),
            "generated_files": json.dumps(file_previews)
        })
        parsed = json.loads(_strip_code_fences(result.content))
    except Exception as e:
        state["errors"].append(f"Package Manager agent returned invalid JSON: {str(e)}")
        parsed = {
            "dependencies": {"react": "^18.2.0", "react-dom": "^18.2.0"},
            "devDependencies": {"vite": "^5.0.0"}
        }

    dependencies = parsed.get("dependencies", {})
    dev_dependencies = parsed.get("devDependencies", {})

    _write_package_json(dependencies, dev_dependencies)

    install_success, install_log = _run_npm_install()
    if not install_success:
        state["errors"].append(f"npm install failed: {install_log[:500]}")

    state["dependencies"] = list({**dependencies, **dev_dependencies}.keys())
    state["install_success"] = install_success

    return state