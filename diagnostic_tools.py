from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain.messages import HumanMessage

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny."

llm = ChatBedrockConverse(
    model="us.meta.llama4-maverick-17b-instruct-v1:0",
    region_name="us-east-1",
    temperature=0.0,
)

llm_with_tools = llm.bind_tools([get_weather])

messages = [HumanMessage(content="What is the weather in London?")]
response = llm_with_tools.invoke(messages)

print(f"Response: {response.content}")
print(f"Tool calls: {response.tool_calls}")
