from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os
import sys

load_dotenv()

with open("test_result.txt", "w", encoding="utf-8") as f:
    f.write("Testing init_chat_model with AWS Bedrock...\n")
    try:
        # Check env vars
        if not os.getenv("AWS_ACCESS_KEY_ID"):
            f.write("WARNING: AWS_ACCESS_KEY_ID not set\n")

        model = init_chat_model(
            model="amazon.nova-lite-v1:0", model_provider="aws_bedrock", temperature=0
        )

        f.write("Model initialized. Invoking...\n")
        response = model.invoke("Hello")
        f.write(f"Response: {response.content}\n")
        f.write("✅ Success\n")

    except Exception as e:
        import traceback

        f.write(f"❌ Verification failed: {e}\n")
        f.write(traceback.format_exc())
