from langchain_ollama import ChatOllama # type: ignore
from langchain_core.prompts import ChatPromptTemplate
from src.agents.state import AgentState
import json
import os
import re
import subprocess

llm = ChatOllama(model="qwen3:4b", temperature=0.2, keep_alive=0)

REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior code reviewer for a React frontend project. You are given
whether the build succeeded, the build log (if it failed), the project spec, and previews of
the generated files. Assess the codebase for correctness, consistency, and completeness.

Respond ONLY in valid JSON, no other text, in this exact format:
{{
  "review_passed": true or false,
  "issues": ["issue 1", "issue 2"],
  "summary": "2-3 sentence plain-language summary of the codebase's state"
}}

Rules:
- If the build failed, review_passed MUST be false, and issues must explain the build error
  in plain language plus which file is likely responsible.
- If the build succeeded, still check the file previews for missing components, inconsistent
  naming, or pages referenced in the spec but not present, and set review_passed to false if
  something important is clearly missing.
- Be specific and factual. Do not invent problems that aren't evidenced by the log or code."""),
    ("user", """Build succeeded: {build_success}
Build log (empty if build succeeded): {build_log}
Spec: {spec}
Generated files (path -> code preview): {generated_files}""")
])

OUTPUT_DIR = "generated_project"
MAX_RETRIES = 2


def _strip_code_fences(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def _run_build() -> tuple[bool, str]:
    """Actually executes npm run build inside the generated project folder.
    This is the action that makes this component an agent, not a generator."""
    if not os.path.isdir(OUTPUT_DIR):
        return False, f"Output directory '{OUTPUT_DIR}' does not exist — nothing to build."
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=OUTPUT_DIR,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stderr
    except FileNotFoundError:
        return False, "npm not found on this machine — is Node.js installed and on PATH?"
    except subprocess.TimeoutExpired:
        return False, "npm run build timed out after 300 seconds"


def reviewer_node(state: AgentState) -> AgentState:
    chain = REVIEW_PROMPT | llm

    spec = state.get("spec") or {}
    generated_files = state.get("generated_files") or {}
    file_previews = {path: code[:300] for path, code in generated_files.items()}

    build_success, build_log = _run_build()

    try:
        result = chain.invoke({
            "build_success": build_success,
            "build_log": build_log[:2000] if not build_success else "",
            "spec": json.dumps(spec),
            "generated_files": json.dumps(file_previews)
        })
        parsed = json.loads(_strip_code_fences(result.content))
    except Exception as e:
        state["errors"].append(f"Reviewer agent returned invalid JSON: {str(e)}")
        parsed = {
            "review_passed": build_success,
            "issues": [] if build_success else ["Build failed; reviewer could not analyze log."],
            "summary": "Automated review failed; falling back to raw build result."
        }

    # Build success is a hard requirement — the LLM can only fail a passing build, never pass a failed one
    review_passed = build_success and parsed.get("review_passed", True)

    review_report = parsed.get("summary", "")
    issues = parsed.get("issues", [])
    if issues:
        review_report += "\n\nIssues found:\n" + "\n".join(f"- {issue}" for issue in issues)

    state["review_report"] = review_report
    state["review_passed"] = review_passed

    if not review_passed:
        state["errors"].append(f"Review failed: {review_report[:300]}")

    return state