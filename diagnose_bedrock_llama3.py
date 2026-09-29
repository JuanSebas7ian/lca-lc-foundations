import traceback
from langchain_aws import ChatBedrock

print("Testing Llama 3.2 connection...")
try:
    # Testing Llama 3.2 11B (safer bet for availability)
    llm = ChatBedrock(
        model_id="meta.llama3-2-11b-instruct-v1:0", region_name="us-east-1"
    )
    res = llm.invoke("hi")
    print("Success with Llama 3.2 11B")
    print(res)
except Exception:
    print("Llama 3.2 11B failed.")
    traceback.print_exc()

    try:
        print("\nTesting Llama 3.1 8B...")
        llm = ChatBedrock(
            model_id="meta.llama3-1-8b-instruct-v1:0", region_name="us-east-1"
        )
        res = llm.invoke("hi")
        print("Success with Llama 3.1 8B")
    except Exception:
        print("Llama 3.1 8B failed too.")
        traceback.print_exc()
