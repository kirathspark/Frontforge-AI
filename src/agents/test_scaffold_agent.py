# test_scaffold_agent.py
import os
import shutil

from src.agents.scaffold_agent import scaffold_node
from src.agents.state import AgentState
from src.actions.filesystem_actions import OUTPUT_DIR

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
    "retry_count": 0,
    "human_intervention_count": 0,
    "errors": []
}

result = scaffold_node(test_state)

print("Errors:", result["errors"] if result["errors"] else "none")

# Real assertions — this agent has no LLM, so its correctness is fully checkable
expected_paths = [
    "index.html",
    "vite.config.js",
    "tailwind.config.js",
    "postcss.config.js",
    "src/main.jsx",
    "src/App.jsx",
    "src/styles/global.css",
    "src/pages/Home.jsx",
    "src/pages/Projects.jsx",
    "src/components/shared/Navbar.jsx",
    "src/components/shared/Footer.jsx",
]

missing = []
for rel_path in expected_paths:
    full_path = os.path.join(OUTPUT_DIR, rel_path)
    if not os.path.isfile(full_path):
        missing.append(full_path)

if missing:
    print("\nFAIL — missing expected files:")
    for m in missing:
        print(f"  - {m}")
else:
    print(f"\nPASS — all {len(expected_paths)} expected files created under '{OUTPUT_DIR}/'")

# Sanity-check a stub file actually contains the component name
navbar_path = os.path.join(OUTPUT_DIR, "src/components/shared/Navbar.jsx")
with open(navbar_path) as f:
    content = f.read()
assert "Navbar" in content, "Navbar stub does not reference component name"
print("PASS — stub file content sanity check")

# Clean up so repeated test runs start fresh
# shutil.rmtree(OUTPUT_DIR, ignore_errors=True)