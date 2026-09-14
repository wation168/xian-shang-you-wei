p=r'D:\\xian-shang-you-wei\\backend\\frontend\\index.html'
lines=open(p,encoding="utf-8").read().splitlines()
print("--- HTML 730-910 ---")
for i in range(730, 911):
    print("%5d|%s" % (i, lines[i-1][0:180]))
