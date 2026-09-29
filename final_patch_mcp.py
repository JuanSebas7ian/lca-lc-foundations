import os

patch_path = r"f:\Cursos_code\lca-lc-foundations\.venv\Lib\site-packages\mcp\os\win32\utilities.py"

if not os.path.exists(patch_path):
    print(f"Error: Path {patch_path} not found.")
    exit(1)

with open(patch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace ALL occurrences of the too-narrow catch
target = "    except NotImplementedError:"
replacement = "    except Exception:  # Patched for Jupyter on Windows"

if target in content:
    new_content = content.replace(target, replacement)
    # Also handle the one I already patched (which might have 'Exception as e' now)
    # If I used 'except Exception as e:' in the previous step, I should normalize it.

    # Just to be sure, let's do a global replace for any narrow catches in this context
    # Usually they follow an anyio.open_process call.

    with open(patch_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully patched ALL occurrences in mcp/os/win32/utilities.py")
else:
    print("Could not find any target lines. Maybe already patched or wrong version?")
    # Check if 'except Exception:' already exists
    if replacement in content:
        print("Patch appears to be already present.")
    else:
        # Let's check for the one I modified with Exception as e
        if "except Exception as e:" in content:
            new_content = content.replace("except Exception as e:", replacement)
            with open(patch_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Normalized previous patch and potentially found others.")
