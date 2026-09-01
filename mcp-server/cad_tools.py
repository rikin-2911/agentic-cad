import random
import uuid
from pathlib import Path
import asyncio

from fastmcp import FastMCP
import cadquery as cq

#OUTPUT_DIR = Path("generated")
OUTPUT_DIR = Path("/home/rikin/agentic-cad/mcp-server/generated")

# Prototype in-memory CAD model registry
MODELS: dict[str, cq.Workplane] = {}

# generating unique design_id for persistent memory of the design using UUID 
def _new_design_id() -> str:
    return str(uuid.uuid4())

# Model id generation 
def _get_model(design_id: str) -> cq.Workplane:
    if design_id not in MODELS:
        raise ValueError(F"Design '{design_id}' not found!")
    return MODELS[design_id]

# creating a FastMCP server instance
mcp = FastMCP("Cad Server")


## TOTAL THERE ARE 13 TOOLS INITIALLY.
# ==============================
# Geometry Functions
# ==============================
# Box
  
async def create_box(length: float, width: float, height: float) -> dict:

    """
    Create a 3D box using CadQuery and export it as a STEP file.

    Args:
        length: Length of the box in millimeters.
        width: Width of the box in millimeters.
        height: Height of the box in millimeters.

    Returns:
        Information about the generated CAD model.
    """


    # validating the input dimensions

    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Dimensions Can't be Negative")

    # create the geometry (box) using cadquery lib and save it in STEP file or STL file
    box = cq.Workplane("XY").box(length=length, width=width, height=height)

    # Assigning the unique design_id to the created object
    design_id = _new_design_id()
    MODELS[design_id] = box

    # Output file
    #output_path = OUTPUT_DIR / "box.step"

    # Export to STEP
    #q.exporters.export(box, str(output_path))

    return {
        "success": True,
        "design_id": design_id,
        "message": "Box created Successfully.",
        "dimensions_mm": {
            "length":length,
            "width":width,
            "height":height
        }
    }

# Cyclinder
 
async def create_cyclinder(radius: float, height: float) -> dict:

    """
    Create a 3D Cyclinder using CadQuery and export it as a STEP file.

    Args:
        radius: Radius of the Cyclinder.
        height: Height of the Cyclinder
        
    
    Returns:
        Information about the generated CAD model.

    """
    if radius <= 0 or height <= 0:
        raise ValueError("Dimensions Can't be Negative")


    # creating cyclinder using the cadquery 
    cyc = cq.Workplane("XY").cylinder(radius=radius, height=height)

    # assigning the model id to the object created
    design_id = _new_design_id()
    MODELS[design_id] = cyc

    return {
        "success": True,
        "design_id": design_id,
        "message": "Cyclinder Object Created Successfully.",
        "dimensions_mm": {
            "radius": radius,
            "height": height
        }
    }

# Sphere
  
async def create_sphere(radius: float) -> dict:

    """
    Create a 3D Sphere using CadQuery and export it as a STEP file.

    Args:
        radius: Radius of the Sphere.

    Return:
        Information about the generated CAD model.
    """

    if radius <= 0: 
        raise ValueError("Dimensions Can't be Negative")

    sphere = cq.Workplane("XY").sphere(radius=radius)

    # assigning the model id to the object created
    design_id = _new_design_id()
    MODELS[design_id] = sphere
    
    # assigning the model id to the object created
    design_id = _new_design_id()
    MODELS[design_id] = sphere
    
    return {
        "success": True,
        "design_id": design_id,
        "message": "Sphere Object Created Successfully.",
        "dimensions_mm": {
            "radius": radius,
        }
    }

# ==============================
# BOOLEAN OPERATIONS
# ==============================
  
async def boolean_union(
    design_id_1: str,
    design_id_2: str,
) -> dict:
    """Combine two CAD solids."""

    model_1 = _get_model(design_id_1)
    model_2 = _get_model(design_id_2)

    result = model_1.union(model_2)

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "union",
        "input_designs": [
            design_id_1,
            design_id_2,
        ],
    }


  
async def boolean_cut(
    design_id: str,
    tool_design_id: str,
) -> dict:
    """Subtract one CAD solid from another."""

    model = _get_model(design_id)
    tool = _get_model(tool_design_id)

    result = model.cut(tool)

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "cut",
        "base_design": design_id,
        "tool_design": tool_design_id,
    }

async def boolean_intersection(
    design_id_1: str,
    design_id_2: str,
) -> dict:
    """Keep only the common volume between two solids."""

    model_1 = _get_model(design_id_1)
    model_2 = _get_model(design_id_2)

    result = model_1.intersect(model_2)

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "intersection",
        "input_designs": [
            design_id_1,
            design_id_2,
        ],
    }


# ==========================================================
# MODIFICATION OPERATIONS
# ==========================================================
"""
async def create_hole(
    design_id: str,
    diameter: float,
    x: float,
    y: float,
    depth: float | None = None,
) -> dict:
    
    #Create a cylindrical hole from the top face.

    #x and y specify the hole position in mm.
    

    if diameter <= 0:
        raise ValueError("Diameter must be greater than 0.")

    model = _get_model(design_id)

    result = (
        model
        .faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(diameter, depth)
    )

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "hole",
        "diameter_mm": diameter,
        "position_mm": {
            "x": x,
            "y": y,
        },
        "depth_mm": depth,
    }
"""
async def create_hole(
    design_id: str,
    diameter: float,
    position: str = "custom",
    x: float | None = None,
    y: float | None = None,
    depth: float | None = None,
) -> dict:
    """
    Create a cylindrical hole from the top face.

    position:
        - "center": automatically place the hole at the center
          of the selected top face.
        - "custom": use the supplied x and y coordinates.

    x and y are measured in mm in the top-face workplane.
    """

    if diameter <= 0:
        raise ValueError("Diameter must be greater than 0.")

    if position not in {"center", "custom"}:
        raise ValueError("Position must be 'center' or 'custom'.")

    model = _get_model(design_id)

    # Select the top face
    top_face = model.faces(">Z")

    # Automatically calculate the center of the top face
    if position == "center":
        center = top_face.val().Center()
        x = center.x
        y = center.y

    elif position == "custom":
        if x is None or y is None:
            raise ValueError(
                "x and y are required when position='custom'."
            )

    result = (
        model
        .faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(diameter, depth)
    )
    

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "hole",
        "diameter_mm": diameter,
        "position": position,
        "position_mm": {
            "x": x,
            "y": y,
        },
        "depth_mm": depth,
    }

async def mirror_entity(
    design_id: str,
    plane: str,
) -> dict:
    """
    Mirror the current CAD entity across a specified plane.

    plane:
        - "XY" -> mirror across XY plane
        - "XZ" -> mirror across XZ plane
        - "YZ" -> mirror across YZ plane
    """

    if plane.upper() not in {"XY", "XZ", "YZ"}:
        raise ValueError(
            "Plane must be one of: XY, XZ, YZ."
        )

    model = _get_model(design_id)

    plane = plane.upper()

    # CadQuery mirror plane
    result = model.mirror(mirrorPlane=plane)

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "mirror",
        "mirror_plane": plane,
        "message": f"Design mirrored across the {plane} plane.",
    }

async def fillet(
    design_id: str,
    radius: float,
) -> dict:
    """Apply a fillet to all currently selected/default edges."""

    if radius <= 0:
        raise ValueError("Fillet radius must be greater than 0.")

    model = _get_model(design_id)

    result = (
        model
        .edges()
        .fillet(radius)
    )

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "fillet",
        "radius_mm": radius,
    }

  
async def chamfer(
    design_id: str,
    distance: float,
) -> dict:
    """Apply a chamfer to all edges."""

    if distance <= 0:
        raise ValueError("Chamfer distance must be greater than 0.")

    model = _get_model(design_id)

    result = (
        model
        .edges()
        .chamfer(distance)
    )

    new_id = _new_design_id()
    MODELS[new_id] = result

    return {
        "success": True,
        "design_id": new_id,
        "operation": "chamfer",
        "distance_mm": distance,
    }


# ==========================================================
# ANALYSIS
# ==========================================================
  
async def measure(design_id: str) -> dict:
    """Return basic geometric measurements."""

    model = _get_model(design_id)

    shape = model.val()
    bbox = shape.BoundingBox()

    return {
        "success": True,
        "design_id": design_id,
        "bounding_box_mm": {
            "length": bbox.xlen,
            "width": bbox.ylen,
            "height": bbox.zlen,
        },
        "volume_mm3": shape.Volume,
        "area_mm2": shape.Area,
    }

  
async def validate_geometry(design_id: str) -> dict:
    """Check whether the CAD geometry is valid."""

    model = _get_model(design_id)

    shape = model.val()

    try:
        valid = shape.isValid()
    except Exception as exc:
        return {
            "success": False,
            "design_id": design_id,
            "valid": False,
            "message": str(exc),
        }

    return {
        "success": True,
        "design_id": design_id,
        "valid": bool(valid),
        "message": (
            "Geometry is valid."
            if valid
            else "Geometry is invalid."
        ),
    }


# ==========================================================
# EXPORT
# ==========================================================
  
async def export_step(design_id: str) -> dict:
    """Export a CAD model as STEP."""

    model = _get_model(design_id)

    #filename = f"{design_id}.step"
    filename = str(design_id + ".step")
    output_path = OUTPUT_DIR / filename

    cq.exporters.export(
        model,
        str(output_path),
    )

    return {
        "success": True,
        "design_id": design_id,
        "format": "STEP",
        "file": str(output_path),
    }

  
async def export_stl(design_id: str) -> dict:
    """Export a CAD model as STL."""

    model = _get_model(design_id)

    filename = f"{design_id}.stl"
    output_path = OUTPUT_DIR / filename

    cq.exporters.export(
        model,
        str(output_path),
    )

    return {
        "success": True,
        "design_id": design_id,
        "format": "STL",
        "file": str(output_path),
    }
