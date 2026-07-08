from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.agents.state import AgentState
import json

llm = ChatOllama(model="qwen3:4b", temperature=0.2, keep_alive="5m")

CLARIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a requirements analyst for a frontend generation system.
Given a user's app request, decide if it's specific enough to build directly,
or if you need to ask clarifying questions about: framework choice (React/Next.js),
styling library (Tailwind/Bootstrap/Shadcn), theme (light/dark/colorful), and complexity
(number of pages, features).

Respond ONLY in valid JSON, no other text, in this exact format:
{{
  "needs_clarification": true or false,
  "questions": ["question1", "question2"],
  "spec": {{
    "framework": "...",
    "styling": "...",
    "theme": "...",
    "pages": ["..."],
    "complexity": "simple/medium/complex"
  }}
}}

If needs_clarification is true, fill spec with your best-guess defaults anyway
(the system will proceed with defaults if the user doesn't respond in time)."""),
    ("user", "{user_prompt}")
])


def clarification_node(state: AgentState) -> AgentState:
    chain = CLARIFICATION_PROMPT | llm
    result = chain.invoke({"user_prompt": state["user_prompt"]})

    try:
        parsed = json.loads(result.content)
    except json.JSONDecodeError:
        state["errors"].append("Clarification agent returned invalid JSON")
        parsed = {
            "needs_clarification": False,
            "questions": [],
            "spec": {
                "framework": "React",
                "styling": "Tailwind",
                "theme": "light",
                "pages": ["Home"],
                "complexity": "simple"
            }
        }

    state["clarification_questions"] = parsed.get("questions", [])
    state["spec"] = parsed.get("spec", {})

    if parsed.get("needs_clarification"):
        state["human_intervention_count"] += 1

    return state