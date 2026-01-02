import nbformat
import re

path = 'notebooks/module-2/2.4_wedding_planners.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

modified = False

for cell in nb.cells:
    if cell.cell_type == 'code' and 'ChatBedrockConverse' in cell.source:
        # Replace the active Nova Lite config with Claude
        old_pattern = r'llm = ChatBedrockConverse\(\s*model="amazon\.nova-lite-v1:0".*?\)'
        new_llm = '''# Claude es más estable para tool use en agentes anidados
llm = ChatBedrockConverse(
    model="anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
    temperature=0.5,
    max_tokens=2048,
)'''
        
        if re.search(old_pattern, cell.source, re.DOTALL):
            cell.source = re.sub(old_pattern, new_llm, cell.source, flags=re.DOTALL)
            modified = True
            print("Switched to Claude Sonnet for stable tool use.")

if modified:
    with open(path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"\n✅ Updated {path}")
else:
    print("⚠️ Pattern not found. Checking current llm config...")
    for cell in nb.cells:
        if 'llm = ' in cell.source and ('ChatBedrock' in cell.source or 'nova' in cell.source.lower()):
            print(f"Found LLM cell:\n{cell.source[:500]}...")
