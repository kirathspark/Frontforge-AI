from src.agents.clarification_agent import clarification_node
from src.agents.planner_agent import planner_node
from src.agents.ui_architect_agent import ui_architect_node

state = {
    "user_prompt": input("Enter your prompt: "),
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

state = clarification_node(state)
state = planner_node(state)
state = ui_architect_node(state)

print(state)