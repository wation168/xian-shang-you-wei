import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JS_PATH = os.path.join(SCRIPT_DIR, "..", "backend", "frontend", "common", "softglow-common.js")

with open(JS_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Find and remove the injected patch block
marker = "/* SOFTGLOW_SEARCH_FIX_V2 */"
if marker in content:
    # The patch is everything from the marker to the end of the _sgSearch function
    # Find the full injected block (ends with };\n before original code)
    start = content.find(marker)
    # Find "window._sgSearch = function" and its closing "};\n"
    # Count braces to find the correct end
    func_start = content.find("window._sgSearch", start)
    if func_start >= 0:
        # Find the opening { of the function
        brace_start = content.find("{", func_start)
        depth = 0
        pos = brace_start
        while pos < len(content):
            if content[pos] == "{":
                depth += 1
            elif content[pos] == "}":
                depth -= 1
                if depth == 0:
                    # Found the closing brace
                    # Skip the trailing ";\n"
                    end = pos + 1
                    if end < len(content) and content[end] == ";":
                        end += 1
                    if end < len(content) and content[end] == "\n":
                        end += 1
                    break
            pos += 1

        removed = content[start:end]
        content = content[:start] + content[end:]
        print(f"REMOVED patch ({len(removed)} chars)")
    else:
        print("WARNING: marker found but no _sgSearch function")
else:
    print("No patch found, file is clean")

# Save restored file
with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nFile size: {len(content)} chars")

# Now show the search-related code
print("\n=== Search-related code ===")
for keyword in ["filter(", "search", "indexOf", "includes"]:
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower() and len(line.strip()) > 10:
            print(f"  Line {i+1}: {line.strip()[:120]}")

print(f"\n=== First 300 chars ===")
print(content[:300])
