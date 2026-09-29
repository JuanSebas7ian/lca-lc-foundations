import os
import json

REPLACEMENTS = {
    "ChatGoogleGenerativeAI": "init_chat_model",
    "ChatOpenAI": "init_chat_model",
    "ChatAnthropic": "init_chat_model",
    "langchain_google_genai": "langchain.chat_models",
    "langchain_openai": "langchain.chat_models",
    "langchain_anthropic": "langchain.chat_models",
}

IMPORT_REPLACEMENTS = {
    "from langchain_google_genai import ChatGoogleGenerativeAI": "from langchain.chat_models import init_chat_model",
    "from langchain_openai import ChatOpenAI": "from langchain.chat_models import init_chat_model",
    "from langchain_anthropic import ChatAnthropic": "from langchain.chat_models import init_chat_model",
}


def fix_content(content):
    # 1. Fix Imports whole lines
    for old_imp, new_imp in IMPORT_REPLACEMENTS.items():
        content = content.replace(old_imp, new_imp)

    # 2. Fix class usages
    # Be careful not to replace text inside strings if possible, but for these specific class names it's likely code.
    # However, replacing "langchain_google_genai" in a string might be bad?
    # Let's stick to replacing the class names when they are function calls pattern-ish?
    # Or just global replace? "ChatGoogleGenerativeAI" is unique enough.

    content = content.replace("ChatGoogleGenerativeAI", "init_chat_model")
    content = content.replace("ChatOpenAI", "init_chat_model")
    content = content.replace("ChatAnthropic", "init_chat_model")

    return content


def process_file(filepath):
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
                        new_line = fix_content(line)
                        if new_line != line:
                            cell_modified = True
                        new_source_list.append(new_line)

                    if cell_modified:
                        cell["source"] = new_source_list
                        modified = True

            if modified:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=1)
                print(f"  Fixed {filepath}")

        else:
            new_content = fix_content(content)
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  Fixed {filepath}")

    except Exception as e:
        print(f"  Error processing {filepath}: {e}")


def main():
    root_dir = "notebooks"
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".ipynb") or filename.endswith(".py"):
                process_file(os.path.join(dirpath, filename))


if __name__ == "__main__":
    main()
