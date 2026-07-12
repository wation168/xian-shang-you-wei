import re

path = "generate_comparison_pages.py"
t = open(path, "r", encoding="utf-8").read()

# Fix: extract data.get() calls out of f-string to avoid {{}} issue
t = t.replace('data.get("intro", {{}}).get("html", "")', '{intro_html}')
t = t.replace('data.get("when_to_use", {{}}).get("a", "")', '{when_a_text}')
t = t.replace('data.get("when_to_use", {{}}).get("b", "")', '{when_b_text}')
t = t.replace('data.get("combined_strategy", {{}}).get("html", "")', '{combined_html}')
t = t.replace('data.get("verdict", {{}}).get("html", "")', '{verdict_html}')

# Add variable definitions before the f-string
old_line = '    html = f\'\'\'<!DOCTYPE html>'
new_line = '''    intro_html = data.get("intro", {}).get("html", "")
    when_a_text = data.get("when_to_use", {}).get("a", "")
    when_b_text = data.get("when_to_use", {}).get("b", "")
    combined_html = data.get("combined_strategy", {}).get("html", "")
    verdict_html = data.get("verdict", {}).get("html", "")

    html = f\'\'\'<!DOCTYPE html>'''

t = t.replace(old_line, new_line, 1)

open(path, "w", encoding="utf-8").write(t)
print("Fixed!")
