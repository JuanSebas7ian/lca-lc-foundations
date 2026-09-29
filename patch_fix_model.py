import json

NOTEBOOK_PATH = r"f:\Cursos_code\lca-lc-foundations\notebooks\module-1\1.4_multimodal_messages.ipynb"


def update_model():
    with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb["cells"]

    found = False
    for cell in cells:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if "meta.llama4-maverick-17b-instruct-v1:0" in source:
                new_source = source.replace(
                    "meta.llama4-maverick-17b-instruct-v1:0",
                    "meta.llama3-8b-instruct-v1:0",
                )
                # rebuild list
                cell["source"] = [
                    line + ("\n" if not line.endswith("\n") else "")
                    for line in new_source.split("\n")
                ]
                # remove trailing empty
                if cell["source"][-1] == "":
                    cell["source"].pop()
                found = True
                print("Downgraded Llama 4 to Llama 3 (8b).")

    if found:
        with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print("Notebook saved.")
    else:
        print("Model ID not found to replace.")


if __name__ == "__main__":
    update_model()
