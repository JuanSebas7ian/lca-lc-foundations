from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os
import sys

load_dotenv()

with open("test_result_v3.txt", "w", encoding="utf-8") as f:
    f.write("Testing init_chat_model with model_provider='bedrock'...\n")
    try:
        model = init_chat_model(
            model="amazon.nova-lite-v1:0", model_provider="bedrock", temperature=0
        )
        f.write("Model initialized. Invoking...\n")
        response = model.invoke("Hello")
        f.write(f"Response: {response.content}\n")
        f.write("✅ Success with bedrock\n")
    except Exception as e:
        import traceback

        f.write(f"❌ Verification failed (bedrock): {e}\n")
        # f.write(traceback.format_exc()) # Reduce verbosity if needed

    f.write("\nTesting init_chat_model with model_provider='bedrock_converse'...\n")
    try:
        model = init_chat_model(
            model="amazon.nova-lite-v1:0",
            model_provider="bedrock_converse",
            temperature=0,
        )
        f.write("Model initialized. Invoking...\n")
        response = model.invoke("Hello")
        f.write(f"Response: {response.content}\n")
        f.write("✅ Success with bedrock_converse\n")
    except Exception as e:
        import traceback

        f.write(f"❌ Verification failed (bedrock_converse): {e}\n")
