# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")
t2 = t.replace("data.is_paid&&p.content", "p.content")
t2 = t2.replace("${!data.is_paid?`<div style=\"font-size:11px;color:var(--text3);margin-top:4px;display:flex;align-items:center;gap:4px\"><span>🔒</span>加入會員查看完整內容</div>`:''}",
                "${!p.content?`<div style=\"font-size:11px;color:var(--text3);margin-top:4px;display:flex;align-items:center;gap:4px\"><span>🔒</span>登入後可看內文，留言需付費</div>`:''}")
t2 = t2.replace(
    "headers:{'Cache-Control':'no-cache','Pragma':'no-cache'}\n    });",
    "headers:{'Cache-Control':'no-cache','Pragma':'no-cache',...(_authHeaders()||{})}\n    });",
    1,
)
p.write_text(t2, encoding="utf-8")
print("forum is_paid->content", t.count("data.is_paid&&p.content"), "->", t2.count("p.content"))
print("desktop auth", t2.count("_authHeaders()||{}"))
