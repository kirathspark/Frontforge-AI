import json

from src.agents.clarification_agent import clarification_node
from src.agents.state import AgentState

test_state: AgentState = {
    "user_prompt": "build me a simple portfolio website with a home and projects page",
    "clarification_questions": [],
    "clarification_answers": [],
    "spec": None,
    "project_plan": None,
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

result = clarification_node(test_state)
print(json.dumps(result, indent=2))