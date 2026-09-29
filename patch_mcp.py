import os

patch_path = r"f:\Cursos_code\lca-lc-foundations\.venv\Lib\site-packages\mcp\os\win32\utilities.py"

if not os.path.exists(patch_path):
    print(f"Error: Path {patch_path} not found.")
    exit(1)

with open(patch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Target line to find
target = "    except NotImplementedError:"
replacement = '    except (NotImplementedError, io.UnsupportedOperation, AttributeError) if "io" in globals() else (NotImplementedError, AttributeError):'

# Check if we need to add io to the catch, but first check if io is imported.
# Actually, the file likely imports io or we can just catch Exception for safety since it's a fallback block.

replacement = "    except Exception:  # Optimized fix for Jupyter on Windows"

if target in content:
    new_content = content.replace(target, replacement)
    with open(patch_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully patched mcp/os/win32/utilities.py")
else:
    if replacement in content:
        print("Patch already applied.")
    else:
        print("Could not find target line to patch. Printing file head for debug:")
        print(content[:500])
