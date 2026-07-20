"""
彩票站 PostgreSQL 資料匯出腳本
在本機執行，會在同一目錄產生 lottery_data/ 資料夾，裡面有所有 JSON 檔案
"""
import json
import os
import sys

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("安裝 psycopg2...")
    os.system(f"{sys.executable} -m pip install psycopg2-binary")
    import psycopg2
    import psycopg2.extras

DB_URL = "postgresql://root:W79ods2IylkjUCTY6P8Lcg50Mtphq413@43.203.74.115:31177/zeabur"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery_data")
os.makedirs(OUT_DIR, exist_ok=True)

def export_table(cur, table_name, filename=None, query=None):
    """匯出一個表到 JSON"""
    fname = filename or f"{table_name}.json"
    sql = query or f"SELECT * FROM {table_name} ORDER BY 1"
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        data = []
        for row in rows:
            obj = {}
            for i, val in enumerate(row):
                # Convert non-serializable types
                if val is None:
                    obj[cols[i]] = None
                elif hasattr(val, 'isoformat'):
                    obj[cols[i]] = val.isoformat()
                else:
                    obj[cols[i]] = val
            data.append(obj)
        
        path = os.path.join(OUT_DIR, fname)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ {fname}: {len(data)} 筆")
        return len(data)
    except Exception as e:
        print(f"  ❌ {fname}: {e}")
        return 0

def main():
    print(f"連接 PostgreSQL...")
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=15)
    except Exception as e:
        print(f"❌ 連線失敗: {e}")
        print("請確認 Zeabur PostgreSQL 服務已啟動")
        return
    
    print(f"✅ 已連線\n")
    cur = conn.cursor()
    
    # 1. 列出所有表
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
    tables = [r[0] for r in cur.fetchall()]
    print(f"資料庫共有 {len(tables)} 個表: {', '.join(tables)}\n")
    
    # 2. 匯出每個表
    total = 0
    print("開始匯出...")
    
    # lottery_games - 彩種基本資料
    total += export_table(cur, "lottery_games")
    
    # draw_results - 開獎記錄（全部匯出）
    total += export_table(cur, "draw_results", query="""
        SELECT dr.*, lg.slug as lottery_slug 
        FROM draw_results dr 
        JOIN lottery_games lg ON dr.lottery_id = lg.id 
        ORDER BY dr.draw_date DESC
    """)
    
    # number_statistics - 號碼統計
    total += export_table(cur, "number_statistics", query="""
        SELECT ns.*, lg.slug as lottery_slug 
        FROM number_statistics ns 
        JOIN lottery_games lg ON ns.lottery_id = lg.id 
        ORDER BY lg.slug, ns.number
    """)
    
    # seo_pages - SEO 內容
    total += export_table(cur, "seo_pages", query="""
        SELECT sp.*, lg.slug as lottery_slug 
        FROM seo_pages sp 
        JOIN lottery_games lg ON sp.lottery_id = lg.id 
        ORDER BY lg.slug, sp.page_type
    """)
    
    # subscribers - 訂閱（如果有）
    if "subscribers" in tables:
        total += export_table(cur, "subscribers")
    
    # 匯出其他未知的表
    known = {"lottery_games", "draw_results", "number_statistics", "seo_pages", "subscribers"}
    for t in tables:
        if t not in known:
            total += export_table(cur, t)
    
    # 3. 額外：按彩種分開的開獎資料（方便前端引用）
    print("\n按彩種分開匯出開獎資料...")
    os.makedirs(os.path.join(OUT_DIR, "results"), exist_ok=True)
    
    cur.execute("SELECT id, slug FROM lottery_games ORDER BY slug")
    games = cur.fetchall()
    
    for game_id, slug in games:
        cur.execute("""
            SELECT draw_date, draw_number, numbers, bonus_numbers, jackpot, winners, extra_data
            FROM draw_results 
            WHERE lottery_id = %s 
            ORDER BY draw_date DESC
        """, (game_id,))
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        data = []
        for row in rows:
            obj = {}
            for i, val in enumerate(row):
                if val is None:
                    obj[cols[i]] = None
                elif hasattr(val, 'isoformat'):
                    obj[cols[i]] = val.isoformat()
                else:
                    obj[cols[i]] = val
            data.append(obj)
        
        path = os.path.join(OUT_DIR, "results", f"{slug}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ results/{slug}.json: {len(data)} 筆")
    
    conn.close()
    print(f"\n🎉 匯出完成！共 {total} 筆資料")
    print(f"📁 檔案位置: {OUT_DIR}")
    print(f"\n請把整個 lottery_data 資料夾上傳給我")

if __name__ == "__main__":
    main()
