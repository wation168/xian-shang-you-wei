# -*- coding: utf-8 -*-
from pathlib import Path
import re, subprocess
root = Path(r"D:\xian-shang-you-wei")
idx = (root/"backend/frontend/index.html").read_text(encoding="utf-8")
main = (root/"backend/main.py").read_text(encoding="utf-8")
il, ml = idx.splitlines(), main.splitlines()

def lineno(text, needle):
    i = text.find(needle)
    return text[:i].count("\n")+1 if i>=0 else None

print("B1 analyze 429 helper", lineno(idx, "_handleQuotaLimit(_j429"))
print("B1 pf 429", lineno(idx, "_handleQuotaLimit(j429"))
print("B1 _handleQuotaLimit def", lineno(idx, "function _handleQuotaLimit"))
print("B2 deep lock", lineno(idx, "lock-ov-deep"))
print("B2 _applyResultMasks", lineno(idx, "function _applyResultMasks"))
print("nit report sig", lineno(main, "def report_generate(req: ReportReq, request: Request,"))
print("nit referral", lineno(main, "return exp >= _taipei_today()"))
print("quota_429", lineno(main, "def _quota_429"))

# show _applyResultMasks locked vs deepLocked
i = idx.find("function _applyResultMasks")
print("\n--- masks excerpt ---")
print(idx[i:i+700])
print("...")
j = idx.find("B2：")
print(idx[j:j+700])

print("\n--- analyze 429 ---")
print(idx[idx.find("if(r.status===429)"):idx.find("if(r.status===429)")+420])

print("\n--- pf 429 ---")
print(idx[idx.find("if(r.status===429 ||"):idx.find("if(r.status===429 ||")+380])

fails=[]
def ok(c,m):
    print(("OK" if c else "FAIL"), m)
    if not c: fails.append(m)
ok("_handleQuotaLimit" in idx and "_handleQuotaLimit(_j429" in idx, "analyze uses helper")
ok("_handleQuotaLimit(j429" in idx, "pf uses helper")
ok("lock-ov-deep" in idx and "deepLocked = !_hasPremium()" in idx, "B2 independent deep lock")
ok("locked = _creditExhausted()" in idx, "general pack still credit-gated")
ok("request: Request," in re.search(r"def report_generate\([^\)]+\)", main).group(0) and "= None" not in re.search(r"def report_generate\([^\)]+\)", main).group(0), "report Request required")
ok("return exp >= _taipei_today()" in main, "referral taipei")
ok("def _quota_429" in main, "429+credit helper")
print("VERIFY", "OK" if not fails else fails)
r=subprocess.run(["git","diff","--stat","backend/main.py","backend/frontend/index.html"], cwd=str(root), capture_output=True, text=True)
print(r.stdout)
