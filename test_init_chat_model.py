from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv()

print("Testing init_chat_model with AWS Bedrock...")

try:
    # Attempt to initialize AWS Bedrock model via init_chat_model
    # Note: explicit model_provider might be needed if it can't infer from name
    model = init_chat_model(
        model="amazon.nova-lite-v1:0", model_provider="aws_bedrock", temperature=0
    )

    response = model.invoke("Hello, who are you?")
    print(f"Response: {response.content}")
    print("✅ init_chat_model verification successful")

except Exception as e:
    print(f"❌ Verification failed: {e}")
