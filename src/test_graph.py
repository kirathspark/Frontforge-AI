# test_graph.py
import shutil

from src.graph import build_graph
from src.actions.filesystem_actions import OUTPUT_DIR

test_prompt = "Build me a simple portfolio website with a home page and a projects page"

initial_state = {
    "user_prompt": test_prompt,
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

app = build_graph()

print(f"Running full pipeline for prompt: '{test_prompt}'")
print("(This will take a while on CPU — clarification, planner, ui_architect, component,")
print("styling, and reviewer all make LLM calls; package_manager + reviewer run real npm commands.)\n")

final_state = app.invoke(initial_state)

print("\n=== PIPELINE RESULT ===")
print(f"Spec: {final_state.get('spec')}")
print(f"Pages planned: {[p.get('name') for p in (final_state.get('project_plan') or {}).get('pages', [])]}")
print(f"Files generated: {list(final_state.get('generated_files', {}).keys())}")
print(f"Styling applied: {final_state.get('styling_applied')}")
print(f"Install success: {final_state.get('install_success')}")
print(f"Review passed: {final_state.get('review_passed')}")
print(f"Retries used: {final_state.get('retry_count')}")
print(f"Human intervention count: {final_state.get('human_intervention_count')}")

if final_state.get("errors"):
    print("\nErrors encountered during run:")
    for err in final_state["errors"]:
        print(f"  - {err}")
else:
    print("\nNo errors recorded.")

print(f"\nReview report:\n{final_state.get('review_report')}")

# Uncomment to clean up the generated project after inspecting it manually:
# shutil.rmtree(OUTPUT_DIR, ignore_errors=True)