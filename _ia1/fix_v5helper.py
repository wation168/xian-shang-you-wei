from pathlib import Path
p = Path(r"D:/xian-shang-you-wei/_ia1/v5.css")
if p.exists():
    t = p.read_text(encoding="utf-8")
    t2 = t.replace("#homeDash.result-open #homeFlow{display:none}\n", "")
    p.write_text(t2, encoding="utf-8")
    print("v5.css helper updated", "#homeFlow{display:none}" in t2)
else:
    print("no helper v5")
