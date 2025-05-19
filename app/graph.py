from langgraph import StateGraph
from .schemes import AgentState
from langchain_core.tools import tool
from .services import get_routing_llm, get_chat_llm

model = get_chat_llm()
# Template for a React agent node
def react_agent_node(state: AgentState) -> AgentState:
    # Implement the logic for the React agent here
    # For now, just return the state unchanged as a template
    return state
workflow = StateGraph(AgentState)

# Dummy tool implementation
@tool
def dummy_tool(place_holder: str):
    print("this is a tool call")

# Template for a Task Breakdown node
def task_breakdown_node(state: AgentState) -> AgentState:
        # Implement the logic for the Task Breakdown node here
        # For now, just return the state unchanged as a template
        return state
    
# Template for a Retriever node
def retriever_node(state: AgentState) -> AgentState:
    # Implement the logic for the Retriever node here
    # For now, just return the state unchanged as a template
    return state

# Template for a Generator node
def generator_node(state: AgentState) -> AgentState:
    # Implement the logic for the Generator node here
    # For now, just return the state unchanged as a template
    return state

# Template for a Web Browser node
def web_browser_node(state: AgentState) -> AgentState:
    # Implement the logic for the Web Browser node here
    # For now, just return the state unchanged as a template
    return state

def route_based_on_intent(state: AgentState) -> str:
    if not state.tasks or len(state.tasks) == 0:
        return "error, no tasks found"
    first_task = state.tasks[0]
    router_llm = get_routing_llm()
    prompt = f"Given the following task: {first_task}, decide the agent to handle it. Respond with one of: chat, quiz, error."
    response = router_llm(prompt)
    intent = response.strip().lower()
    if intent in ["web_browser", "retriever", "generator", "END"]:
        return intent
    else:
        return "error"

tools = [dummy_tool]
model = model.bind_tools(tools)

workflow.add_node(task_breakdown_node,
                  name="task_breakdown_node",
                  description="Task Breakdown node")
workflow.add_node(react_agent_node,
                  name="react_agent_node",
                  description="React agent node")
workflow.add_node(retriever_node,
                  name="retriever_node",
                  description="Retriever node")
workflow.add_node(generator_node,
                  name="generator_node",
                  description="Generator node")
workflow.add_node(web_browser_node,
                  name="web_browser_node",
                  description="Web Browser node")


# Add edges between nodes
workflow.set_entry_point("task_breakdown_node")
workflow.add_edge("task_breakdown_node", "react_agent_node")

workflow.add_conditional_edges(
    "react_agent_node", 
    route_based_on_intent, # Path mapping function
    {
        web_browser_node: "web_browser",
        retriever_node: "retriever",
        generator_node: "generator",
        "end": "END",
    }
)

workflow.add_edge(retriever_node,react_agent_node )
workflow.add_edge(generator_node,react_agent_node )
workflow.add_edge(web_browser_node,react_agent_node )

