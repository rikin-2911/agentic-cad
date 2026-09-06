## Output parser for CAD state validation

from pydantic import BaseModel, Field # for validation
from typing import Literal # Literal is a type checker from the given list of mcp/tool functions 

class CadAction(BaseModel):

    # mcp tools actions or functions
    action: Literal[
        "create_box",
        "create_cyclinder", 
        "create_sphere", 
        "create_hole", 
        "mirror_entity", 
        "chamfer", 
        "boolean_cut",
        "boolean_intersection", 
        "boolean_union", 
        "fillet",
        "measure", 
        "export_stl", 
        "export_step",
        "validate_geometry"
    ]

    # design ig
    design_id: str | None = None

    # diameter 
    diameter = float | None = Field(default=None, ge=0)

    # coordinates
    x: float | None = None
    y: float | None = None

    depth_z = float | None = Field(default=None, gt=0)

    # LLM explanation
    explanation = str