import boto3

bedrock = boto3.client("bedrock", region_name="us-east-1")
print("Listing Llama models:")
try:
    response = bedrock.list_foundation_models(byProvider="meta")
    for model in response.get("modelSummaries", []):
        print(f"- {model['modelId']}")
except Exception as e:
    print(f"Error listing methods: {e}")

print("\nListing Amazon models:")
try:
    response = bedrock.list_foundation_models(byProvider="amazon")
    for model in response.get("modelSummaries", []):
        print(f"- {model['modelId']}")
except Exception as e:
    print(f"Error listing methods: {e}")
