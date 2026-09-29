import os
import json
import re

# Models mapping
MODEL_MAPPING = {
    # Original -> New (AWS Nova)
    "gpt-5-nano": "amazon.nova-lite-v1:0",
    "gpt-4o": "amazon.nova-pro-v1:0",
    "gpt-3.5-turbo": "amazon.nova-lite-v1:0",
    "claude-sonnet-4-5": "amazon.nova-pro-v1:0",
    "gemini-3-pro-preview": "amazon.nova-pro-v1:0",
}

# Provider handling for init_chat_model
# Regex to find init_chat_model(..., model="OLD_MODEL", ...) and inject/update model_provider="bedrock"
# This is complex with regex. simpler approach:
# 1. Replace model names.
# 2. Add 'model_provider="bedrock"' to init_chat_model strings if not present?
# Or just rely on replacing model name, BUT init_chat_model might fail if it doesn't know the provider for nova.
# As seen in my test, "Unsupported model_provider='aws_bedrock'" and it needs "bedrock" or "bedrock_converse"
# AND it needs the provider explicitly if it can't infer it.
# LangChain might not infer amazon.nova* as bedrock yet?
# Let's assume we need to add `model_provider="bedrock"` usage.


def migrate_content(content):
    original_content = content

    # 1. Simple model name replacement
    for old_model, new_model in MODEL_MAPPING.items():
        # Use regex to be safe about boundaries where possible, or just string replace if unique enough
        # These IDs seem unique enough.
        content = content.replace(old_model, new_model)

    # 2. Update init_chat_model calls
    # Pattern: init_chat_model(...)
    # We want to ensure usage of AWS Nova models uses the provider.
    # If we just swapped the name, we now have init_chat_model(model="amazon.nova-lite-v1:0")
    # We should append provider.

    # Find patterns like: model="amazon.nova-lite-v1:0"
    # and replace with: model="amazon.nova-lite-v1:0", model_provider="bedrock"

    # Avoid double replacement if run multiple times?
    # Check if provider is already there?

    nova_models = ["amazon.nova-lite-v1:0", "amazon.nova-pro-v1:0"]

    for nova_model in nova_models:
        # Check for quoted usage
        pattern = f'"{nova_model}"'
        # We want to ensure it is followed by provider kwarg if inside init_chat_model?
        # Actually, simpler: replace occurrences of the model string with the model string + provider kwarg
        # BUT only if it looks like a function argument context?
        # "amazon.nova-lite-v1:0" -> "amazon.nova-lite-v1:0", model_provider="bedrock"
        # This might break if it's just a variable assignment: x = "amazon..."

        # Safe approach for init_chat_model:
        # init_chat_model(model="amazon.nova-lite-v1:0")
        # init_chat_model("amazon.nova-lite-v1:0")

        # Regex for init_chat_model with named arg
        # capture init_chat_model call
        pass

    # If simple text replacement, we risk syntax errors.
    # However, given the standardized course structure, let's try a regex for the specific call site found in 1.1

    # From: init_chat_model(model="gpt-5-nano")
    # To:   init_chat_model(model="amazon.nova-lite-v1:0", model_provider="bedrock")

    # We already replaced "gpt-5-nano" with "amazon.nova-lite-v1:0" in step 1.
    # So we look for: model="amazon.nova-lite-v1:0" and ensure it has provider.

    # Regex to add provider if missing
    for nova_model in nova_models:
        regex_model_arg = f'model="{nova_model}"'
        replacement = f'model="{nova_model}", model_provider="bedrock"'

        # Only replace if model_provider is NOT present nearby
        # This is tricky with regex.

        # Let's try to be specific for the known pattern in this codebase.
        # usually: model = init_chat_model(model="...")

        # If we see `init_chat_model(model="amazon.nova-lite-v1:0")` replace closing paren?
        # No, arguments might follow.

        # Let's try replacing `model="amazon.nova-lite-v1:0"` with `model="amazon.nova-lite-v1:0", model_provider="bedrock"`
        # This is generally safe in python kwargs if it's the first arg or middle arg.

        content = content.replace(
            f'model="{nova_model}"', f'model="{nova_model}", model_provider="bedrock"'
        )

        # Also handle positional arg: init_chat_model("amazon.nova-lite-v1:0")
        # Replace `"amazon.nova-lite-v1:0"` with `"amazon.nova-lite-v1:0", model_provider="bedrock"`
        # BUT we must be careful not to double replace the one above which now looks like:
        # model="amazon.nova-lite-v1:0", model_provider="bedrock"
        # The string "amazon..." is inside.

        # If we replaced `model="` version first, we are good for that case.
        # Now check for `init_chat_model("amazon.nova-lite-v1:0")`

        # We can search for `init_chat_model("{nova_model}")`
        content = content.replace(
            f'init_chat_model("{nova_model}")',
            f'init_chat_model("{nova_model}", model_provider="bedrock")',
        )
        content = content.replace(
            f"init_chat_model('{nova_model}')",
            f"init_chat_model('{nova_model}', model_provider='bedrock')",
        )

    return content


def process_file(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        is_notebook = filepath.endswith(".ipynb")

        if is_notebook:
            data = json.loads(content)
            modified = False

            for cell in data["cells"]:
                if cell["cell_type"] == "code":
                    source_list = cell["source"]
                    new_source_list = []
                    cell_modified = False
                    for line in source_list:
                        new_line = migrate_content(line)
                        if new_line != line:
                            cell_modified = True
                        new_source_list.append(new_line)

                    if cell_modified:
                        cell["source"] = new_source_list
                        modified = True

            if modified:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=1)
                print(f"  Updated {filepath}")
            else:
                print(f"  No changes needed for {filepath}")

        else:
            # Regular python file
            new_content = migrate_content(content)
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  Updated {filepath}")
            else:
                print(f"  No changes needed for {filepath}")

    except Exception as e:
        print(f"  Error processing {filepath}: {e}")


def main():
    root_dir = "notebooks"
    if not os.path.exists(root_dir):
        print(f"{root_dir} does not exist.")
        return

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".ipynb") or filename.endswith(".py"):
                process_file(os.path.join(dirpath, filename))


if __name__ == "__main__":
    main()
