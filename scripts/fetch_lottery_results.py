#!/usr/bin/env python3
"""
fetch_lottery_results.py — 每日抓取各彩種最新開獎結果
GitHub Actions 用，更新 scripts/lottery_data/results/*.json
"""
import json, os, sys
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests")
    import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery_data", "results")
STATS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery_data", "stats")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATS_DIR, exist_ok=True)

MAGAYO_KEY = "BVtcKUz4y2wFvBmpgr"

def load_existing(slug):
    path = os.path.join(DATA_DIR, f"{slug}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_results(slug, draws):
    # Sort by date desc, deduplicate
    seen = set()
    unique = []
    for d in draws:
        key = d["date"]
        if key not in seen:
            seen.add(key)
            unique.append(d)
    unique.sort(key=lambda x: x["date"], reverse=True)
    
    path = os.path.join(DATA_DIR, f"{slug}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False)
    return len(unique)

def recalc_stats(slug, draws, pick_range, bonus_range):
    """Recalculate hot/cold stats from draws"""
    from collections import Counter
    main_counter = Counter()
    main_last = {}
    total = len(draws)
    
    for i, d in enumerate(draws):
        for n in d.get("numbers", []):
            main_counter[n] += 1
            if n not in main_last:
                main_last[n] = i
    
    stats = {"total_draws": total, "main_numbers": [], "bonus_numbers": []}
    for n in range(1, pick_range + 1):
        stats["main_numbers"].append({
            "number": n,
            "count": main_counter.get(n, 0),
            "frequency": round(main_counter.get(n, 0) / total * 100, 2) if total > 0 else 0,
            "last_seen": main_last.get(n, total),
        })
    
    path = os.path.join(STATS_DIR, f"{slug}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False)


# ============================================================
# FETCH FUNCTIONS PER LOTTERY
# ============================================================

def fetch_powerball():
    """Powerball — data.ny.gov"""
    slug = "powerball"
    existing = load_existing(slug)
    try:
        r = requests.get("https://data.ny.gov/resource/d6yy-54nr.json?$order=draw_date%20DESC&$limit=10", timeout=15)
        r.raise_for_status()
        data = r.json()
        new_draws = []
        for d in data:
            date = d.get("draw_date", "")[:10]
            nums_str = d.get("winning_numbers", "")
            if not nums_str:
                continue
            parts = nums_str.strip().split()
            if len(parts) < 6:
                continue
            numbers = [int(x) for x in parts[:5]]
            bonus = [int(parts[5])]
            multiplier = d.get("multiplier")
            new_draws.append({"date": date, "numbers": numbers, "bonus": bonus, "multiplier": multiplier})
        
        all_draws = new_draws + existing
        count = save_results(slug, all_draws)
        recalc_stats(slug, all_draws[:count], 69, 26)
        print(f"  ✅ {slug}: {count} total draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")

def fetch_mega_millions():
    """Mega Millions — data.ny.gov"""
    slug = "mega-millions"
    existing = load_existing(slug)
    try:
        r = requests.get("https://data.ny.gov/resource/5xaw-6ayf.json?$order=draw_date%20DESC&$limit=10", timeout=15)
        r.raise_for_status()
        data = r.json()
        new_draws = []
        for d in data:
            date = d.get("draw_date", "")[:10]
            nums_str = d.get("winning_numbers", "")
            if not nums_str:
                continue
            parts = nums_str.strip().split()
            if len(parts) < 6:
                continue
            numbers = [int(x) for x in parts[:5]]
            bonus = [int(parts[5])]
            multiplier = d.get("mega_ball", None)
            new_draws.append({"date": date, "numbers": numbers, "bonus": bonus})
        
        all_draws = new_draws + existing
        count = save_results(slug, all_draws)
        recalc_stats(slug, all_draws[:count], 70, 24)
        print(f"  ✅ {slug}: {count} total draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")

def fetch_taiwan(slug, game_code, pick_range, bonus_range):
    """Taiwan lotteries — api.taiwanlottery.com"""
    existing = load_existing(slug)
    try:
        url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/LastNumber?gameCode={game_code}&count=10"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        new_draws = []
        items = data.get("content", {}).get("lotteryNumbers", [])
        for item in items:
            date = item.get("period", "")
            # Parse date from period format
            draw_date = item.get("date", "")
            if not draw_date and "period" in item:
                draw_date = item.get("drawDate", "")
            
            nums = []
            bonus_nums = []
            
            # Try different field names
            for key in ["normalNumbers", "numbers"]:
                if key in item and item[key]:
                    if isinstance(item[key], list):
                        nums = [int(n) for n in item[key]]
                    elif isinstance(item[key], str):
                        nums = [int(n) for n in item[key].split(",")]
                    break
            
            for key in ["specialNumbers", "special"]:
                if key in item and item[key]:
                    if isinstance(item[key], list):
                        bonus_nums = [int(n) for n in item[key]]
                    elif isinstance(item[key], str):
                        bonus_nums = [int(n) for n in item[key].split(",")]
                    break
            
            if nums and draw_date:
                new_draws.append({"date": draw_date[:10], "numbers": sorted(nums), "bonus": sorted(bonus_nums)})
        
        all_draws = new_draws + existing
        count = save_results(slug, all_draws)
        recalc_stats(slug, all_draws[:count], pick_range, bonus_range)
        print(f"  ✅ {slug}: {count} total draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")

def fetch_magayo(slug, game_id, pick_range, bonus_range):
    """Magayo API lotteries"""
    existing = load_existing(slug)
    try:
        url = f"https://api.magayo.com/results.php?api_key={MAGAYO_KEY}&game={game_id}"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        if data.get("error"):
            print(f"  ⚠️ {slug}: magayo error {data.get('error')}")
            return
        
        date = data.get("draw_date", "")
        nums_str = data.get("result", "")
        if not nums_str or not date:
            print(f"  ⚠️ {slug}: no data from magayo")
            return
        
        parts = nums_str.split("-")
        numbers = [int(x) for x in parts]
        
        # Check if bonus is separate
        bonus = []
        bonus_str = data.get("bonus", "")
        if bonus_str:
            bonus = [int(x) for x in bonus_str.split("-")]
        
        new_draw = {"date": date, "numbers": sorted(numbers), "bonus": sorted(bonus)}
        all_draws = [new_draw] + existing
        count = save_results(slug, all_draws)
        recalc_stats(slug, all_draws[:count], pick_range, bonus_range)
        print(f"  ✅ {slug}: {count} total draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")

def fetch_mega_sena():
    """Mega-Sena — caixa.gov.br"""
    slug = "mega-sena"
    existing = load_existing(slug)
    try:
        r = requests.get("https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/", timeout=15)
        r.raise_for_status()
        data = r.json()
        
        date_str = data.get("dataApuracao", "")
        # Convert DD/MM/YYYY to YYYY-MM-DD
        if "/" in date_str:
            parts = date_str.split("/")
            date = f"{parts[2]}-{parts[1]}-{parts[0]}"
        else:
            date = date_str
        
        nums = [int(x) for x in data.get("listaDezenas", [])]
        
        if nums and date:
            new_draw = {"date": date, "numbers": sorted(nums), "bonus": []}
            all_draws = [new_draw] + existing
            count = save_results(slug, all_draws)
            recalc_stats(slug, all_draws[:count], 60, 0)
            print(f"  ✅ {slug}: {count} total draws")
        else:
            print(f"  ⚠️ {slug}: no data")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")

def fetch_euromillions():
    """EuroMillions — GitHub archive"""
    slug = "euromillions"
    existing = load_existing(slug)
    try:
        url = "https://raw.githubusercontent.com/daowa89/lottery-archive/main/euromillions.csv"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        
        lines = r.text.strip().split("\n")
        new_draws = []
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(",")
            if len(parts) >= 8:
                date = parts[0]
                numbers = sorted([int(parts[i]) for i in range(1, 6)])
                bonus = sorted([int(parts[i]) for i in range(6, 8)])
                new_draws.append({"date": date, "numbers": numbers, "bonus": bonus})
        
        all_draws = new_draws + existing
        count = save_results(slug, all_draws)
        recalc_stats(slug, all_draws[:count], 50, 12)
        print(f"  ✅ {slug}: {count} total draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")

def fetch_lotto_6aus49():
    """Lotto 6aus49 — GitHub archive"""
    slug = "lotto-6aus49"
    existing = load_existing(slug)
    try:
        url = "https://raw.githubusercontent.com/daowa89/lottery-archive/main/lotto6aus49.csv"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        
        lines = r.text.strip().split("\n")
        new_draws = []
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) >= 8:
                date = parts[0]
                numbers = sorted([int(parts[i]) for i in range(1, 7)])
                bonus = [int(parts[7])] if len(parts) > 7 else []
                new_draws.append({"date": date, "numbers": numbers, "bonus": bonus})
        
        all_draws = new_draws + existing
        count = save_results(slug, all_draws)
        recalc_stats(slug, all_draws[:count], 49, 9)
        print(f"  ✅ {slug}: {count} total draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")


# ============================================================
# MAIN
# ============================================================
def main():
    print(f"=== Lottery Results Fetch — {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} ===\n")
    
    # US
    fetch_powerball()
    fetch_mega_millions()
    
    # Taiwan
    fetch_taiwan("taiwan-bingo", "5134", 38, 8)
    fetch_taiwan("taiwan-lotto", "5118", 49, 49)
    fetch_taiwan("daily-cash", "1197", 39, 0)
    
    # Europe
    fetch_euromillions()
    fetch_lotto_6aus49()
    fetch_magayo("uk-lotto", "uk_lotto", 59, 0)
    fetch_magayo("oz-lotto", "au_oz_lotto", 47, 47)
    fetch_magayo("lotto-max", "ca_lotto_max", 50, 0)
    
    # Brazil
    fetch_mega_sena()
    
    # These don't have reliable free APIs yet — skip silently
    for slug in ["korea-lotto", "japan-loto6", "el-gordo", "superenalotto"]:
        existing = load_existing(slug)
        if existing:
            print(f"  ⏭️ {slug}: kept {len(existing)} existing draws (no free API)")
        else:
            print(f"  ⏭️ {slug}: no data, no API available")
    
    print(f"\n✅ Fetch complete!")


if __name__ == "__main__":
    main()
