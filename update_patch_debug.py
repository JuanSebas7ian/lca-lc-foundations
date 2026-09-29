import os

patch_path = r"f:\Cursos_code\lca-lc-foundations\.venv\Lib\site-packages\mcp\os\win32\utilities.py"

with open(patch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make the patch even more aggressive and add a debug print
target = "    except Exception:  # Optimized fix for Jupyter on Windows"
replacement = """    except Exception as e:
        print(f"DEBUG: MCP Patch triggered. Caught: {type(e).__name__}: {e}")
"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(patch_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated patch with debug print.")
else:
    print("Could not find previous patch to update.")
