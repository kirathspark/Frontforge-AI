# from src.agents.clarification_agent import clarification_node
# from src.agents.planner_agent import planner_node
# from src.agents.ui_architect_agent import ui_architect_node

# state = {
#     "user_prompt": input("Enter your prompt: "),
#     "clarification_questions": [],
#     "clarification_answers": [],
#     "spec": None,
#     "project_plan": None,
#     "folder_structure": None,
#     "generated_files": {},
#     "styling_applied": False,
#     "dependencies": [],
#     "install_success": None,
#     "review_report": None,
#     "review_passed": None,
#     "human_intervention_count": 0,
#     "errors": []
# }

# state = clarification_node(state)
# state = planner_node(state)
# state = ui_architect_node(state)

# print(state)


# src/main.py
from src.graph import build_graph


def build_initial_state(user_prompt: str) -> dict:
    return {
        "user_prompt": user_prompt,
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
        "retry_count": 0,
        "human_intervention_count": 0,
        "errors": []
    }


def main():
    user_prompt = input("Enter your prompt: ")
    app = build_graph()
    final_state = app.invoke(build_initial_state(user_prompt))

    print("\n=== Pipeline finished ===")
    print(f"Review passed: {final_state.get('review_passed')}")
    print(f"Retries used: {final_state.get('retry_count')}")
    print(f"Human intervention count: {final_state.get('human_intervention_count')}")

    if final_state.get("errors"):
        print("\nErrors encountered:")
        for err in final_state["errors"]:
            print(f"  - {err}")

    print(f"\nReview report:\n{final_state.get('review_report')}")


if __name__ == "__main__":
    main()