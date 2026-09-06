## Agent State file

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# pydantic model validation
from cad_opt_parser import CadAction

# STATE
class CadAgentState(TypedDict):

    # user input
    user_input: str

    # design id
    design_id: str

    # design context
    design_context: dict

    # action or result -> Output parser -> Pydantic Validated
    action: CadAction | None

    # validation error -> action
    validation_errors: list[str]

    requires_approval: bool

    approved: bool

    tool_result: dict | None

    # messages for conversation history
    messages: Annotated[list, add_messages]
