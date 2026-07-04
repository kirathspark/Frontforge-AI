from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.agents.state import AgentState
import json
import os
import re

llm = ChatOllama(model="qwen3:4b", temperature=0.3, keep_alive=0)

COMPONENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a React developer generating a single component file.
Use the given file path, component name, and project spec to write clean, working JSX code.
Use functional components with hooks (no class components). Use Tailwind CSS utility classes
for styling if styling is "Tailwind", otherwise plain CSS class names. Use hardcoded/placeholder
data wherever real backend data would normally be needed — never fetch from an external API.
If documentation snippets are provided, follow their patterns and correct class/prop names.

Output ONLY the raw JSX/TSX code for this one file. No explanation. No markdown code fences."""),
    ("user", """File path: {file_path}
Component name: {component_name}
Project spec: {spec}
Page/route this belongs to (if any): {page_context}
Relevant documentation (may be empty): {doc_context}""")
])

OUTPUT_DIR = "generated_project"


def _strip_code_fences(raw: str) -> str:
    """Removes ```jsx / ```tsx / ``` fences if the model adds them despite instructions."""
    cleaned = raw.strip()
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def _retrieve_docs(query: str) -> str:
    """Optional RAG hook. Returns an empty string if the RAG module isn't built yet,
    so this agent still works standalone before rag/retriever.py exists."""
    try:
        from rag.retriever import retrieve
        chunks = retrieve(query, top_k=3)
        return "\n\n".join(chunks)
    except Exception:
        return ""


def component_node(state: AgentState) -> AgentState:
    chain = COMPONENT_PROMPT | llm
    folder_structure = state.get("folder_structure") or {}
    files = folder_structure.get("files", [])
    project_plan = state.get("project_plan") or {}
    spec = state.get("spec") or {}

    generated_files = {}

    for file_entry in files:
        file_path = file_entry.get("path")
        component_name = file_entry.get("component", "Component")

        if not file_path:
            continue

        page_context = next(
            (p for p in project_plan.get("pages", [])
             if component_name in p.get("components", []) or p.get("name") == component_name),
            None
        )

        doc_context = _retrieve_docs(f"React {component_name} {spec.get('styling', 'Tailwind')} example")

        try:
            result = chain.invoke({
                "file_path": file_path,
                "component_name": component_name,
                "spec": json.dumps(spec),
                "page_context": json.dumps(page_context) if page_context else "none",
                "doc_context": doc_context
            })
            code = _strip_code_fences(result.content)

            full_path = os.path.join(OUTPUT_DIR, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code)

            generated_files[file_path] = code

        except Exception as e:
            state["errors"].append(f"Component agent failed on {file_path}: {str(e)}")

    state["generated_files"] = generated_files

    return state