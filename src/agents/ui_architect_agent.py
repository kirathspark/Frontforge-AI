from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.agents.state import AgentState
import json

llm = ChatOllama(model="qwen3:4b", temperature=0.2, keep_alive=0)

UI_ARCHITECT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior frontend architect designing the folder and file structure
for a React project. Given a project plan (pages, shared components, routing, dependencies),
produce a folder structure specification.

Respond ONLY in valid JSON, no other text, in this exact format:
{{
  "folders": ["src", "src/components", "src/components/shared", "src/pages", "src/routes", "src/assets", "src/styles"],
  "files": [
    {{"path": "src/pages/Home.jsx", "type": "page", "component": "Home"}},
    {{"path": "src/components/shared/Navbar.jsx", "type": "component", "component": "Navbar"}}
  ],
  "naming_convention": "PascalCase for components, camelCase for utility files",
  "entry_point": "src/main.jsx"
}}

Rules:
- Every page in project_plan.pages must map to exactly one file under src/pages/.
- Every entry in project_plan.shared_components must map to one file under src/components/shared/.
- Any page-specific (non-shared) component must map to a file under src/components/<PageName>/.
- Do not invent pages or components that are not present in the project plan.
- Keep the structure idiomatic for a Vite + React project."""),
    ("user", "{project_plan}")
])


def ui_architect_node(state: AgentState) -> AgentState:
    chain = UI_ARCHITECT_PROMPT | llm
    result = chain.invoke({"project_plan": json.dumps(state["project_plan"])})

    try:
        parsed = json.loads(result.content)
    except json.JSONDecodeError:
        state["errors"].append("UI Architect agent returned invalid JSON")
        parsed = {
            "folders": ["src", "src/components", "src/components/shared", "src/pages"],
            "files": [],
            "naming_convention": "PascalCase for components, camelCase for utility files",
            "entry_point": "src/main.jsx"
        }

    state["folder_structure"] = parsed

    return state