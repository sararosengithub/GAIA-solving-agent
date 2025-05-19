from langgraph import Workflow, Agent, RouterAgent, RetrieverAgent, GeneratorAgent

# Define the retriever agent
retriever = RetrieverAgent(
    name="retriever",
    description="Retrieves relevant documents from a knowledge base."
)

# Define the generator agent
generator = GeneratorAgent(
    name="generator",
    description="Generates answers based on retrieved documents."
)

# Define the router agent
router = RouterAgent(
    name="router",
    description="Routes the input to the appropriate agent based on the query intent.",
    routes={
        "retrieve": retriever,
        "generate": generator
    }
)

# Define the workflow
workflow = Workflow(
    agents=[router, retriever, generator],
    entrypoint=router
)

# Example usage
if __name__ == "__main__":
    query = "What is the capital of France?"
    result = workflow.run(query)
    print(result)