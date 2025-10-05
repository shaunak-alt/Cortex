from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Import our agent functions
from .agents import router_agent, parameter_extractor_agent

# --- 1. Define the State ---
# This is the "memory" of our graph. It's what gets passed between each step.

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        user_message: The initial message from the user.
        tool_queue: A list of tools the router has decided to call.
        final_payloads: A list to store the JSON outputs from the parameter extractors.
    """
    user_message: str
    tool_queue: List[str]
    final_payloads: List[Dict[str, Any]]


# --- 2. Define the Nodes ---
# The nodes are the "steps" in our workflow. Each node is a function that modifies the state.

def route_to_tools(state: GraphState) -> Dict[str, Any]:
    """
    The first step in our workflow. This node calls the router agent to decide which tool(s) to use.
    The result is added to the 'tool_queue' in our state.
    """
    print("--- NODE: route_to_tools ---")
    user_message = state["user_message"]
    chosen_tools = router_agent(user_message)
    return {"tool_queue": chosen_tools, "final_payloads": []} # Start with an empty list for payloads

def extract_tool_parameters(state: GraphState) -> Dict[str, Any]:
    """
    This node gets the next tool from the queue and calls the parameter extractor agent for it.
    The resulting JSON payload is added to our list of final payloads.
    """
    print("--- NODE: extract_tool_parameters ---")
    user_message = state["user_message"]
    tool_queue = state["tool_queue"]
    
    # Get the next tool to process
    tool_to_run = tool_queue[0]
    
    # Call the parameter extractor
    payload = parameter_extractor_agent(user_message, tool_to_run)
    
    # Add the new payload to list of results
    new_payloads = state.get("final_payloads", []) + [payload]
    
    # Remove the processed tool from the queue
    remaining_tools = tool_queue[1:]
    
    return {"tool_queue": remaining_tools, "final_payloads": new_payloads}


# --- 3. Define the Edges (Decision Logic) ---
# The edges decide which node to go to next.

def should_continue(state: GraphState) -> str:
    """
    This is our conditional edge. It checks if there are still tools left in the queue.
    If the queue is not empty, it loops back to the parameter extractor.
    If the queue is empty, it ends the workflow.
    """
    print("--- CONDITIONAL EDGE: should_continue ---")
    if state["tool_queue"]:
        print("Decision: Continue to parameter extraction.")
        return "continue"
    else:
        print("Decision: End workflow.")
        return "end"


# --- 4. Assemble the Graph ---

def build_graph():
    """
    Builds and returns the LangGraph workflow.
    """
    workflow = StateGraph(GraphState)

    # Add the nodes
    workflow.add_node("router", route_to_tools)
    workflow.add_node("extractor", extract_tool_parameters)

    # Define the workflow's entry point
    workflow.set_entry_point("router")

    # Add the conditional edge for loop
    workflow.add_conditional_edges(
        "extractor",
        should_continue,
        {
            "continue": "extractor", # If tools remain, loop back to the extractor
            "end": END              # If no tools remain, finish
        }
    )

    # Connect the router to the extractor
    workflow.add_edge("router", "extractor")

    # Compile the graph into a runnable app
    app = workflow.compile()
    print("--- Graph Compiled Successfully ---")
    return app