
import json
import os

def fix_source_notebook():
    nb_path = "/home/juansebas7ian/lca-lc-foundations/notebooks/module-3/3.5_email_agent.ipynb"
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb_data = json.load(f)

    # 1. FIX: Rename dynamic_prompt to dynamic_prompt_func to avoid collision and match user snippet
    for cell in nb_data['cells']:
        if cell['cell_type'] == 'code':
            src = "".join(cell.get('source', []))
            if "@dynamic_prompt" in src and "def dynamic_prompt(" in src:
                # Rename the function definition
                new_src = src.replace("def dynamic_prompt(", "def dynamic_prompt_func(")
                # Also update the return/assignment if needed, but usually just the def is enough here 
                # as the decorator handles registration.
                cell['source'] = [line.replace("def dynamic_prompt(", "def dynamic_prompt_func(") for line in cell['source']]
                print("Fixed: Renamed 'dynamic_prompt' to 'dynamic_prompt_func' in definition.")
    
    # 2. INSERT/UPDATE: The exact create_agent code requested by user
    create_agent_source = [
        "# CREACIÓN DEL AGENTE:\n",
        "# Aquí se orquestan todos los componentes: \n",
        "# El LLM, las herramientas, el esquema de estado, el contexto y los middlewares.\n",
        "agent = create_agent(\n",
        "        llm,\n",
        "        tools=[authenticate, check_inbox, send_email],\n",
        "        state_schema=AuthenticatedState,\n",
        "        context_schema=EmailContext,\n",
        "        middleware=[\n",
        "            dynamic_tool_call,\n",
        "            dynamic_prompt_func,\n",
        "            HumanInTheLoopMiddleware(\n",
        "                interrupt_on={\n",
        "                    \"authenticate\": False,\n",
        "                    \"check_inbox\": False,\n",
        "                    \"send_email\": True, # Pausa para aprobación humana en esta herramienta\n",
        "                }\n",
        "            ),\n",
        "        ],\n",
        "    )"
    ]
    
    # Remove any existing create_agent cell to avoid duplicates before inserting
    nb_data['cells'] = [c for c in nb_data['cells'] if "agent = create_agent(" not in "".join(c.get('source', []))]
    
    # Find insertion point (after LLM config)
    cells = nb_data['cells']
    insert_index = -1
    for i, cell in enumerate(cells):
        src = "".join(cell.get('source', []))
        if "llm = ChatBedrock" in src:
            insert_index = i + 1
            break
            
    if insert_index != -1:
        new_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": create_agent_source
        }
        cells.insert(insert_index, new_cell)
        print(f"Fixed! Inserted EXACT create_agent cell at index {insert_index}")
    else:
        print("Could not find insertion point (llm definition)")

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb_data, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    fix_source_notebook()
