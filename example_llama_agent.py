import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState, END

# 1. Initialize the ChatBedrock model specifically for the Llama 4 model
# This is where we explicitly define the non-Amazon model usage.
llm = ChatBedrock(
    model_id="meta.llama4-maverick-17b-instruct-v1:0",
    model_kwargs={
        "temperature": 0.5,
        "max_gen_len": 2048,  # Llama specific parameter example
    },
    region_name="us-east-1",  # Ensure this matches where you have model access
)


# 2. Define the Agent Logic (Simple Graph)
def call_model(state: MessagesState):
    messages = state["messages"]
    # Ensure system prompt is handled if we want one
    # (Here we just let the model handle the messages directly)
    response = llm.invoke(messages)
    return {"messages": [response]}


# 3. Compile the Agent
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
agent = workflow.compile()

# 4. Use the Agent
print("Invoking Agent with Llama 4 Maverick...")
response = agent.invoke(
    {
        "messages": [
            HumanMessage(content="Explain the significance of the Moon in 3 sentences.")
        ]
    }
)

print("\nResponse:")
print(response["messages"][-1].content)
