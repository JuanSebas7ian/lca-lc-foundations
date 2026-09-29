import os
import json
import re

# The target configuration
NEW_MODEL_ID = "us.meta.llama4-maverick-17b-instruct-v1:0"
NEW_CONFIG_BLOCK = f"""llm = ChatBedrock(
    model_id="{NEW_MODEL_ID}",  # Nota el prefijo "us."
    region_name="us-east-1",
    model_kwargs={{
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 0.9,
    }}
)"""


def migrate_notebook(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        modified = False
        for cell in data["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])

                # Replace init_chat_model calls
                if "init_chat_model(" in source:
                    # Replace the whole assignment line if it matches model setup
                    new_source = re.sub(
                        r"(model\s*=\s*init_chat_model\s*\().*?(\))",
                        f'model = ChatBedrock(\n    model_id="{NEW_MODEL_ID}",\n    region_name="us-east-1",\n    model_kwargs={{"temperature": 0.7, "max_tokens": 2048, "top_p": 0.9}}\n)',
                        source,
                        flags=re.DOTALL,
                    )
                    # Also ensure import is there
                    if (
                        "ChatBedrock" not in new_source
                        and "from langchain_aws import ChatBedrock" not in source
                    ):
                        new_source = (
                            "from langchain_aws import ChatBedrock\n" + new_source
                        )

                    if new_source != source:
                        cell["source"] = [
                            l + ("\n" if not l.endswith("\n") else "")
                            for l in new_source.splitlines()
                        ]
                        modified = True

                # Replace direct model ID references in create_agent or strings
                elif "amazon.nova" in source:
                    new_source = source.replace("amazon.nova-lite-v1:0", NEW_MODEL_ID)
                    new_source = new_source.replace(
                        "amazon.nova-pro-v1:0", NEW_MODEL_ID
                    )
                    if new_source != source:
                        cell["source"] = [
                            l + ("\n" if not l.endswith("\n") else "")
                            for l in new_source.splitlines()
                        ]
                        modified = True

        if modified:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=1)
            print(f"  Updated {filepath}")
        else:
            print(f"  No changes made.")

    except Exception as e:
        print(f"  Error: {e}")


def main():
    root = "notebooks"
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".ipynb"):
                migrate_notebook(os.path.join(dirpath, filename))


if __name__ == "__main__":
    main()
