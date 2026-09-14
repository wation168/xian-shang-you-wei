# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("FAIL %s count=%s\n%s" % (label, n, old[:300]))
    t = t.replace(old, new, 1)
    print("OK", label)

rep(
'def get_opening_picks():\n    """開盤熱門股（成交量前20，無需登入）',
'def get_opening_picks(user: dict | None = Depends(get_current_user)):\n    """開盤熱門股（成交量前20；遊客弱預覽／免費藏名／付費全開）',
"opening_sig")

helper = '''
def _picks_payload(rows, updated_at, user):
    st = _taipei_now_str("%Y-%m-%d %H:%M")
    if _is_premium(user):
        return {"data": rows, "updated_at": updated_at, "server_time": st,
                "tier": "paid", "masked": False, "preview": False}
    if user:
        masked = [_deep_mask_item(dict(x)) if isinstance(x, dict) else x for x in rows]
        return {"data": masked, "updated_at": updated_at, "server_time": st,
                "tier": "free", "masked": True, "preview": False}
    n = len(rows or [])
    placeholders = [{
        "stock_id": "＊＊＊＊", "stock_name": "＊＊＊＊",
        "masked": True, "preview": True,
    } for _ in range(min(3, n) if n else 2)]
    return {"data": placeholders, "updated_at": updated_at, "server_time": st,
            "approx_count": n, "tier": "guest", "masked": True, "preview": True}

'''
if "def _picks_payload(" not in t:
    t = t.replace(
        'def get_opening_picks(user: dict | None = Depends(get_current_user)):',
        helper + 'def get_opening_picks(user: dict | None = Depends(get_current_user)):',
        1,
    )
    print("OK picks_helper")

rep(
'''    if not base_data:
        # 2026/07/27：沒資料時也帶上查詢時間，前端才能一律顯示時間那一行
        return {"data": base_data, "updated_at": updated_at,
                "server_time": _taipei_now_str("%Y-%m-%d %H:%M")}''',
'''    if not base_data:
        return _picks_payload(base_data, updated_at, user)''',
"opening_empty")

rep(
'''    return {"data": enriched, "updated_at": updated_at,
            "server_time": _taipei_now_str("%Y-%m-%d %H:%M")}''',
'''    return _picks_payload(enriched, updated_at, user)''',
"opening_full")

p.write_text(t, encoding="utf-8")
print("P5_DONE")
