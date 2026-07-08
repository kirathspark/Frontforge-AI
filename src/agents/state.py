# from typing import TypedDict, List, Optional


# class AgentState(TypedDict):
    
#     user_prompt: str
#     clarification_questions: List[str]
#     clarification_answers: List[str]
#     spec: Optional[dict]  

    
#     project_plan: Optional[dict]  

    
#     folder_structure: Optional[dict]

    
#     generated_files: dict  

    
#     styling_applied: bool

    
#     dependencies: List[str]
#     install_success: Optional[bool]

    
#     review_report: Optional[str]
#     review_passed: Optional[bool]

    
#     human_intervention_count: int
#     errors: List[str]


# src/agents/state.py
from typing import TypedDict, List, Optional


class AgentState(TypedDict):

    user_prompt: str
    clarification_questions: List[str]
    clarification_answers: List[str]
    spec: Optional[dict]

    project_plan: Optional[dict]

    folder_structure: Optional[dict]

    generated_files: dict

    styling_applied: bool

    dependencies: List[str]
    install_success: Optional[bool]

    review_report: Optional[str]
    review_passed: Optional[bool]
    retry_count: int

    human_intervention_count: int
    errors: List[str]