# 🤖 Agentic CAD

> **An AI-powered engineering assistant that converts natural-language mechanical and robotics requirements into CAD designs, validates them through simulation, and iteratively improves the design.**

---

## 📌 Overview

**Agentic CAD** is an AI-based mechanical and robotics design system designed to reduce the manual work involved in converting an engineering idea into a usable CAD model.

Instead of manually performing every step:

```text
Requirement
    ↓
Mechanical Design
    ↓
CAD Modeling
    ↓
Simulation
    ↓
Modification
    ↓
Final CAD
```

the system allows an engineer to describe the requirement in natural language:

> "Design a lightweight robotic arm capable of carrying a 2 kg payload with three rotational joints."

The system interprets the requirement, breaks it into engineering tasks, generates a design, evaluates it, identifies problems, and improves the design.

### Core idea

```text
                 ┌───────────────────────┐
                 │      User Request     │
                 │ Natural Language Spec │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │    AI Design Agent    │
                 │ Understands the goal  │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │   Planning / Routing  │
                 │     LangGraph         │
                 └───────────┬───────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     ┌────────────┐   ┌────────────┐   ┌────────────┐
     │ CAD Agent  │   │ Simulation │   │ CAM Agent  │
     │            │   │   Agent    │   │            │
     └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
           │                │                │
           └────────────────┼────────────────┘
                            ▼
                  ┌───────────────────────┐
                  │  Evaluation / Check   │
                  └───────────┬───────────┘
                              │
                     Pass? ───┴─── No
                      │             │
                     Yes            ▼
                      │      ┌─────────────┐
                      │      │ Optimization│
                      │      └──────┬──────┘
                      │             │
                      └──────┬──────┘
                             ▼
                  ┌───────────────────────┐
                  │ Final Design + Export │
                  └───────────────────────┘
```

---

# 🎯 Problem Statement

Mechanical and robotics design usually requires engineers to move between several independent tools.

For example:

1. Understand the requirements.
2. Calculate dimensions.
3. Create a CAD model.
4. Modify the model manually.
5. Run a simulation.
6. Inspect the results.
7. Change the design.
8. Repeat the simulation.
9. Prepare the final model.
10. Export the required manufacturing files.

This process is powerful but can be slow and repetitive.

The main problem is not that CAD software is incapable of doing these tasks.

The problem is that **the engineer has to manually coordinate all of them.**

Agentic CAD attempts to solve this coordination problem using AI agents.

---

# 💡 Proposed Solution

Agentic CAD introduces an AI layer above engineering tools.

The AI does not replace CAD or simulation software.

Instead, it acts as an **engineering coordinator**.

It decides:

* What does the user actually want?
* What design should be created?
* Which CAD operation should be performed?
* What needs to be simulated?
* Did the design satisfy the requirements?
* What should be changed if it failed?
* When should the process stop?
* Which final file should be exported?

The system therefore creates a closed-loop engineering workflow:

```text
Understand
    ↓
Plan
    ↓
Create
    ↓
Simulate
    ↓
Evaluate
    ↓
Improve
    ↓
Create Again
    ↓
Validate
    ↓
Export
```

---

# 🏷️ Project Name

## Agentic CAD

### Short Problem Name

**AI-Driven Automated Mechanical Design**

### One-line description

> **An agentic AI system that transforms engineering requirements into validated CAD designs through automated design, simulation, and optimization loops.**

---

# 🏗️ System Architecture

The project is divided into several major layers.

```text
┌──────────────────────────────────────────────────────────────┐
│                         USER LAYER                           │
│                                                              │
│  Natural Language Engineering Requirement                    │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                       AI AGENT LAYER                         │
│                                                              │
│  Requirement Agent                                           │
│  Design Agent                                                │
│  Simulation Agent                                            │
│  Optimization Agent                                          │
│  CAM Agent                                                   │
│  Visualization / Export Agent                                │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                        │
│                                                              │
│                         LangGraph                            │
│                                                              │
│  State → Planning → Agent Execution → Feedback → Routing     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                       MCP LAYER                              │
│                                                              │
│              Model Context Protocol Server                   │
│                                                              │
│  Tool discovery → Validation → Routing → Execution → Result  │
└───────────────┬──────────────────────┬───────────────────────┘
                │                      │
                ▼                      ▼
┌──────────────────────────┐  ┌──────────────────────────────┐
│       CAD TOOLS          │  │      SIMULATION TOOLS        │
│                          │  │                              │
│ FreeCAD / SolidWorks     │  │ PyBullet / ROS / FEA         │
│ Onshape                  │  │ Motion / Physics Simulation  │
└────────────┬─────────────┘  └──────────────┬───────────────┘
             │                               │
             └───────────────┬───────────────┘
                             ▼
                  ┌─────────────────────────┐
                  │      DESIGN OUTPUT      │
                  │                         │
                  │ STEP / STL / DXF /      │
                  │ SLDPRT / SLDASM /      │
                  │ G-code                  │
                  └─────────────────────────┘
```

---

# 🧩 Major Components

## 1. User Interface

The user interface is the entry point into the system.

The user does not need to know the exact CAD commands required.

Instead, they provide an engineering requirement.

### Example

```text
Create a mounting bracket for a robotic arm.

Requirements:
- Material: Aluminium
- Maximum load: 5 kg
- Keep weight below 500 g
- Four mounting holes
- Must withstand the expected load
```

The system converts this high-level request into structured engineering information.

### Responsibilities

* Accept user requirements
* Display generated designs
* Display simulation results
* Display agent progress
* Show validation results
* Allow users to review final designs
* Provide downloadable CAD files

---

# 🧠 2. Requirement Understanding Agent

The first agent converts human language into structured requirements.

### Input

```text
Design a lightweight robotic arm bracket
that supports a 5 kg load.
```

### Output

```json
{
  "object": "robotic_arm_bracket",
  "load": "5 kg",
  "priority": "lightweight",
  "application": "robotics",
  "required_validation": true
}
```

The important point is that the rest of the system should not have to repeatedly interpret the original user message.

The requirement agent creates a structured representation that other agents can use.

### Responsibilities

* Understand natural language
* Extract dimensions
* Identify constraints
* Identify materials
* Identify loads
* Identify manufacturing requirements
* Identify simulation requirements
* Detect missing information
* Convert the request into structured state

---

# 🧭 3. Planning Agent

The planning agent determines **what needs to happen next**.

For example:

```text
User Requirement
       ↓
Create initial geometry
       ↓
Apply material
       ↓
Apply constraints
       ↓
Run simulation
       ↓
Check stress
       ↓
Check displacement
       ↓
Optimize
       ↓
Export
```

The planner is important because the system is not simply executing a fixed sequence.

Different engineering problems require different workflows.

### Example

For a simple bracket:

```text
Requirement
 → CAD
 → Simulation
 → Validation
 → Export
```

For a robotic component:

```text
Requirement
 → CAD
 → Assembly
 → Motion Simulation
 → Structural Simulation
 → Optimization
 → Export
```

---

# 🧠 4. Design Generation Agent

The Design Agent is responsible for converting engineering requirements into actual CAD operations.

It does not directly "draw" the model like a human.

Instead, it determines which operations are required.

For example:

```text
Create sketch
      ↓
Create rectangle
      ↓
Add dimensions
      ↓
Extrude
      ↓
Create holes
      ↓
Apply fillet
      ↓
Create final body
```

These operations are then sent to the CAD tool through MCP.

### Responsibilities

* Select geometry
* Determine dimensions
* Create sketches
* Create features
* Create assemblies
* Modify existing geometry
* Apply constraints
* Create manufacturing-friendly geometry
* Save intermediate designs

---

# 🔌 5. MCP Server

The **Model Context Protocol (MCP)** layer is one of the most important parts of the system.

MCP provides a standardized way for the AI agents to communicate with external engineering software.

Instead of allowing the LLM to directly execute arbitrary CAD commands, the system exposes controlled tools.

### Concept

```text
AI Agent
   │
   │ "Create a 50 mm extrusion"
   ▼
MCP Tool
   │
   │ Validate request
   ▼
CAD Software
   │
   │ Execute operation
   ▼
MCP Response
   │
   ▼
AI Agent
```

### Why MCP is useful

Without a tool layer:

```text
LLM ───────────────► CAD
```

The connection becomes difficult to control.

With MCP:

```text
LLM
 │
 ▼
MCP
 │
 ├── Validate
 ├── Check parameters
 ├── Apply limits
 ├── Select correct tool
 └── Execute
      │
      ▼
     CAD
```

MCP therefore acts as a **controlled bridge** between AI and engineering software.

---

# 🛠️ MCP Tool Categories

The MCP server can expose tools such as:

## CAD Lifecycle

```text
create_document()
open_document()
save_document()
close_document()
```

## Geometry

```text
create_sketch()
create_box()
create_cylinder()
create_extrusion()
create_revolution()
create_fillet()
create_chamfer()
```

## Assembly

```text
create_component()
add_constraint()
create_joint()
assemble_components()
```

## Modification

```text
modify_dimension()
modify_feature()
delete_feature()
update_sketch()
```

## Simulation

```text
create_simulation()
apply_material()
apply_load()
apply_constraint()
run_simulation()
get_simulation_result()
```

## Export

```text
export_step()
export_stl()
export_dxf()
export_sldprt()
export_sldasm()
```

The exact tool list can grow as the project grows.

---

# 🕸️ 6. LangGraph Orchestration

LangGraph is responsible for coordinating the agents.

Instead of creating one large AI function, the project represents the workflow as a graph.

```text
                    ┌──────────────┐
                    │   START      │
                    └──────┬───────┘
                           ▼
                 ┌──────────────────┐
                 │ Understand Input │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │      Plan        │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │ Generate Design  │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │     Simulate     │
                 └────────┬─────────┘
                          ▼
                 ┌──────────────────┐
                 │    Evaluate      │
                 └────────┬─────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
              PASS                FAIL
                │                   │
                ▼                   ▼
             Export             Optimize
                                    │
                                    ▼
                              Generate Again
                                    │
                                    └──────► Simulate
```

### Why LangGraph?

The system needs:

* State management
* Multiple agents
* Conditional routing
* Iteration
* Error handling
* Feedback loops

LangGraph provides a clean way to represent this behavior.

---

# 📦 7. Shared Agent State

All agents should work with a common state.

A simplified state can look like:

```python
state = {
    "user_request": "...",
    "requirements": {},
    "design_parameters": {},
    "cad_model": None,
    "simulation_results": {},
    "validation": {},
    "optimization_history": [],
    "errors": [],
    "final_output": None
}
```

This allows one agent to provide information to another.

### Example

The Design Agent writes:

```text
width = 50 mm
height = 80 mm
thickness = 8 mm
```

The Simulation Agent reads those values.

After simulation:

```text
maximum_stress = 85 MPa
maximum_displacement = 0.42 mm
```

The Optimization Agent reads these results and decides whether the design needs modification.

---

# 🔬 8. Simulation Agent

Creating a CAD model is not enough.

The system must determine whether the design actually satisfies the engineering requirements.

The Simulation Agent is responsible for this.

Depending on the problem, it may use:

* Physics simulation
* Motion simulation
* Structural analysis
* Robotics simulation
* FEA
* Collision checking

### Example

```text
Design
  ↓
Apply material
  ↓
Apply load
  ↓
Apply constraints
  ↓
Run simulation
  ↓
Collect results
```

Example result:

```text
Maximum Stress       : 72 MPa
Maximum Displacement : 0.31 mm
Factor of Safety     : 2.4
Result               : PASS
```

---

# ⚙️ 9. Optimization Agent

If the design fails validation, the system should not simply stop.

The Optimization Agent analyzes the simulation results and determines what should change.

### Example

Initial design:

```text
Stress = 180 MPa
Allowed = 120 MPa

Result = FAIL
```

The agent may reason:

```text
Stress is too high.

Possible changes:
- Increase thickness
- Add fillet
- Add support
- Change material
- Modify geometry
```

It then requests a design modification.

```text
Simulation
    ↓
Failure
    ↓
Optimization Agent
    ↓
Change parameters
    ↓
CAD Agent
    ↓
New design
    ↓
Simulation
```

This creates the project's **closed-loop design system**.

---

# 🔁 Design Optimization Loop

```text
                ┌─────────────────┐
                │ Initial Design  │
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │    Simulate     │
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │ Evaluate Result │
                └────────┬────────┘
                         ▼
                  ┌─────────────┐
                  │ Requirements│
                  │   satisfied?│
                  └──────┬──────┘
                     YES │ NO
                         │
              ┌──────────┘
              ▼
          ┌─────────┐
          │ Export  │
          └─────────┘

                         NO
                         │
                         ▼
                ┌─────────────────┐
                │    Optimize     │
                └────────┬────────┘
                         ▼
                ┌─────────────────┐
                │ Modify CAD      │
                └────────┬────────┘
                         │
                         └──────────► Simulate
```

---

# 🏭 10. CAM Agent

After the design is validated, it can be prepared for manufacturing.

The CAM Agent converts the CAD design into manufacturing-related information.

Depending on the manufacturing method, this can include:

```text
CAD Model
    ↓
Manufacturing Analysis
    ↓
Tool Selection
    ↓
Toolpath Generation
    ↓
Machining Parameters
    ↓
G-code
```

### Responsibilities

* Check manufacturability
* Identify machining operations
* Select tools
* Generate toolpaths
* Prepare manufacturing files
* Generate G-code where supported

---

# 👁️ 11. Visualization Agent

The Visualization Agent makes the design easier to inspect.

It can provide:

* 3D model previews
* Assembly views
* Simulation result visualization
* Stress distribution
* Motion results
* Design comparison

Example:

```text
                 Design V1
                    │
                    ▼
              Simulation
                    │
                    ▼
              Visualization
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      Geometry            Simulation
       View                  View
```

This is particularly useful because engineers should be able to inspect what the AI created instead of relying only on text output.

---

# 💾 12. Export System

Once the design passes validation, the system exports the result.

Possible formats include:

| Format    | Purpose             |
| --------- | ------------------- |
| `.STEP`   | CAD exchange        |
| `.STL`    | 3D printing / mesh  |
| `.DXF`    | 2D drawings         |
| `.SLDPRT` | SolidWorks part     |
| `.SLDASM` | SolidWorks assembly |
| `.GCODE`  | CNC manufacturing   |

The exact formats depend on the CAD software being connected.

---

# 🧠 Role of the LLM

The LLM is **not the CAD engine**.

Its job is primarily to understand and reason about the engineering task.

```text
LLM
 │
 ├── Understand requirement
 ├── Plan workflow
 ├── Select tools
 ├── Interpret results
 ├── Decide next action
 └── Explain final result
```

The actual engineering operations are performed by external tools.

This separation is important.

### LLM

```text
"What should I do?"
```

### CAD Tool

```text
"Perform the actual geometry operation."
```

### Simulation Tool

```text
"Calculate the physical result."
```

### MCP

```text
"Safely connect the AI request to the correct tool."
```

---

# 🔐 Safety and Validation

The AI should not have unrestricted access to engineering software.

The MCP layer provides an additional control point.

For example:

```text
AI requests:

create_extrusion(
    length = -5000
)
```

The MCP layer can detect that the value is invalid.

```text
AI
 ↓
MCP
 ↓
Validate parameters
 ↓
INVALID
 ↓
Return error
```

This prevents bad model outputs from directly causing unexpected operations.

Validation can include:

* Parameter type checking
* Dimension limits
* Valid CAD operations
* File path validation
* Tool availability
* Simulation constraints
* Maximum iteration count

---

# 🧱 Component Responsibilities

| Component           | Main Responsibility                                   |
| ------------------- | ----------------------------------------------------- |
| User Interface      | Collect requirements and display results              |
| LLM                 | Understand and reason about engineering tasks         |
| Requirement Agent   | Convert natural language into structured requirements |
| Planning Agent      | Decide the required workflow                          |
| Design Agent        | Generate and modify CAD models                        |
| Simulation Agent    | Test the design                                       |
| Optimization Agent  | Improve failed designs                                |
| CAM Agent           | Prepare manufacturing operations                      |
| Visualization Agent | Show geometry and simulation results                  |
| LangGraph           | Coordinate the agents                                 |
| Shared State        | Store information between agents                      |
| MCP Server          | Safely connect agents with external tools             |
| CAD Software        | Perform actual CAD operations                         |
| Simulation Engine   | Perform physical/robotics calculations                |
| Database / Memory   | Store useful design information and history           |
| Export System       | Produce final engineering files                       |

---

# 🔄 Complete End-to-End Workflow

The complete system can be understood as nine stages.

## Stage 1 — User Requirement

```text
"Design a lightweight robotic arm joint
that can support a 2 kg payload."
```

↓

## Stage 2 — Requirement Understanding

The system extracts:

```text
Object:
Robotic arm joint

Payload:
2 kg

Priority:
Lightweight

Application:
Robotics
```

↓

## Stage 3 — Planning

The planner creates:

```text
Requirement
     ↓
CAD Generation
     ↓
Assembly
     ↓
Simulation
     ↓
Validation
     ↓
Optimization if required
     ↓
Export
```

↓

## Stage 4 — CAD Generation

The Design Agent creates:

```text
Sketch
 ↓
Geometry
 ↓
Features
 ↓
Assembly
```

↓

## Stage 5 — Simulation

The Simulation Agent evaluates:

```text
Stress
Displacement
Motion
Collision
Other relevant metrics
```

↓

## Stage 6 — Evaluation

The system compares results with the requirements.

```text
Required:
Factor of Safety >= 2

Actual:
Factor of Safety = 1.4

Result:
FAIL
```

↓

## Stage 7 — Optimization

The Optimization Agent proposes changes.

```text
Increase support thickness
        +
Increase fillet radius
        +
Reduce unnecessary material
```

↓

## Stage 8 — Re-simulation

The modified model is simulated again.

```text
New Factor of Safety = 2.6

Result = PASS
```

↓

## Stage 9 — Export

```text
Validated CAD
     ↓
STEP
STL
DXF
SolidWorks files
G-code
```

---

# 📊 Agent Interaction Diagram

```text
                       USER
                        │
                        ▼
              ┌──────────────────┐
              │ Requirement Agent│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  Planning Agent  │
              └────────┬─────────┘
                       │
                       ▼
                ┌──────────────┐
                │   LangGraph  │
                │ Orchestrator │
                └──────┬───────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      ┌────────┐  ┌──────────┐  ┌────────┐
      │  CAD   │  │Simulation│  │  CAM   │
      │ Agent  │  │  Agent   │  │ Agent  │
      └───┬────┘  └────┬─────┘  └───┬────┘
          │            │            │
          └────────────┼────────────┘
                       ▼
                  ┌─────────┐
                  │   MCP   │
                  │ Server  │
                  └────┬────┘
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
       FreeCAD      Simulator      CAM Tool
          │            │             │
          └────────────┼─────────────┘
                       ▼
                  Tool Results
                       │
                       ▼
                 Evaluation Agent
                       │
                  ┌────┴────┐
                  │         │
                PASS       FAIL
                  │         │
                  ▼         ▼
               Export   Optimization
                            │
                            └──────► CAD
```

---

# 🧠 Why Multiple Agents?

A single large AI agent could theoretically perform everything.

However, that would make the system difficult to maintain.

Instead, each agent has a clear responsibility.

```text
Requirement Agent
       ↓
"What is the user asking?"

Planning Agent
       ↓
"What steps are required?"

CAD Agent
       ↓
"How should the geometry be created?"

Simulation Agent
       ↓
"Does the design work?"

Optimization Agent
       ↓
"How can it be improved?"

CAM Agent
       ↓
"How can it be manufactured?"

Visualization Agent
       ↓
"How should the result be presented?"
```

This makes the system easier to understand, test, and extend.

---

# 🧰 Technology Stack

## AI / Agent Layer

| Technology | Role                                           |
| ---------- | ---------------------------------------------- |
| Python     | Main programming language                      |
| LLM        | Reasoning and natural-language understanding   |
| LangChain  | LLM and tool integration                       |
| LangGraph  | Agent orchestration and workflow               |
| MCP        | Communication between AI and engineering tools |

---

## Backend

| Technology | Role                               |
| ---------- | ---------------------------------- |
| FastAPI    | Backend API                        |
| Python     | Application logic                  |
| Pydantic   | Structured input/output validation |

---

## CAD

The architecture is designed to work with CAD systems that expose programmable interfaces.

Potential integrations include:

* FreeCAD
* SolidWorks
* Onshape

The important architectural principle is:

```text
Agent
  ↓
MCP
  ↓
CAD Adapter
  ↓
CAD Software
```

This means the agent does not need to know the internal details of every CAD application.

---

# 🤖 Robotics / Simulation

For robotics-related workflows, the system can connect to:

* PyBullet
* ROS
* Gazebo
* Physics simulation tools
* FEA tools

A robotics workflow can therefore look like:

```text
Natural Language
      ↓
CAD Generation
      ↓
Robot Model
      ↓
Simulation
      ↓
Motion / Collision Testing
      ↓
Evaluation
      ↓
Design Modification
```

---

# 🔀 Error Handling

AI-generated operations can fail.

For example:

```text
Agent
 ↓
create_hole(diameter=1000mm)
 ↓
CAD
 ↓
ERROR
```

The system should not terminate immediately.

Instead:

```text
CAD Error
    ↓
MCP
    ↓
Structured Error
    ↓
Agent
    ↓
Understand Error
    ↓
Correct Parameters
    ↓
Retry
```

Example:

```json
{
  "success": false,
  "error": "Hole diameter exceeds body dimensions",
  "suggestion": "Use a smaller diameter"
}
```

This allows the agent to correct its action.

---

# 🔁 Retry and Iteration Limits

The system should not run forever.

A workflow can maintain:

```text
max_design_iterations = 5
max_tool_retries = 3
```

Example:

```text
Attempt 1 → FAIL
Attempt 2 → FAIL
Attempt 3 → PASS
```

If the system cannot produce a valid design within the allowed attempts:

```text
Optimization Failed

Reason:
Design constraints could not be satisfied.

Action:
Return the best generated design
and explain the remaining constraints.
```

---

# 🧠 Memory

The project can maintain useful information from previous designs.

For example:

```text
Design A
 ├── Material: Aluminium
 ├── Thickness: 5 mm
 ├── Stress: 150 MPa
 └── Result: FAIL

Design B
 ├── Material: Aluminium
 ├── Thickness: 8 mm
 ├── Stress: 95 MPa
 └── Result: PASS
```

The system can use this information to avoid repeating unsuccessful configurations.

Memory can store:

* Previous designs
* Simulation results
* Failed parameters
* Successful parameters
* User preferences
* Design templates

---

# 🔍 Observability

Because several agents and external tools are involved, logging is important.

A typical execution log might look like:

```text
[12:01:03] User request received

[12:01:04] Requirement Agent started

[12:01:06] Requirements extracted

[12:01:07] Planning workflow

[12:01:09] CAD Agent started

[12:01:14] CAD model generated

[12:01:15] Simulation started

[12:01:29] Simulation completed

[12:01:30] Maximum stress = 142 MPa

[12:01:30] Requirement check = FAIL

[12:01:31] Optimization started

[12:01:35] Geometry modified

[12:01:36] Simulation restarted

[12:01:49] Maximum stress = 91 MPa

[12:01:49] Requirement check = PASS

[12:01:50] STEP export completed
```

This makes debugging much easier.

---

# 🧪 Testing Strategy

Testing should happen at multiple levels.

## Unit Testing

Test individual components.

```text
Requirement Agent
CAD Tool
MCP Tool
Validation Function
Optimization Function
```

## Integration Testing

Test communication between components.

```text
Agent
 ↓
MCP
 ↓
CAD
 ↓
Result
```

## Workflow Testing

Test the complete graph.

```text
User
 ↓
Requirement
 ↓
Planning
 ↓
CAD
 ↓
Simulation
 ↓
Optimization
 ↓
Export
```

## Failure Testing

Test what happens when:

* CAD operation fails
* Simulation fails
* Invalid parameters are generated
* Tool becomes unavailable
* Requirements cannot be satisfied
* Optimization reaches its iteration limit

---

# 📈 Evaluation Metrics

The project should not only evaluate whether the AI produced a CAD file.

Useful metrics include:

### Design Success Rate

```text
Successful Designs
─────────────────── × 100
Total Requests
```

### Tool Success Rate

```text
Successful Tool Calls
───────────────────── × 100
Total Tool Calls
```

### Average Iterations

```text
Total Design Iterations
───────────────────────
Number of Designs
```

### Constraint Satisfaction

Measure how many requested requirements were satisfied.

Example:

```text
Requirements: 5

Satisfied:
✓ Weight
✓ Dimensions
✓ Material
✓ Load
✗ Manufacturing constraint

Score = 4 / 5
```

### Time to Valid Design

Measure:

```text
Request received
        ↓
Valid design generated
```

This is useful for comparing automated design against a manual workflow.

---

# 🛡️ Design Principles

The project follows several important principles.

## 1. AI should not directly control everything

The LLM should use controlled tools.

```text
LLM
 ↓
MCP
 ↓
Tool
```

---

## 2. Engineering software remains the source of truth

The AI can suggest a design.

The CAD and simulation systems determine whether the design is actually valid.

---

## 3. Every important decision should be traceable

The system should be able to answer:

```text
Why was this dimension selected?

Why was the design modified?

Why did the design fail?

Why was this material selected?

Why did the system stop?
```

---

## 4. Failure should generate feedback

A failed simulation is not simply an error.

It is information.

```text
Failure
   ↓
Understand
   ↓
Modify
   ↓
Test Again
```

---

# 🚀 Example Use Case

Consider the following request:

```text
Design a lightweight mounting bracket
for a robotic arm.

Requirements:
- Payload: 5 kg
- Aluminium
- Four mounting holes
- Low weight
- Must withstand the expected load
```

### Step 1 — Understand

```text
Object = mounting bracket
Material = aluminium
Payload = 5 kg
Mounting holes = 4
Optimization target = low weight
```

### Step 2 — Plan

```text
Create CAD
 ↓
Apply material
 ↓
Apply constraints
 ↓
Run structural simulation
 ↓
Check stress
 ↓
Optimize if necessary
 ↓
Export
```

### Step 3 — Generate

The CAD Agent creates the initial geometry.

### Step 4 — Simulate

The Simulation Agent evaluates the bracket.

```text
Stress = 165 MPa
Allowed = 120 MPa

FAIL
```

### Step 5 — Optimize

The Optimization Agent modifies the geometry.

```text
Increase support thickness
Add fillet
Remove unnecessary material
```

### Step 6 — Simulate Again

```text
Stress = 98 MPa

PASS
```

### Step 7 — Export

```text
bracket.step
bracket.stl
bracket.dxf
```

The complete process therefore becomes:

```text
User
 │
 ▼
Requirement Agent
 │
 ▼
Planner
 │
 ▼
CAD Agent
 │
 ▼
MCP
 │
 ▼
CAD Software
 │
 ▼
Simulation Agent
 │
 ▼
Evaluation
 │
 ├──────── PASS ───────► Export
 │
 └──────── FAIL
          │
          ▼
     Optimization
          │
          ▼
       CAD Agent
          │
          └────────► Simulation
```

---

# 🌐 API-Level Architecture

The backend can expose endpoints such as:

```text
POST /design
```

Starts a new design request.

```text
GET /design/{id}
```

Returns the current design status.

```text
GET /design/{id}/simulation
```

Returns simulation results.

```text
GET /design/{id}/history
```

Returns previous iterations.

```text
GET /design/{id}/export
```

Returns generated files.

---

# 🔌 Communication Flow

```text
Frontend
   │
   │ HTTP
   ▼
FastAPI
   │
   ▼
LangGraph
   │
   ├──────────────┐
   ▼              ▼
Agents          State
   │
   ▼
MCP Client
   │
   ▼
MCP Server
   │
   ├───────────┬────────────┐
   ▼           ▼            ▼
  CAD       Simulation      CAM
```

---

# 🐳 Deployment Architecture

The system can be containerized so individual services can be managed separately.

```text
┌──────────────────────────────────────────────┐
│                  Host System                 │
│                                              │
│  ┌────────────┐       ┌──────────────────┐  │
│  │ Frontend   │──────►│ FastAPI Backend  │  │
│  └────────────┘       └────────┬─────────┘  │
│                                │            │
│                                ▼            │
│                       ┌────────────────┐    │
│                       │   LangGraph    │    │
│                       └───────┬────────┘    │
│                               │             │
│                               ▼             │
│                       ┌────────────────┐    │
│                       │   MCP Server   │    │
│                       └───────┬────────┘    │
│                               │             │
│                ┌──────────────┼──────────┐  │
│                ▼              ▼          ▼  │
│             CAD Tool      Simulator     CAM │
│                                              │
└──────────────────────────────────────────────┘
```

---

# 🔮 Future Development

The architecture is designed so additional capabilities can be added without rebuilding the complete system.

Potential future additions include:

## Advanced CAD Generation

```text
Natural Language
       ↓
Parametric CAD
       ↓
Editable Feature Tree
```

## Multi-Objective Optimization

Optimize multiple objectives simultaneously:

```text
Minimize:
- Weight
- Cost

Maximize:
- Strength
- Performance

Subject to:
- Dimensions
- Material
- Manufacturing constraints
```

## Generative Design

Generate multiple design candidates:

```text
                 Requirement
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
      Design A    Design B    Design C
         │           │           │
         ▼           ▼           ▼
      Simulate    Simulate    Simulate
         │           │           │
         └───────────┼───────────┘
                     ▼
                 Compare
                     │
                     ▼
                Best Design
```

## Robotics Integration

Connect generated CAD models directly to robotics environments.

```text
CAD
 ↓
Robot Model
 ↓
ROS
 ↓
Gazebo / Simulation
 ↓
Motion Testing
 ↓
Feedback
 ↓
CAD Modification
```

This creates a complete design-to-simulation loop.

---

# 📚 Core Concept

The most important idea behind Agentic CAD is that **CAD generation is only one part of the problem**.

A useful engineering AI system should be able to perform:

```text
             ┌───────────────┐
             │  Understand   │
             └───────┬───────┘
                     ▼
             ┌───────────────┐
             │     Plan      │
             └───────┬───────┘
                     ▼
             ┌───────────────┐
             │     Design    │
             └───────┬───────┘
                     ▼
             ┌───────────────┐
             │    Simulate   │
             └───────┬───────┘
                     ▼
             ┌───────────────┐
             │    Evaluate   │
             └───────┬───────┘
                     ▼
                ┌─────────┐
                │  Valid? │
                └────┬────┘
                  Yes│  No
                     │   │
                     │   ▼
                     │ Optimize
                     │   │
                     │   └──────► Design
                     ▼
                  Export
```

The system therefore moves from:

> **"AI that generates CAD"**

towards:

> **"AI that can reason through an engineering design process."**

---

# 🏁 Final Architecture

```text
                           ┌──────────────────┐
                           │       USER       │
                           │ Engineering Spec │
                           └────────┬─────────┘
                                    │
                                    ▼
                     ┌──────────────────────────┐
                     │   REQUIREMENT AGENT      │
                     │ Extract constraints      │
                     └────────────┬─────────────┘
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │      PLANNING AGENT      │
                     │ Decide workflow          │
                     └────────────┬─────────────┘
                                  │
                                  ▼
              ┌─────────────────────────────────────────┐
              │               LANGGRAPH                 │
              │                                         │
              │         Shared State + Routing          │
              └────────────────────┬────────────────────┘
                                   │
              ┌────────────────────┼─────────────────────┐
              │                    │                     │
              ▼                    ▼                     ▼
      ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
      │  DESIGN      │     │ SIMULATION   │     │     CAM      │
      │    AGENT     │     │    AGENT     │     │    AGENT     │
      └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │       MCP SERVER         │
                     │                          │
                     │ Tool validation          │
                     │ Tool routing             │
                     │ Tool execution           │
                     │ Structured responses     │
                     └────────────┬─────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌────────────┐      ┌────────────┐      ┌────────────┐
       │    CAD     │      │ Simulation │      │    CAM     │
       │  Software  │      │   Engine   │      │   System   │
       └─────┬──────┘      └─────┬──────┘      └─────┬──────┘
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │     EVALUATION      │
                      │                     │
                      │ Requirements met?   │
                      └─────────┬───────────┘
                                │
                         ┌──────┴──────┐
                         │             │
                       PASS           FAIL
                         │             │
                         ▼             ▼
                     ┌───────┐   ┌──────────────┐
                     │Export │   │ OPTIMIZATION │
                     └───┬───┘   └──────┬───────┘
                         │              │
                         │              ▼
                         │        Modify Design
                         │              │
                         │              └──────► Simulation
                         │
                         ▼
              ┌──────────────────────────────┐
              │       FINAL OUTPUT           │
              │                              │
              │ STEP / STL / DXF / SLDPRT  │
              │ SLDASM / G-code             │
              └──────────────────────────────┘
```

---

# 🎓 What This Project Demonstrates

Agentic CAD combines several important areas of modern software and AI engineering:

* **Agentic AI** — AI that can decide and execute multiple steps.
* **LLM reasoning** — understanding engineering requirements.
* **Graph-based workflows** — controlling complex agent execution.
* **Tool calling** — allowing AI to interact with external software.
* **MCP** — standardized communication between agents and tools.
* **CAD automation** — programmatic mechanical design.
* **Simulation** — validating generated designs.
* **Optimization** — improving designs based on feedback.
* **Robotics** — connecting mechanical designs to robotic simulation.
* **Backend engineering** — exposing the system through APIs.
* **Observability** — tracking what the AI is doing.
* **Software architecture** — separating reasoning, orchestration, tools, and execution.

---

# ⭐ Project Vision

The long-term goal of Agentic CAD is not simply to generate a CAD model from a text prompt.

The goal is to create an **AI engineering assistant capable of understanding a mechanical or robotics problem, creating a candidate solution, testing it, learning from the results, and producing a validated engineering artifact.**

```text
Human Engineer
      │
      │ Requirements
      ▼
┌─────────────────────────────┐
│        AGENTIC CAD          │
│                             │
│ Understand                  │
│ Plan                        │
│ Design                      │
│ Simulate                    │
│ Evaluate                    │
│ Optimize                    │
│ Manufacture                 │
└──────────────┬──────────────┘
               │
               ▼
        Validated Design
               │
        ┌──────┴──────┐
        ▼             ▼
      CAD           CAM
     Output        Output
```

> **Agentic CAD — From engineering intent to validated design.**
