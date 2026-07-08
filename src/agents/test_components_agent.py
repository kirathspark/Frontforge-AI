import json

from src.agents.component_agent import component_node
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
    # Use real UI Architect output here (or paste the JSON test_ui_architect.py printed)
    "folder_structure": {
        "folders": ["src", "src/components", "src/components/shared", "src/pages"],
        "files": [
            {"path": "src/pages/Home.jsx", "type": "page", "component": "Home"},
            {"path": "src/pages/Projects.jsx", "type": "page", "component": "Projects"},
            {"path": "src/components/shared/Navbar.jsx", "type": "component", "component": "Navbar"},
            {"path": "src/components/shared/Footer.jsx", "type": "component", "component": "Footer"}
        ],
        "naming_convention": "PascalCase for components, camelCase for utility files",
        "entry_point": "src/main.jsx"
    },
    "generated_files": {},
    "styling_applied": False,
    "dependencies": [],
    "install_success": None,
    "review_report": None,
    "review_passed": None,
    "human_intervention_count": 0,
    "errors": []
}

result = component_node(test_state)

# Don't dump full file contents into the terminal — just show which files were generated
print("Generated files:")
for path in result["generated_files"]:
    print(f"  - {path}")

if result["errors"]:
    print("\nErrors:")
    for err in result["errors"]:
        print(f"  - {err}")

print("\nFull generated_files JSON saved to test_output.json")
with open("test_output.json", "w") as f:
    json.dump(result["generated_files"], f, indent=2)