import boto3
import json
from dotenv import load_dotenv

load_dotenv()

client = boto3.client("bedrock", region_name="us-east-1")
response = client.list_foundation_models()

for model in response["modelSummaries"]:
    if "meta" in model["modelId"]:
        print(f"ID: {model['modelId']}, Name: {model['modelName']}")
