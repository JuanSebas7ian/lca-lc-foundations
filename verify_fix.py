from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from dataclasses import dataclass

load_dotenv()

@dataclass
class ColourContext:
    favourite_colour: str = "blue"
    least_favourite_colour: str = "yellow"

@tool
def get_favourite_colour(runtime) -> str:
    """Get the favourite colour of the user"""
    return runtime.context.favourite_colour

llm = ChatBedrockConverse(
    model="us.meta.llama4-maverick-17b-instruct-v1:0",
    region_name="us-east-1",
    temperature=0.0,
)

agent = create_agent(
    model=llm,
    tools=[get_favourite_colour],
    context_schema=ColourContext
)

response = agent.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext()
)

print(f"Tool calls: {response['messages'][1].tool_calls}")
print(f"Final response: {response['messages'][-1].content}")
