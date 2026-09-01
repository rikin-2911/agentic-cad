from fastmcp import FastMCP

from cad_tools import (create_box, create_cyclinder, create_hole, mirror_entity, 
                       create_sphere, chamfer, boolean_cut, 
                       boolean_intersection, boolean_union, fillet,
                       measure, export_stl, export_step, validate_geometry)

# MCP Server Initialisation
mcp = FastMCP("Cad Server")


# Getting the tools 
mcp.tool(create_box)
mcp.tool(create_cyclinder)
mcp.tool(create_sphere)

mcp.tool(boolean_union)
mcp.tool(boolean_cut)
mcp.tool(boolean_intersection)

mcp.tool(create_hole)
mcp.tool(mirror_entity)
mcp.tool(fillet)
mcp.tool(chamfer)

mcp.tool(measure)
mcp.tool(validate_geometry)

mcp.tool(export_step)
mcp.tool(export_stl)

if __name__ == "__main__":
    mcp.run()