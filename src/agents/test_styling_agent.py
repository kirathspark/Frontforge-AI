import json

from src.agents.styling_agent import styling_node
from src.agents.state import AgentState

test_state: AgentState = {
    "user_prompt": "build me a simple portfolio website with a home and projects page",
    "clarification_questions": [],
    "clarification_answers": [],
    "spec": {
        "framework": "React",
        "styling": "Tailwind",
        "theme": "light",
        "pages": ["home", "projects"],
        "complexity": "simple"
    },
    "project_plan": {
        "pages": [
            {"name": "Home", "route": "/", "components": ["Navbar", "Hero", "Footer"]},
            {"name": "Projects", "route": "/projects", "components": ["Navbar", "ProjectCard", "Footer"]}
        ],
        "shared_components": ["Navbar", "Footer"],
        "routing": "react-router-dom",
        "dependencies": ["react", "react-router-dom", "tailwindcss"]
    },
    "folder_structure": {
        "folders": ["src", "src/components", "src/components/shared", "src/pages"],
        "files": [
            {"path": "src/pages/Home.jsx", "type": "page", "component": "Home"},
            {"path": "src/components/shared/Navbar.jsx", "type": "component", "component": "Navbar"}
        ],
        "naming_convention": "PascalCase for components, camelCase for utility files",
        "entry_point": "src/main.jsx"
    },
    # Use real Component Agent output here (or paste from test_output.json)
    "generated_files": {
        "src/pages/Home.jsx": """export default function Home() {
  return (
    <div>
      <h1>Welcome</h1>
      <p>This is the home page.</p>
    </div>
  );
}""",
        "src/components/shared/Navbar.jsx": """export default function Navbar() {
  return (
    <nav>
      <a href="/">Home</a>
      <a href="/projects">Projects</a>
    </nav>
  );
}"""
    },
    "styling_applied": False,
    "dependencies": [],
    "install_success": None,
    "review_report": None,
    "review_passed": None,
    "human_intervention_count": 0,
    "errors": []
}

result = styling_node(test_state)

print(f"Styling applied: {result['styling_applied']}")
print("\nStyled files:")
for path in result["generated_files"]:
    print(f"  - {path}")

if result["errors"]:
    print("\nErrors:")
    for err in result["errors"]:
        print(f"  - {err}")

print("\nFull styled output saved to test_styled_output.json")
with open("test_styled_output.json", "w") as f:
    json.dump(result["generated_files"], f, indent=2)