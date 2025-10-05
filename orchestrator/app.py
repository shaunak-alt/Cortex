from fastapi import FastAPI
from pydantic import BaseModel

# Import graph builder
from .graph import build_graph

# Initialize the FastAPI app
app = FastAPI(
    title="YoLearn.ai Tutor Orchestrator",
    description="An intelligent middleware to orchestrate educational tools.",
    version="1.0.0"
)

# Build LangGraph app
langgraph_app = build_graph()

# Define the request model for API endpoint
class OrchestratorRequest(BaseModel):
    user_message: str

@app.get("/")
def read_root():
    """A simple endpoint to confirm the server is running."""
    return {"status": "Orchestrator is running and graph is compiled!"}


@app.post("/invoke")
def invoke_orchestrator(request: OrchestratorRequest):
    """
    The main endpoint to process a user's message and run the orchestration graph.
    """
    print(f"\n--- API INVOKED with message: '{request.user_message}' ---")
    
    # This is the input for graph's memory (the "state")
    inputs = {"user_message": request.user_message}
    
    # call the .invoke() method on our compiled graph to run the entire workflow
    final_state = langgraph_app.invoke(inputs)
    
    print(f"--- GRAPH EXECUTION COMPLETE ---")
    
    # The final state contains the list of all the JSON payloads created
    return {
        "input_message": request.user_message,
        "final_payloads": final_state.get("final_payloads", [])
    }