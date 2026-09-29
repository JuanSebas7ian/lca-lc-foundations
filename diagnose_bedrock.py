import traceback
from langchain_aws import ChatBedrock

print("Testing model connection...")
try:
    # Explicitly testing the model ID configured
    llm = ChatBedrock(
        model_id="meta.llama4-maverick-17b-instruct-v1:0", region_name="us-east-1"
    )
    res = llm.invoke("hi")
    print("Success")
    print(res)
except Exception:
    traceback.print_exc()
