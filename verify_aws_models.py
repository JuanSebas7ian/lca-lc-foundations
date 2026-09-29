import os
import sys
from dotenv import load_dotenv

# Try to load .env file
if not load_dotenv():
    print("⚠️  Warning: .env file not found. Using environment variables if set.")

try:
    from langchain_aws import ChatBedrock
except ImportError:
    print("❌ langchain-aws not installed. Please run: pip install langchain-aws")
    sys.exit(1)


def verify_model(model_id):
    print(f"\nTesting model: {model_id}...")

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        print("❌ AWS credentials not found in environment variables.")
        print(
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in your .env file."
        )
        return False

    try:
        llm = ChatBedrock(model_id=model_id, region_name=aws_region)
        response = llm.invoke("Hello, are you working?")
        print(f"✅ Success! Response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ Error invoking model: {e}")
        return False


if __name__ == "__main__":
    print("Verifying AWS Bedrock Setup for Nova Models...")

    models_to_test = ["amazon.nova-pro-v1:0", "amazon.nova-lite-v1:0"]

    success_count = 0
    for model in models_to_test:
        if verify_model(model):
            success_count += 1

    if success_count == len(models_to_test):
        print("\n✨ All AWS Nova models verified successfully!")
    else:
        print(
            f"\n⚠️  {len(models_to_test) - success_count} model(s) failed verification."
        )
