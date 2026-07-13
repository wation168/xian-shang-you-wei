import os, re

errs = 0
pound = 0
total = 0
err_files = []
pound_files = []

for r, _, fs in os.walk("."):
    for f in fs:
        if not f.endswith(".html") or f == "index.html":
            continue
        total += 1
        t = open(os.path.join(r, f), "r", encoding="utf-8").read()
        if chr(163) in t:
            pound += 1
            if pound <= 5:
                pound_files.append(os.path.join(r, f))
        ids = set(re.findall(r'getElementById\(["\']([^"\']+)', t))
        html_ids = set(re.findall(r'id=["\']([^"\']+)', t))
        missing = ids - html_ids
        if missing:
            errs += 1
            if errs <= 5:
                err_files.append((os.path.join(r, f), missing))

print(f"Total: {total}")
print(f"JS ID mismatch: {errs}")
print(f"Contains pound sign: {pound}")
if err_files:
    print("\nSample JS errors:")
    for fp, ms in err_files:
        print(f"  {fp}: {ms}")
if pound_files:
    print("\nSample pound files:")
    for fp in pound_files:
        print(f"  {fp}")
