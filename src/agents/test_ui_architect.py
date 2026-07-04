import json

from src.agents.ui_architect_agent import ui_architect_node
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
    "folder_structure": None,
    "generated_files": {},
    "styling_applied": False,
    "dependencies": [],
    "install_success": None,
    "review_report": None,
    "review_passed": None,
    "human_intervention_count": 0,
    "errors": []
}

result = ui_architect_node(test_state)
print(json.dumps(result, indent=2))