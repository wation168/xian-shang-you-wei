# -*- coding: utf-8 -*-
"""
綠界 ECPay CheckMacValue 簽章驗證（獨立模組）
================================================
放置位置：backend/ecpay_verify.py（跟 main.py 同一層）

設計原則：
  - 所有驗證邏輯都在這支檔案裡，main.py 只負責呼叫，不含任何驗證細節
  - 這支檔案不 import main.py，沒有循環相依，可以單獨執行測試
  - 任何內部錯誤都不會讓 webhook 掛掉（fail-safe，見 check_webhook）

兩階段上線（重要）：
  階段一（預設）：環境變數 ECPAY_VERIFY_ENFORCE 未設定或=0
      → 只「觀察並記錄」，不阻擋任何 webhook。正式付款完全不受影響。
  階段二：確認記錄裡都是 matched=1 之後，在 Zeabur 把 ECPAY_VERIFY_ENFORCE 設成 1
      → 開始真正阻擋簽章不符的偽造請求。不需要改任何程式碼。

查看觀察結果：
  GET /admin/ecpay-verify-log?key=你的ADMIN_API_KEY
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import urllib.parse
from datetime import datetime, timedelta, timezone

_TAIPEI = timezone(timedelta(hours=8))

# .NET 的 HttpUtility.UrlEncode 不會編碼這些字元，Python 的 quote_plus 會，
# 這是兩邊算出來的簽章對不上的最常見原因。
_NET_SAFE = "-_.!*()"

_TABLE = "ecpay_verify_log"
_KEEP_ROWS = 300  # 記錄只保留最近 N 筆，避免無限成長


# ---------------------------------------------------------------------------
# 核心：計算 CheckMacValue
# ---------------------------------------------------------------------------

def _build_raw(params: dict, hash_key: str, hash_iv: str) -> str:
    """步驟 1-2：參數 A→Z 排序後串接，前面加 HashKey、後面加 HashIV。"""
    filtered = {
        k: ("" if v is None else str(v))
        for k, v in params.items()
        if k not in ("CheckMacValue", "HashKey", "HashIV")
    }
    ordered = sorted(filtered.items(), key=lambda kv: kv[0].lower())
    body = "&".join(f"{k}={v}" for k, v in ordered)
    return f"HashKey={hash_key}&{body}&HashIV={hash_iv}"


def _enc_python_default(raw: str) -> str:
    """Python 內建編碼（= main.py 目前 create_order 在用的方式）。"""
    return urllib.parse.quote_plus(raw).lower()


def _enc_dotnet(raw: str) -> str:
    """符合綠界文件要求的 .NET 編碼規則。"""
    return urllib.parse.quote_plus(raw, safe=_NET_SAFE).lower()


def _enc_dotnet_tilde(raw: str) -> str:
    """.NET 編碼，且波浪號另外編成 %7e（部分 .NET 版本的行為）。"""
    return urllib.parse.quote_plus(raw, safe=_NET_SAFE).replace("~", "%7e").lower()


def compute_variants(params: dict, hash_key: str, hash_iv: str) -> dict:
    """
    算出各種編碼規則下的 CheckMacValue。
    因為無法百分之百確定綠界對特殊字元的處理方式，這裡一次算出所有可能的組合，
    觀察階段會記錄「實際是哪一種對上」，之後就能確定該用哪一種。
    """
    raw = _build_raw(params, hash_key, hash_iv)
    encoders = {
        "python_default": _enc_python_default,
        "dotnet": _enc_dotnet,
        "dotnet_tilde": _enc_dotnet_tilde,
    }
    out = {}
    for name, fn in encoders.items():
        encoded = fn(raw)
        out[f"sha256_{name}"] = hashlib.sha256(encoded.encode("utf-8")).hexdigest().upper()
        out[f"md5_{name}"] = hashlib.md5(encoded.encode("utf-8")).hexdigest().upper()
    return out


def verify(params: dict, hash_key: str, hash_iv: str):
    """
    驗證單筆 webhook 的簽章。
    回傳 (是否通過, 對上的編碼方式名稱 或 None)
    """
    received = str(params.get("CheckMacValue", "") or "").upper()
    if not received:
        return False, None
    variants = compute_variants(params, hash_key, hash_iv)
    # 優先序：綠界文件規定的 .NET SHA256 放最前面
    order = [
        "sha256_dotnet",
        "sha256_python_default",
        "sha256_dotnet_tilde",
        "md5_dotnet",
        "md5_python_default",
        "md5_dotnet_tilde",
    ]
    for name in order:
        if variants.get(name) == received:
            return True, name
    return False, None


# ---------------------------------------------------------------------------
# 記錄：寫進資料庫，不依賴即時 log，隨時可查
# ---------------------------------------------------------------------------

def _conn(db_path: str):
    c = sqlite3.connect(db_path, check_same_thread=False, timeout=10)
    c.row_factory = sqlite3.Row
    return c


def _ensure_table(conn) -> None:
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS {_TABLE} (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            source           TEXT,
            merchant_trade_no TEXT,
            matched          INTEGER,
            matched_variant  TEXT,
            received_mac     TEXT,
            expected_json    TEXT,
            params_json      TEXT,
            enforced         INTEGER,
            created_at       TEXT
        )"""
    )


def _record(db_path: str, source: str, params: dict, matched: bool,
            variant, variants: dict, enforced: bool) -> None:
    conn = None
    try:
        conn = _conn(db_path)
        _ensure_table(conn)
        conn.execute(
            f"""INSERT INTO {_TABLE}
                (source, merchant_trade_no, matched, matched_variant,
                 received_mac, expected_json, params_json, enforced, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                source,
                str(params.get("MerchantTradeNo", "")),
                1 if matched else 0,
                variant or "",
                str(params.get("CheckMacValue", "")),
                json.dumps(variants, ensure_ascii=False),
                json.dumps(params, ensure_ascii=False),
                1 if enforced else 0,
                datetime.now(_TAIPEI).strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        # 只留最近 N 筆
        conn.execute(
            f"DELETE FROM {_TABLE} WHERE id NOT IN "
            f"(SELECT id FROM {_TABLE} ORDER BY id DESC LIMIT {_KEEP_ROWS})"
        )
        conn.commit()
    except Exception as e:  # 記錄失敗絕不能影響金流
        print(f"[ecpay_verify] ⚠️ 寫入記錄失敗（不影響付款）：{e}")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def _matched_count(db_path: str, source: str) -> int:
    """查這個來源累計成功驗證過幾次（只會增加，不會被偽造請求拉低）。"""
    conn = None
    try:
        conn = _conn(db_path)
        _ensure_table(conn)
        row = conn.execute(
            f"SELECT COUNT(*) c FROM {_TABLE} WHERE source=? AND matched=1", (source,)
        ).fetchone()
        return int(row["c"]) if row else 0
    except Exception:
        return 0
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def _auto_threshold() -> int:
    try:
        return max(1, int(os.environ.get("ECPAY_VERIFY_AUTO_THRESHOLD", "2")))
    except Exception:
        return 2


def is_enforcing(db_path: str = None, source: str = "ecpay") -> bool:
    """
    是否進入「真正阻擋」模式。

    判斷順序：
      1. 環境變數 ECPAY_VERIFY_ENFORCE 有明確設定 → 以它為準（人工強制開/關）
      2. 否則自動判斷：這個來源已經成功驗證過 N 次真實通知 → 自動開啟阻擋
         （N 預設 2，可用 ECPAY_VERIFY_AUTO_THRESHOLD 調整）

    設計重點：成功次數只增不減，偽造請求無法把它拉回觀察模式。
    """
    manual = os.environ.get("ECPAY_VERIFY_ENFORCE", "").strip()
    if manual in ("1", "true", "True", "yes"):
        return True
    if manual in ("0", "false", "False", "no"):
        return False
    if not db_path:
        return False
    return _matched_count(db_path, source) >= _auto_threshold()


# ---------------------------------------------------------------------------
# main.py 唯一需要呼叫的函式
# ---------------------------------------------------------------------------

def check_webhook(params: dict, hash_key: str, hash_iv: str,
                  db_path: str, source: str = "ecpay") -> bool:
    """
    給 main.py 的 webhook 呼叫。

    回傳 True  → 放行，繼續原本的處理流程
    回傳 False → 應該拒絕（只有在已自動或人工進入阻擋模式時才可能回 False）

    無論如何都不會丟出例外：任何內部錯誤一律放行並印出警告，
    確保這支模組永遠不會變成正式付款失敗的原因。
    """
    try:
        enforcing = is_enforcing(db_path, source)
    except Exception:
        enforcing = False
    try:
        if not hash_key or not hash_iv:
            print("[ecpay_verify] ⚠️ HashKey/HashIV 未設定，略過驗證")
            return True

        variants = compute_variants(params, hash_key, hash_iv)
        matched, variant = verify(params, hash_key, hash_iv)

        _record(db_path, source, params, matched, variant, variants, enforcing)

        if matched:
            done = _matched_count(db_path, source)
            need = _auto_threshold()
            if enforcing:
                print(f"[ecpay_verify] ✅ 簽章驗證通過（{variant}）source={source}｜阻擋模式運作中")
            else:
                print(f"[ecpay_verify] ✅ 簽章驗證通過（{variant}）source={source}｜"
                      f"觀察中 {done}/{need}，達標後自動開始阻擋偽造請求")
            return True

        if enforcing:
            print(f"[ecpay_verify] 🚫 簽章不符，已拒絕此請求 source={source} "
                  f"MerchantTradeNo={params.get('MerchantTradeNo')}")
            return False

        print(f"[ecpay_verify] ⚠️ 簽章不符，但尚未進入阻擋模式，仍放行 source={source} "
              f"MerchantTradeNo={params.get('MerchantTradeNo')}")
        return True

    except Exception as e:
        print(f"[ecpay_verify] ⚠️ 驗證過程發生錯誤，一律放行（不影響付款）：{e}")
        return True


# ---------------------------------------------------------------------------
# 查看記錄用的 API（掛在這支模組裡，main.py 只需 include_router 一行）
# ---------------------------------------------------------------------------

try:
    from fastapi import APIRouter, HTTPException

    router = APIRouter()

    @router.get("/admin/ecpay-verify-log")
    def ecpay_verify_log(key: str = "", limit: int = 20, full: int = 0, q: str = ""):
        """
        查看綠界通知記錄。
          /admin/ecpay-verify-log?key=金鑰                 → 看最近的通知與驗證狀態
          /admin/ecpay-verify-log?key=金鑰&q=someone@x.com → 查特定客人（email 或訂單編號皆可）
          /admin/ecpay-verify-log?key=金鑰&full=1          → 顯示綠界送來的完整原始欄位
        """
        import secrets as _secrets

        admin_key = os.environ.get("ADMIN_API_KEY", "")
        if not admin_key or not _secrets.compare_digest(key, admin_key):
            raise HTTPException(status_code=403, detail="Forbidden")

        db_path = os.environ.get("DB_PATH", "/data/members.db")
        conn = None
        try:
            conn = _conn(db_path)
            _ensure_table(conn)
            n = max(1, min(int(limit), 100))
            kw = (q or "").strip()
            if kw:
                rows = conn.execute(
                    f"""SELECT * FROM {_TABLE}
                        WHERE merchant_trade_no LIKE ? OR params_json LIKE ?
                        ORDER BY id DESC LIMIT ?""",
                    (f"%{kw}%", f"%{kw}%", n),
                ).fetchall()
            else:
                rows = conn.execute(
                    f"SELECT * FROM {_TABLE} ORDER BY id DESC LIMIT ?", (n,)
                ).fetchall()
            total = conn.execute(f"SELECT COUNT(*) c FROM {_TABLE}").fetchone()["c"]
            ok = conn.execute(f"SELECT COUNT(*) c FROM {_TABLE} WHERE matched=1").fetchone()["c"]
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

        _rtn = {"1": "✅ 付款成功", "0": "❌ 付款失敗"}
        items = []
        for r in rows:
            try:
                p = json.loads(r["params_json"] or "{}")
            except Exception:
                p = {}
            item = {
                "時間": r["created_at"],
                "來源": "一次性付款" if r["source"] == "ecpay" else "定期定額扣款",
                "訂單編號": r["merchant_trade_no"],
                "會員Email": p.get("CustomField1", ""),
                "金額": p.get("TradeAmt") or p.get("PeriodAmount") or p.get("Amount", ""),
                "商品": p.get("ItemName", ""),
                "綠界付款結果": _rtn.get(str(p.get("RtnCode", "")), f"其他({p.get('RtnCode','')}) {p.get('RtnMsg','')}"),
                "綠界付款時間": p.get("PaymentDate", ""),
                "簽章是否相符": "✅ 相符" if r["matched"] else "❌ 不符",
                "當時是否阻擋模式": bool(r["enforced"]),
            }
            if full:
                item["對上的編碼方式"] = r["matched_variant"]
                item["收到的CheckMacValue"] = r["received_mac"]
                item["各種算法結果"] = json.loads(r["expected_json"] or "{}")
                item["綠界送來的完整原始欄位"] = p
            items.append(item)

        need = _auto_threshold()
        status = {}
        for src, label in (("ecpay", "一次性付款"), ("ecpay_recurring", "定期定額扣款")):
            done = _matched_count(db_path, src)
            on = is_enforcing(db_path, src)
            status[label] = {
                "目前狀態": "🛡️ 阻擋模式（偽造請求會被拒絕）" if on
                            else f"👀 觀察中（成功驗證 {done}/{need} 次，達標後自動開啟）",
                "累計成功驗證次數": done,
            }

        return {
            "各來源狀態": status,
            "說明": "不需要手動切換，成功驗證次數達標後會自己進入阻擋模式。"
                    f"｜查特定客人請加 &q=email或訂單編號｜只保留最近 {_KEEP_ROWS} 筆",
            "查詢條件": kw or "（未指定，顯示最近的記錄）",
            "本次符合筆數": len(items),
            "資料庫累計筆數": total,
            "其中簽章相符": ok,
            "記錄": items,
        }

except ImportError:  # 沒有 fastapi 時（例如單獨執行本檔案測試）不影響
    router = None


# ---------------------------------------------------------------------------
# 單獨執行本檔案時的自我測試：python ecpay_verify.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 綠界官方公開的測試用金鑰（沙盒），僅用於驗證演算法本身
    K, V = "pwFHCqoQZGmho4w6", "EkRm7iFT261dpevs"

    sample = {
        "MerchantID": "2000132",
        "MerchantTradeNo": "Test1234567",
        "MerchantTradeDate": "2013/03/12 15:30:23",
        "PaymentType": "aio",
        "TotalAmount": "1000",
        "TradeDesc": "測試交易描述",
        "ItemName": "線上有位月費方案",
        "ReturnURL": "https://api.softglow-ai.com/webhook/ecpay",
        "ChoosePayment": "ALL",
    }

    print("=" * 62)
    print("測試 1：來回驗證（自己算出來的簽章，自己要驗得過）")
    variants = compute_variants(sample, K, V)
    for name, mac in variants.items():
        if not name.startswith("sha256"):
            continue
        probe = dict(sample, CheckMacValue=mac)
        ok, hit = verify(probe, K, V)
        print(f"  {name:24s} → {'✅ 通過' if ok else '❌ 失敗'}（對上 {hit}）")

    print()
    print("測試 2：偽造的簽章必須被擋下")
    fake = dict(sample, CheckMacValue="0000000000000000000000000000000000000000000000000000000000000000")
    ok, hit = verify(fake, K, V)
    print(f"  偽造簽章 → {'❌ 竟然通過了，有問題' if ok else '✅ 正確擋下'}")

    print()
    print("測試 3：含特殊字元時，兩種編碼規則會算出不同結果（這正是要觀察的重點）")
    special = dict(sample, ItemName="月費方案(限時)")
    sv = compute_variants(special, K, V)
    same = sv["sha256_python_default"] == sv["sha256_dotnet"]
    print(f"  Python 預設編碼 : {sv['sha256_python_default'][:24]}...")
    print(f"  .NET  規則編碼 : {sv['sha256_dotnet'][:24]}...")
    print(f"  兩者相同？{'是（此例無差異）' if same else '否 → 所以必須靠實際資料判斷用哪一種'}")

    print()
    print("測試 4：確認目前模式")
    print(f"  ECPAY_VERIFY_ENFORCE = {os.environ.get(chr(39))}")
    print(f"  目前為：{'阻擋模式' if is_enforcing() else '觀察模式（安全，不會影響付款）'}")
    print("=" * 62)
