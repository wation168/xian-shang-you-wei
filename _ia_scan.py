p=r'D:\\xian-shang-you-wei\\backend\\frontend\\index.html'
lines=open(p,encoding="utf-8").read().splitlines()
for i, l in enumerate(lines, 1):
    if "homeDash" in l or "homeMkt" in l or "stockInput" in l or "desktopTabBar" in l or "hotkeysEl" in l:
        if len(l) < 200:
            print(i, l)
        else:
            print(i, l[:160])
