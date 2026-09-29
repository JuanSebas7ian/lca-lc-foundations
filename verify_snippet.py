from langchain_aws import ChatBedrock
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, END
from IPython.display import display, Markdown


# Polyfill logic as applied to the notebook
def create_agent(model, tools=None, system_prompt=None):
    llm = ChatBedrock(model_id=model, model_kwargs={"temperature": 0.5})
    if tools:
        llm = llm.bind_tools(tools)

    def call_model(state: MessagesState):
        messages = list(state["messages"])
        if system_prompt and not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=system_prompt))
        response = llm.invoke(messages)
        return {"messages": [response]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", call_model)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()


# User's Snippet Logic
agent = create_agent(
    model="meta.llama4-maverick-17b-instruct-v1:0",
    system_prompt="You are a science fiction writer, create a capital city at the users request.",
)

question = HumanMessage(
    content=[{"type": "text", "text": "What is the capital of The Moon?"}]
)

print("Invoking agent...")
response = agent.invoke({"messages": [question]})

print("\nResponse Content:")
print(response["messages"][-1].content)
