"""
Project Initializer

Responsibilities
----------------
1. Create a unique project directory.
2. Initialize a React or Next.js project.
3. Save the generated project path in AgentState.

No LLM calls are made here.
"""

from pathlib import Path
import subprocess
import uuid
from src.agents.state import AgentState


# Where all generated projects will be stored
OUTPUT_ROOT = Path("outputs")


def project_initializer_node(state: AgentState) -> AgentState:
    """
    Creates a new frontend project based on the framework selected
    by previous agents.

    Expected state:

    state["spec"]["framework"]
        React
        or
        Next.js
    """

    framework = state["spec"]["framework"]

    # Create outputs directory if needed
    OUTPUT_ROOT.mkdir(exist_ok=True)

    # Unique folder for every generation
    session_id = str(uuid.uuid4())[:8]

    project_name = f"project_{session_id}"

    project_path = OUTPUT_ROOT / project_name

    print(f"\nCreating project: {project_name}")

    try:

        # -------------------------
        # React + Vite
        # -------------------------
        if framework.lower() == "react":

            subprocess.run(
                [
                    "npm",
                    "create",
                    "vite@latest",
                    str(project_path),
                    "--",
                    "--template",
                    "react"
                ],
                check=True
            )

        # -------------------------
        # Next.js
        # -------------------------
        elif framework.lower() == "next.js":

            subprocess.run(
                [
                    "npx",
                    "create-next-app@latest",
                    str(project_path),
                    "--yes"
                ],
                check=True
            )

        else:

            raise ValueError(
                f"Unsupported framework: {framework}"
            )

        print("Project created successfully.")

        # Save information into state
        state["project_name"] = project_name
        state["project_path"] = str(project_path)

    except subprocess.CalledProcessError as e:

        state["errors"].append(
            f"Project initialization failed: {e}"
        )

    return state
```