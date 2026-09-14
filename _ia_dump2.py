p=r'D:\\xian-shang-you-wei\\backend\\frontend\\index.html'
lines=open(p,encoding="utf-8").read().splitlines()
print("--- homeGo ---")
for i, l in enumerate(lines, 1):
    if "function _homeGo" in l or l.startswith("function showPage") or "function renderHomeDash" in l or
          "function _observeHomeDash" in l:
        print(i, l)
print("--- __homeGo body ---")
for i, l in enumerate(lines, 1):
    if l.startswith("function _homeGo"):
        for j in range(i, i+60):
            print(j, lines[j] [0:170])
        break
