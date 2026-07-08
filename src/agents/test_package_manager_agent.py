import json

from src.agents.package_manager_agent import package_manager_node
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
    # Use real Styling Agent output here (or paste from test_styled_output.json)
    "generated_files": {
        "src/pages/Home.jsx": """export default function Home() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">Welcome</h1>
      <p className="text-gray-600">This is the home page.</p>
    </div>
  );
}""",
        "src/components/shared/Navbar.jsx": """export default function Navbar() {
  return (
    <nav className="flex gap-4 p-4 bg-white shadow">
      <a href="/">Home</a>
      <a href="/projects">Projects</a>
    </nav>
  );
}"""
    },
    "styling_applied": True,
    "dependencies": ["react", "react-router-dom", "tailwindcss"],
    "install_success": None,
    "review_report": None,
    "review_passed": None,
    "retry_count": 0,
    "human_intervention_count": 0,
    "errors": []
}

result = package_manager_node(test_state)

print(f"Install success: {result['install_success']}")
print(f"\nFinal dependencies list:")
for dep in result["dependencies"]:
    print(f"  - {dep}")

if result["errors"]:
    print("\nErrors:")
    for err in result["errors"]:
        print(f"  - {err}")

print(json.dumps(result, indent=2))