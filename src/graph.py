# src/graph.py
"""
LangGraph orchestration for the FrontForge pipeline.

Sequential path:
  clarification -> planner -> ui_architect -> scaffold (action, no LLM)
  -> component -> styling -> package_manager -> reviewer

Conditional edge:
  reviewer routes back to component for regeneration, up to MAX_RETRIES times,
  if the build fails or review does not pass. After MAX_RETRIES it terminates
  regardless, and review_report/errors explain why.
"""

from langgraph.graph import StateGraph, END

from src.agents.state import AgentState
from src.agents.clarification_agent import clarification_node
from src.agents.planner_agent import planner_node
from src.agents.ui_architect_agent import ui_architect_node
from src.agents.scaffold_agent import scaffold_node
from src.agents.component_agent import component_node
from src.agents.styling_agent import styling_node
from src.agents.package_manager_agent import package_manager_node
from src.agents.reviewer_agent import reviewer_node

MAX_RETRIES = 2


def route_after_review(state: AgentState) -> str:
    if state.get("review_passed"):
        return "done"
    if state.get("retry_count", 0) < MAX_RETRIES:
        return "retry"
    return "done"  # exhausted retries — review_report/errors carry the reason


def increment_retry_node(state: AgentState) -> AgentState:
    state["retry_count"] = state.get("retry_count", 0) + 1
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("clarification", clarification_node)
    graph.add_node("planner", planner_node)
    graph.add_node("ui_architect", ui_architect_node)
    graph.add_node("scaffold", scaffold_node)
    graph.add_node("component", component_node)
    graph.add_node("styling", styling_node)
    graph.add_node("package_manager", package_manager_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("increment_retry", increment_retry_node)

    graph.set_entry_point("clarification")

    graph.add_edge("clarification", "planner")
    graph.add_edge("planner", "ui_architect")
    graph.add_edge("ui_architect", "scaffold")
    graph.add_edge("scaffold", "component")
    graph.add_edge("component", "styling")
    graph.add_edge("styling", "package_manager")
    graph.add_edge("package_manager", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "retry": "increment_retry",
            "done": END,
        }
    )
    graph.add_edge("increment_retry", "component")

    return graph.compile()