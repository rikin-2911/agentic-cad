# making the agent for the tool handling    
# Create the State and Graph for the agent reasoning.. --> In async manner because 

# ==================
# step - 1 Imports
# ==================
import os
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from typing import TypedDict, Annotated

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition  # ToolNode is already -> Asynchronous
from langchain_core.tools import tool

from langchain_groq import ChatGroq

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient 
from langchain_mcp_adapters.tools import load_mcp_tools

from prompt import prompt

# ==================
# step - 2 LLM Initialisation
# ==================
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
hf_api_key = os.getenv("HUGGINGFACE_HUB_ACCESS_TOKEN")

"""
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5,
    max_tokens=1800,
    api_key=groq_api_key,
)
"""

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.8-27B",
    task="text-generation",
    huggingfacehub_api_token=hf_api_key,
    max_new_tokens=500
)

llm = ChatHuggingFace(llm=llm)

# ==================
# MCP Client
# ==================
# Can connect with multiple MCP Client with both locally and remotely severs...

mcp_client = MultiServerMCPClient(
    {
        "cad_client": {
            "transport":"stdio",  # transport --> 1. For local server -> stdio | 2. For remote server -> HTTP/SSE
            "command": "/home/rikin/agentic-cad/mcp-server/.venv/bin/python",  # Command for executing the tool in the mcp_server from this file 
            "args": ["/home/rikin/agentic-cad/mcp-server/main.py"] # parh of the mcp-server -> main.py file where tools are created.
        }
        
    }
)

# Fir fetching the tools name -> build_graph()

# ==================
# step - 4 LangGraph Workflow In [ASYNC manner]
# ==================

# STATE
class CadAgentState(TypedDict):

    messages: Annotated[list, add_messages]

"""

# NODES
#"For Async execution - Make all the nodes async"

# 1. Agent Node
async def agent_node(state: CadAgentState):

    response = await llm.ainvoke(state["messages"])

    return {
        "messages": [response]
    }

# 2. Tool Node -> 
tool_node = ToolNode(tools)  # Already Async i.e., ToolNode Class

"""
# ASYNC GRAPH -> using function
async def build_graph(tools):

    # binding the mcp tools with llm
    llm_with_tools = llm.bind_tools(tools)

    # agent node for llm responses
    async def agent_node(state: CadAgentState):
        response = await llm_with_tools.ainvoke(
            state["messages"]
        )

        return {
            "messages": [response]
        }

    # tool node 
    tool_node = ToolNode(tools)

    # graph building
    graph = StateGraph(CadAgentState)
    
    graph.add_node("agent_node", agent_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent_node")

    graph.add_conditional_edges(
        "agent_node",
        tools_condition
    )

    graph.add_edge("tools", "agent_node")

    return graph.compile()
    """
    # Getting the tools from the MCP Client
    tools = await mcp_client.get_tools()  # fetch all the tools from the server
    print(tools)

    # Binding tools with LLM
    llm_with_tools = llm.bind_tools(tools)

    # Nodes
    # 1. Agent Node
    async def agent_node(state: CadAgentState):

        response = await llm_with_tools.ainvoke(state["messages"])

        return {
            "messages": [response]
        }

    # 2. Tool Node
    tool_node = ToolNode(tools)  # Already Async i.e., ToolNode Class

    # Creating the Graph and nodes with edges or connections
    graph = StateGraph(CadAgentState)

    graph.add_node("agent_node", agent_node)
    graph.add_node("tools", tool_node)


    # Defining graph connections
    graph.add_edge(START, "agent_node")
    graph.add_conditional_edges("agent_node", tools_condition)
    graph.add_edge("tools", "agent_node")

    cad_agent = graph.compile()

    return cad_agent
    """


# ASYNC MAIN function for building the graph
async def main():
    async with mcp_client.session("cad_client") as session:

        tools = await load_mcp_tools(session)

        print("MCP tools loaded: ")

        for tool in tools:
            print("-", tool.name)

        cad_agent = await build_graph(tools)

        result = await cad_agent.ainvoke({"messages": [HumanMessage(content="You are expert Sr. CAD Design Engineer with 15+ years of experience in designing, draw the figures given in the task with the correct dimensions and take care of the geometry. " \
        "Task:Make a cube of 100mm of length, width, and height. Export it to STEP file/model")]})

        for message in result["messages"]:
            print("\n =============== ")
            print(type(message).__name__)
            print(message.content)
    """
    cad_agent = await build_graph()

    result = await cad_agent.ainvoke({"messages": [HumanMessage(content="Create a box of length 3mm, width 4mm and height 5 mm then export the model in the STEP file.")]})

    print(result['messages'][-1].content)


    # Print the model messages and tool's execution if any..
    for message in result["messages"]:
        print("\n====================")
        print(type(message).__name__)
        print(message)
    """
if __name__ == '__main__':
    asyncio.run(main())