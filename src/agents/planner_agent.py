from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.agents.state import AgentState
import json

llm = ChatOllama(model="qwen3:4b", temperature=0.2, keep_alive="5m")

PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a frontend architect planning a React project structure.
Given a structured spec, produce a detailed project plan.

Respond ONLY in valid JSON, no other text, in this exact format:
{{
  "pages": [
    {{"name": "Home", "route": "/", "components": ["Navbar", "Hero", "Footer"]}}
  ],
  "shared_components": ["Navbar", "Footer"],
  "routing": "react-router-dom",
  "dependencies": ["react", "react-router-dom", "tailwindcss"]
}}

Base pages and components strictly on spec.pages and spec.complexity.
List every component each page needs, including shared ones like Navbar/Footer."""),
    ("user", "{spec}")
])


def planner_node(state: AgentState) -> AgentState:
    chain = PLANNER_PROMPT | llm
    result = chain.invoke({"spec": json.dumps(state["spec"])})

    try:
        parsed = json.loads(result.content)
    except json.JSONDecodeError:
        state["errors"].append("Planner agent returned invalid JSON")
        parsed = {"pages": [], "shared_components": [], "routing": "react-router-dom", "dependencies": ["react"]}

    state["project_plan"] = parsed
    state["dependencies"] = parsed.get("dependencies", [])

    return state