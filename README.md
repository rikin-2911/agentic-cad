# Agentic CAD

> **From engineering intent to a structured, executable CAD workflow.**

Agentic CAD is an AI-assisted CAD automation system that converts a
natural-language engineering request into structured CAD operations and
produces a CAD model, including STEP export.

The project combines **LangGraph**, **LLM tool calling**, **Model
Context Protocol (MCP)**, **FastAPI**, **FastMCP**, **Pydantic**, and
**CAD automation** into one workflow.

------------------------------------------------------------------------

## 🚀 Current Architecture

``` text
                         ┌──────────────────────┐
                         │        USER          │
                         │  Natural-language    │
                         │  CAD requirement     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         │  Request / Response  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │          LangGraph            │
                    │   Agent Workflow / State      │
                    └──────────────┬────────────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
              ┌──────────────┐           ┌──────────────┐
              │     LLM      │           │  Structured  │
              │ Groq / Qwen  │           │    State     │
              └──────┬───────┘           │   Pydantic   │
                     │                   └──────────────┘
                     │ Tool Calls
                     ▼
              ┌──────────────┐
              │  MCP Client  │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ FastMCP      │
              │    Server    │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────────┐
              │    CAD Tools     │
              │ Geometry / Holes │
              │ Features / Save  │
              │ STEP Export      │
              └────────┬─────────┘
                       │
                       ▼
                 ┌────────────┐
                 │ STEP File  │
                 │ .step/.stp │
                 └────────────┘

             ┌──────────────────────┐
             │      Database        │
             │ Designs / State /    │
             │ Tool results / Logs  │
             └──────────▲───────────┘
                        │
                        └── workflow persistence
```

------------------------------------------------------------------------

## 🧠 How the System Works

The workflow is intentionally separated into four layers:

``` text
┌────────────────────────────────────────────────────┐
│  1. APPLICATION                                    │
│     FastAPI                                        │
├────────────────────────────────────────────────────┤
│  2. REASONING & ORCHESTRATION                      │
│     LLM + LangGraph + Pydantic                     │
├────────────────────────────────────────────────────┤
│  3. TOOL COMMUNICATION                             │
│     MCP Client + FastMCP Server                    │
├────────────────────────────────────────────────────┤
│  4. ENGINEERING EXECUTION                          │
│     CAD tools + STEP export + Database             │
└────────────────────────────────────────────────────┘
```

The LLM decides **what should happen**.\
LangGraph controls **when it should happen**.\
MCP provides the controlled **tool interface**.\
The CAD tool performs the **actual geometry operation**.

------------------------------------------------------------------------

# 🔄 End-to-End Workflow

``` text
User Request
     │
     ▼
FastAPI
     │
     ▼
LangGraph State
     │
     ▼
System Prompt + Guardrails
     │
     ▼
LLM
(Groq / Qwen)
     │
     ▼
Structured Output
(Pydantic)
     │
     ▼
Tool Selection
     │
     ▼
MCP Client
     │
     ▼
FastMCP Server
     │
     ▼
CAD Tool
     │
     ├── Create geometry
     ├── Modify geometry
     ├── Validate parameters
     └── Export STEP
     │
     ▼
Tool Result
     │
     ▼
LangGraph State Update
     │
     ├───────────────► Database
     │
     ▼
Final Response
```

------------------------------------------------------------------------

# 🤖 LLM Layer

The project supports an interchangeable LLM layer.

### Groq

The current cloud-based workflow uses:

``` text
Groq
  │
  └── openai/gpt-oss-120b
```

Groq provides the inference API while the rest of the application
communicates with the model through the application's LLM interface.

### Qwen 

The project can also use an open-source Qwen model.

For local experimentation:

``` text
Hugging Face
     │
     ▼
Qwen/Qwen3-0.6B
     │
     ▼
vLLM (In New Version)
     │
     ▼
OpenAI-compatible API
     │
     ▼
LangGraph
```

The LLM provider is therefore separated from the agent workflow:

``` text
                    ┌── Groq
                    │
LangGraph ── LLM ───┼── Qwen + vLLM(In New Version)
                    │
                    └── Other compatible models
```

This makes it possible to change the inference backend without
redesigning the CAD workflow.

> **Note:** Local vLLM inference is an optional deployment path. The
> primary workflow can continue using a hosted model.

------------------------------------------------------------------------

# 🕸️ LangGraph Agent Workflow

LangGraph is responsible for orchestrating the workflow and maintaining
shared state.

A simplified graph:

``` text
                         START
                           │
                           ▼
                  ┌─────────────────┐
                  │ Parse Request   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Validate Input  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │     LLM Agent   │
                  │ Plan CAD action │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Structured      │
                  │ Output/Pydantic │
                  └────────┬────────┘
                           │
                           ▼
                     Tool required?
                      /          \
                    No            Yes
                    │              │
                    ▼              ▼
                  END          MCP Client
                                   │
                                   ▼
                              MCP Server
                                   │
                                   ▼
                               CAD Tool
                                   │
                                   ▼
                              Tool Result
                                   │
                                   ▼
                              Update State
                                   │
                                   └──────► next step
```

LangGraph allows the workflow to become stateful and conditional instead
of being a single linear LLM call.

------------------------------------------------------------------------

# 🔌 MCP: Model Context Protocol

MCP is the interface between the AI workflow and external CAD
capabilities.

``` text
                LangGraph / LLM
                       │
                       │ tool call
                       ▼
                 ┌─────────────┐
                 │ MCP Client  │
                 └──────┬──────┘
                        │
                        │ MCP
                        ▼
                 ┌─────────────┐
                 │ FastMCP     │
                 │   Server    │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  CAD Tools  │
                 └──────┬──────┘
                        │
                        ▼
                    CAD Model
```

### Why MCP?

The LLM should not directly execute arbitrary CAD code.

Instead:

``` text
LLM
 │
 │ requested operation
 ▼
MCP
 │
 ├── validate arguments
 ├── expose allowed tools
 ├── execute controlled operation
 └── return structured result
 │
 ▼
CAD
```

This gives the system a clear boundary between **AI reasoning** and
**engineering execution**.

------------------------------------------------------------------------

# 🛠️ CAD Tool Layer

The MCP server exposes controlled CAD operations.

Examples:

``` text
Document
├── create_document
├── open_document
└── save_document

Geometry
├── create_box
├── create_cylinder
├── create_sketch
├── create_extrusion
├── create_hole
├── create_fillet
└── create_chamfer

Modification
├── modify_feature
├── modify_dimension
├── delete_feature
└── mirror_entity

Export
└── export_step
```

The tool list can grow as additional CAD operations are implemented.

------------------------------------------------------------------------

# 📐 STEP File Generation

One of the primary outputs of the current CAD workflow is a **STEP
file**.

``` text
Natural Language Requirement
             │
             ▼
        LLM Reasoning
             │
             ▼
       Tool Selection
             │
             ▼
        MCP Tool Call
             │
             ▼
        CAD Geometry
             │
             ▼
       Validate Model
             │
             ▼
       Export to STEP
             │
             ▼
       model.step
```

STEP provides a practical neutral CAD exchange format for transferring
the generated model to compatible CAD systems.

------------------------------------------------------------------------

# 🧾 Structured Output with Pydantic

The agent should not rely only on free-form text.

The workflow uses structured schemas to make agent output predictable.

Conceptually:

``` text
LLM
 │
 ▼
Raw model output
 │
 ▼
Pydantic validation
 │
 ├── Valid ──────► continue workflow
 │
 └── Invalid ────► retry / error handling
```

This provides a clear contract between the LLM and the rest of the
application.

------------------------------------------------------------------------

# 🛡️ Prompting and Guardrails

The system prompt defines the agent's role, available capabilities, and
operating constraints.

A simplified flow:

``` text
User Input
    │
    ▼
System Prompt
    │
    ├── Agent role
    ├── CAD rules
    ├── Tool usage rules
    ├── Output format
    └── Safety constraints
    │
    ▼
LLM
    │
    ▼
Guardrails
    │
    ├── Parameter validation
    ├── Allowed operations
    ├── Dimension limits
    ├── Invalid tool detection
    └── Output schema validation
    │
    ▼
MCP Tool
```

Guardrails are important because an LLM-generated tool call should never
be treated as automatically correct.

------------------------------------------------------------------------

# 🙋 Human-in-the-Loop (HITL)

For operations that require user approval, the workflow can pause before
execution.

``` text
              Agent proposes operation
                        │
                        ▼
                 ┌─────────────┐
                 │ HITL Review │
                 └──────┬──────┘
                        │
                ┌───────┴───────┐
                │               │
             APPROVE          REJECT
                │               │
                ▼               ▼
            MCP Tool       Modify / Retry
                │               │
                └───────┬───────┘
                        ▼
                  Continue Graph
```

This is particularly useful for destructive, ambiguous, or high-impact
CAD operations.

------------------------------------------------------------------------

# 🗄️ Database Integration

The database provides persistence beyond a single workflow execution.

The intended flow is:

``` text
FastAPI
   │
   ▼
LangGraph
   │
   ├──────────────► Database
   │                    │
   │                    ├── workflow state
   │                    ├── design history
   │                    ├── tool results
   │                    └── artifacts
   │
   ▼
MCP / CAD
```

This makes it possible to resume workflows, inspect design history, and
maintain multiple design versions.

------------------------------------------------------------------------

# 🌐 FastAPI Backend

FastAPI provides the HTTP interface for the application.


Communication:

``` text
Client / Frontend
       │
       │ HTTP
       ▼
    FastAPI
       │
       ▼
   LangGraph
       │
       ▼
  Agent + MCP
```

FastAPI keeps the API layer separate from the agent and CAD execution
layers.

------------------------------------------------------------------------

# 🧩 Complete Component Map

``` text
┌──────────────────────────────────────────────────────────────┐
│                         APPLICATION                          │
│                                                              │
│                         FastAPI                              │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATION                       │
│                                                              │
│                         LangGraph                            │
│                                                              │
│      State ──► Agent ──► Validation ──► Routing              │
└───────────────┬──────────────────────────────┬───────────────┘
                │                              │
                ▼                              ▼
       ┌─────────────────┐            ┌─────────────────┐
       │       LLM       │            │    Pydantic     │
       │ Groq / Qwen     │            │ Structured      │
       │ + vLLM optional │            │ Output          │
       └────────┬────────┘            └─────────────────┘
                │
                ▼
       ┌─────────────────┐
       │   MCP Client    │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ FastMCP Server  │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │    CAD Tools    │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │  CAD Model      │
       │  + STEP Export  │
       └─────────────────┘

                ┌─────────────────┐
                │    Database     │
                │ State / History │
                │ Results / Files │
                └─────────────────┘
```

------------------------------------------------------------------------

# 🔁 Example: Simple CAD Request

User:

``` text
Create a 100 × 60 × 10 mm plate
with four 8 mm diameter holes.
Export it as STEP.
```

Workflow:

``` text
User
 │
 ▼
FastAPI
 │
 ▼
LangGraph
 │
 ▼
LLM
 │
 │ structured plan
 ▼
Pydantic
 │
 ▼
MCP Client
 │
 ├── create_box(...)
 │
 ├── create_hole(...)
 │
 ├── create_hole(...)
 │
 ├── create_hole(...)
 │
 ├── create_hole(...)
 │
 └── export_step(...)
 │
 ▼
FastMCP Server
 │
 ▼
CAD Tool
 │
 ▼
plate.step
```

------------------------------------------------------------------------

# 🔐 Design Principles

### 1. Separate reasoning from execution

``` text
LLM → decides
LangGraph → orchestrates
MCP → controls tool access
CAD → executes
```

### 2. Validate model output

``` text
LLM
 ↓
Pydantic
 ↓
Guardrails
 ↓
MCP
 ↓
CAD
```

### 3. Keep workflow state explicit

Important state should be represented in structured objects rather than
hidden inside prompts.

### 4. Make operations traceable

A design should be able to answer:

``` text
What operation was requested?
Which tool executed it?
What parameters were used?
What was the result?
Which workflow step ran next?
```

### 5. Keep the LLM provider interchangeable

``` text
              ┌── Groq
              │
LangGraph ────┼── Qwen + vLLM
              │
              └── Future models
```

------------------------------------------------------------------------

# 🧪 Testing

The project should test individual components as well as the complete
workflow.

``` text
Unit Tests
   │
   ├── Pydantic schemas
   ├── Guardrails
   ├── CAD tools
   └── Database functions
   │
   ▼
Integration Tests
   │
   ├── Agent → MCP
   ├── MCP → CAD
   └── CAD → STEP
   │
   ▼
End-to-End Test
   │
   └── User → API → Agent → MCP → CAD → STEP
```

------------------------------------------------------------------------

# 🗺️ Current Development Direction

The project is being developed incrementally.

``` text
                    ┌──────────────────┐
                    │ Basic Agent      │
                    │ Workflow         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ MCP Client +     │
                    │ FastMCP Server   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ CAD Tool Calling │
                    │ + STEP Export    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Structured       Guardrails      Database
         Outputs
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    ┌──────────────────┐
                    │ HITL + Reliable  │
                    │ Agent Workflow   │
                    └──────────────────┘
```

------------------------------------------------------------------------

# 🔮 Future Scope

The architecture can later be extended with:

-   More CAD operations and feature types
-   Assembly generation
-   Design modification and mirroring
-   Simulation integration
-   Design optimization
-   Multiple CAD backends
-   Rich frontend visualization
-   Versioned CAD artifacts
-   Persistent workflow checkpoints
-   More advanced HITL approval flows
-   Local LLM inference through vLLM
-   Multi-agent engineering workflows

------------------------------------------------------------------------

# 📌 Project Goal

Agentic CAD aims to build a reliable bridge between **natural-language
engineering intent** and **executable CAD workflows**.

``` text
Engineering Intent
       │
       ▼
      LLM
       │
       ▼
   LangGraph
       │
       ▼
 Pydantic + Guardrails
       │
       ▼
   MCP Client
       │
       ▼
 FastMCP Server
       │
       ▼
   CAD Tools
       │
       ▼
  Validated Model
       │
       ▼
    STEP File
```

> **Agentic CAD --- From engineering intent to executable CAD.**
