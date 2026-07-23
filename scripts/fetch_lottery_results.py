#!/usr/bin/env python3
"""
fetch_lottery_results.py — 每日抓取各彩種最新開獎結果
GitHub Actions 用，更新 scripts/lottery_data/results/*.json

資料來源清單（2026/07/23 更新）：
  ✅ powerball        — data.ny.gov 公開 API
  ✅ mega-millions    — data.ny.gov 公開 API
  ✅ taiwan-bingo     — api.taiwanlottery.com 官方 API
  ✅ taiwan-lotto     — api.taiwanlottery.com 官方 API
  ✅ daily-cash       — api.taiwanlottery.com 官方 API
  ✅ mega-sena        — caixa.gov.br 官方 API
  ✅ euromillions     — euromillions.api.pedromealha.dev 免費 API
  ✅ lotto-6aus49     — JohannesFriedrich GitHub Archive
  ✅ uk-lotto         — magayo API（加 DNS fallback）
  ✅ oz-lotto         — magayo API（加 DNS fallback）
  ✅ lotto-max        — magayo API（加 DNS fallback）
  ✅ korea-lotto      — dhlottery.co.kr 官方 JSON API
  ✅ japan-loto6      — lottolyzer.com 爬蟲
  ✅ el-gordo         — loteriasyapuestas.es 官網爬蟲
  ✅ superenalotto    — superenalotto.net 爬蟲
"""
import json, os, re, sys, socket
from datetime import datetime, timedelta, date

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests")
    import requests

# Suppress InsecureRequestWarning for verify=False
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery_data", "results")
STATS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery_data", "stats")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATS_DIR, exist_ok=True)

MAGAYO_KEY = "BVtcKUz4y2wFvBmpgr"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def load_existing(slug):
    path = os.path.join(DATA_DIR, f"{slug}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_results(slug, draws):
    """Sort by date desc, deduplicate, save"""
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


def _save_and_report(slug, new_draws, existing, pick_range, bonus_range):
    """Common helper: merge, save, recalc stats, print result"""
    all_draws = new_draws + existing
    count = save_results(slug, all_draws)
    recalc_stats(slug, all_draws[:count], pick_range, bonus_range)
    new_count = count - len(existing) if count > len(existing) else 0
    print(f"  ✅ {slug}: {count} total draws (+{new_count} new)")


# ============================================================
# FETCH FUNCTIONS — 已有且能用的（保留原邏輯）
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
            dt = d.get("draw_date", "")[:10]
            nums_str = d.get("winning_numbers", "")
            if not nums_str:
                continue
            parts = nums_str.strip().split()
            numbers = [int(x) for x in parts[:5]]
            pb = d.get("powerball")
            if pb is not None:
                bonus = [int(pb)]
            elif len(parts) >= 6:
                bonus = [int(parts[5])]
            else:
                bonus = []
            multiplier = d.get("multiplier")
            if numbers:
                new_draws.append({"date": dt, "numbers": numbers, "bonus": bonus, "multiplier": multiplier})
        _save_and_report(slug, new_draws, existing, 69, 26)
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
            dt = d.get("draw_date", "")[:10]
            nums_str = d.get("winning_numbers", "")
            if not nums_str:
                continue
            parts = nums_str.strip().split()
            numbers = [int(x) for x in parts[:5]]
            mega_ball = d.get("mega_ball")
            if mega_ball is not None:
                bonus = [int(mega_ball)]
            elif len(parts) >= 6:
                bonus = [int(parts[5])]
            else:
                bonus = []
            if numbers:
                new_draws.append({"date": dt, "numbers": numbers, "bonus": bonus})
        _save_and_report(slug, new_draws, existing, 70, 24)
    except Exception as e:
        print(f"  ❌ {slug}: {e}")


def fetch_taiwan(slug, game_code, pick_range, bonus_range):
    """Taiwan lotteries — api.taiwanlottery.com (2026/07 new API format)"""
    existing = load_existing(slug)
    try:
        url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/LastNumber?gameCode={game_code}&count=10"
        r = requests.get(url, timeout=15, verify=False)
        r.raise_for_status()
        data = r.json()
        new_draws = []
        items = data.get("content", {}).get("lastNumberList", [])
        if not items:
            items = data.get("content", {}).get("lotteryNumbers", [])
        for item in items:
            item_code = item.get("gameCode")
            if item_code is not None and str(item_code) != str(game_code):
                continue
            draw_date = item.get("drawDate", "") or item.get("date", "")
            if not draw_date:
                continue
            draw_date = draw_date[:10]
            nums = []
            bonus_nums = []
            if "lotNumber" in item and item["lotNumber"]:
                lot = item["lotNumber"]
                if isinstance(lot, list):
                    all_nums = [int(n) for n in lot]
                    if bonus_range > 0 and len(all_nums) > pick_range:
                        nums = all_nums[:pick_range]
                        bonus_nums = all_nums[pick_range:]
                    else:
                        nums = all_nums
            if not nums:
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
                new_draws.append({"date": draw_date, "numbers": sorted(nums), "bonus": sorted(bonus_nums)})
        _save_and_report(slug, new_draws, existing, pick_range, bonus_range)
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
        if "/" in date_str:
            parts = date_str.split("/")
            dt = f"{parts[2]}-{parts[1]}-{parts[0]}"
        else:
            dt = date_str
        nums = [int(x) for x in data.get("listaDezenas", [])]
        if nums and dt:
            new_draws = [{"date": dt, "numbers": sorted(nums), "bonus": []}]
            _save_and_report(slug, new_draws, existing, 60, 0)
        else:
            print(f"  ⚠️ {slug}: no data")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")


# ============================================================
# FETCH FUNCTIONS — lottolyzer.com 通用爬蟲
# ============================================================

def fetch_lottolyzer(slug, lottolyzer_path, pick_range, bonus_range, expected_nums=None):
    """Generic lottolyzer.com scraper — works for all lotteries on that site.
    All lottolyzer history pages use the same HTML table structure:
      <td class="sum-p1">YYYY-MM-DD</td>     ← Date
      <td class="sum-p1">N,N,N,...</td>       ← Winning numbers
      <td class="sum-p1">N[,N]</td>           ← Bonus/Supp (if column exists)
    """
    existing = load_existing(slug)
    try:
        url = f"https://en.lottolyzer.com/history/{lottolyzer_path}"
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.raise_for_status()
        html = r.text

        new_draws = []

        # Try 3-column match first (date + numbers + bonus)
        rows = re.findall(
            r'<td class="sum-p1">\s*(\d{4}-\d{2}-\d{2})\s*</td>\s*'
            r'<td class="sum-p1">\s*([\d,]+)\s*</td>\s*'
            r'<td class="sum-p1">\s*([\d,]+)\s*</td>',
            html
        )
        if rows:
            for dt, nums_str, bonus_str in rows:
                nums = sorted([int(n) for n in nums_str.split(",")])
                bonus = sorted([int(n) for n in bonus_str.split(",")])
                if expected_nums is None or len(nums) == expected_nums:
                    new_draws.append({"date": dt, "numbers": nums, "bonus": bonus})

        # Fallback: 2-column match (date + numbers, no bonus column)
        if not new_draws:
            rows2 = re.findall(
                r'<td class="sum-p1">\s*(\d{4}-\d{2}-\d{2})\s*</td>\s*'
                r'<td class="sum-p1">\s*([\d,]+)\s*</td>',
                html
            )
            for dt, nums_str in rows2:
                nums = sorted([int(n) for n in nums_str.split(",")])
                if expected_nums is None or len(nums) == expected_nums:
                    new_draws.append({"date": dt, "numbers": nums, "bonus": []})

        if new_draws:
            _save_and_report(slug, new_draws, existing, pick_range, bonus_range)
        else:
            print(f"  ⚠️ {slug}: lottolyzer scrape found no data, keeping {len(existing)} existing draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")
        if existing:
            print(f"      (keeping {len(existing)} existing draws)")


# ============================================================
# FETCH FUNCTIONS — magayo（加 DNS fallback）
# ============================================================

def _resolve_magayo():
    """Try to resolve api.magayo.com, fallback to known IPs if DNS fails"""
    try:
        ip = socket.gethostbyname("api.magayo.com")
        return ip
    except socket.gaierror:
        # Known IPs for api.magayo.com (may change, but worth trying)
        known_ips = ["104.21.77.194", "172.67.198.194"]
        for ip in known_ips:
            try:
                r = requests.get(f"https://{ip}/results.php?api_key={MAGAYO_KEY}&game=uk_lotto",
                                 headers={**HEADERS, "Host": "api.magayo.com"},
                                 timeout=10, verify=False)
                if r.status_code == 200:
                    return ip
            except Exception:
                continue
    return None


def fetch_magayo(slug, game_id, pick_range, bonus_range):
    """Magayo API lotteries with DNS fallback"""
    existing = load_existing(slug)
    try:
        # Try normal DNS first
        url = f"https://api.magayo.com/results.php?api_key={MAGAYO_KEY}&game={game_id}"
        try:
            r = requests.get(url, timeout=15, headers=HEADERS)
            r.raise_for_status()
        except (requests.exceptions.ConnectionError, socket.gaierror):
            # DNS failed, try IP fallback
            print(f"  ⚠️ {slug}: magayo DNS failed, trying IP fallback...")
            magayo_ip = _resolve_magayo()
            if not magayo_ip:
                print(f"  ❌ {slug}: magayo unreachable (DNS + IP fallback failed)")
                return
            url = f"https://{magayo_ip}/results.php?api_key={MAGAYO_KEY}&game={game_id}"
            r = requests.get(url, timeout=15, headers={**HEADERS, "Host": "api.magayo.com"}, verify=False)
            r.raise_for_status()

        data = r.json()
        if data.get("error"):
            print(f"  ⚠️ {slug}: magayo error {data.get('error')}")
            return
        dt = data.get("draw_date", "")
        nums_str = data.get("result", "")
        if not nums_str or not dt:
            print(f"  ⚠️ {slug}: no data from magayo")
            return
        parts = nums_str.split("-")
        numbers = [int(x) for x in parts]
        bonus = []
        bonus_str = data.get("bonus", "")
        if bonus_str:
            bonus = [int(x) for x in bonus_str.split("-")]
        new_draws = [{"date": dt, "numbers": sorted(numbers), "bonus": sorted(bonus)}]
        _save_and_report(slug, new_draws, existing, pick_range, bonus_range)
    except Exception as e:
        print(f"  ❌ {slug}: {e}")


# ============================================================
# FETCH FUNCTIONS — 新增替代來源
# ============================================================

def fetch_euromillions():
    """EuroMillions — lottolyzer.com 爬蟲（pedromealha API 被限流 429）
    HTML 結構（已驗證 2026/07/23）：
      <td class="sum-p1">2026-07-21</td>               ← Date
      <td class="sum-p1">2,3,8,28,39</td>              ← 5 main numbers
      <td class="sum-p1">2,11</td>                     ← 2 Lucky Stars (comma-separated)
    """
    slug = "euromillions"
    existing = load_existing(slug)
    try:
        url = "https://en.lottolyzer.com/history/multi-country/euromillions"
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.raise_for_status()
        html = r.text

        new_draws = []
        rows = re.findall(
            r'<td class="sum-p1">\s*(\d{4}-\d{2}-\d{2})\s*</td>\s*'
            r'<td class="sum-p1">\s*([\d,]+)\s*</td>\s*'
            r'<td class="sum-p1">\s*([\d,]+)\s*</td>',
            html
        )
        for dt, nums_str, bonus_str in rows:
            nums = sorted([int(n) for n in nums_str.split(",")])
            bonus = sorted([int(n) for n in bonus_str.split(",")])
            if len(nums) == 5:
                new_draws.append({"date": dt, "numbers": nums, "bonus": bonus})

        if new_draws:
            _save_and_report(slug, new_draws, existing, 50, 12)
        else:
            print(f"  ⚠️ {slug}: lottolyzer scrape found no data, keeping {len(existing)} existing draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")
        if existing:
            print(f"      (keeping {len(existing)} existing draws)")


def fetch_lotto_6aus49():
    """Lotto 6aus49 — JohannesFriedrich GitHub Archive (替代壞掉的 daowa89)"""
    slug = "lotto-6aus49"
    existing = load_existing(slug)
    try:
        # GitHub Pages JSON archive (updated regularly)
        url = "https://johannesfriedrich.github.io/LottoNumberArchive/Lottonumbers_tidy_complete.json"
        r = requests.get(url, timeout=30, headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        # Data format: list of {"date": "DD.MM.YYYY", "variable": "Lottozahl"|"Superzahl", "value": int}
        # Group by date, collect Lottozahl and Superzahl
        from collections import defaultdict
        by_date = defaultdict(lambda: {"numbers": [], "bonus": []})
        for item in data:
            d = item.get("date", "")
            var = item.get("variable", "")
            val = item.get("value")
            if not d or val is None:
                continue
            # Convert DD.MM.YYYY to YYYY-MM-DD
            if "." in d:
                p = d.split(".")
                if len(p) == 3:
                    d = f"{p[2]}-{p[1]}-{p[0]}"
            if var == "Lottozahl":
                by_date[d]["numbers"].append(int(val))
            elif var == "Superzahl":
                by_date[d]["bonus"] = [int(val)]

        # Only keep last 500 draws (sorted desc)
        new_draws = []
        for dt, info in by_date.items():
            if len(info["numbers"]) == 6:
                new_draws.append({
                    "date": dt,
                    "numbers": sorted(info["numbers"]),
                    "bonus": info["bonus"]
                })
        new_draws.sort(key=lambda x: x["date"], reverse=True)
        new_draws = new_draws[:500]  # Keep manageable size

        if new_draws:
            _save_and_report(slug, new_draws, existing, 49, 9)
        else:
            print(f"  ⚠️ {slug}: archive returned no draws, keeping existing {len(existing)}")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")
        if existing:
            print(f"      (keeping {len(existing)} existing draws)")


def fetch_korea_lotto():
    """Korea Lotto 6/45 — dhlottery.co.kr 官方 JSON API"""
    slug = "korea-lotto"
    existing = load_existing(slug)
    try:
        # Calculate latest round number
        # Round 1 was 2002-12-07, draws every Saturday
        start_date = date(2002, 12, 7)
        today = date.today()
        weeks = (today - start_date).days // 7
        latest_round = weeks + 1

        new_draws = []
        # Fetch last 5 rounds
        for rnd in range(latest_round, max(latest_round - 5, 0), -1):
            try:
                url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={rnd}"
                r = requests.get(url, timeout=10, headers=HEADERS, verify=False)
                if r.status_code != 200:
                    continue
                data = r.json()
                if data.get("returnValue") != "success":
                    continue
                dt = data.get("drwNoDate", "")  # "YYYY-MM-DD"
                if not dt:
                    continue
                numbers = sorted([data[f"drwtNo{i}"] for i in range(1, 7)])
                bonus = [data.get("bnusNo", 0)]
                if all(n > 0 for n in numbers):
                    new_draws.append({"date": dt, "numbers": numbers, "bonus": bonus})
            except Exception:
                continue

        if new_draws:
            _save_and_report(slug, new_draws, existing, 45, 45)
        else:
            print(f"  ⚠️ {slug}: dhlottery API returned no data (might be blocked)")
            if existing:
                print(f"      (keeping {len(existing)} existing draws)")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")


def fetch_japan_loto6():
    """Japan Loto 6 — lottolyzer.com 爬蟲
    HTML 結構（已驗證 2026/07/23）：
      <td>2121</td>                                    ← Draw number
      <td class="sum-p1">2026-07-20</td>               ← Date (YYYY-MM-DD)
      <td class="sum-p1">1,3,10,17,25,26</td>          ← Numbers (comma-separated)
      <td class="sum-p1">36</td>                        ← Bonus
    """
    slug = "japan-loto6"
    existing = load_existing(slug)
    try:
        url = "https://en.lottolyzer.com/history/japan/lotto-6"
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.raise_for_status()
        html = r.text

        new_draws = []
        # Each draw row has: draw_number, date, numbers(comma-sep), bonus
        # Pattern: <td class="sum-p1">YYYY-MM-DD</td> followed by numbers and bonus
        rows = re.findall(
            r'<td class="sum-p1">\s*(\d{4}-\d{2}-\d{2})\s*</td>\s*'
            r'<td class="sum-p1">\s*([\d,]+)\s*</td>\s*'
            r'<td class="sum-p1">\s*(\d+)\s*</td>',
            html
        )
        for dt, nums_str, bonus_str in rows:
            nums = sorted([int(n) for n in nums_str.split(",")])
            bonus = [int(bonus_str.strip())]
            if len(nums) == 6:
                new_draws.append({"date": dt, "numbers": nums, "bonus": bonus})

        if new_draws:
            _save_and_report(slug, new_draws, existing, 43, 43)
        else:
            print(f"  ⚠️ {slug}: lottolyzer scrape found no data, keeping {len(existing)} existing draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")


def fetch_el_gordo():
    """El Gordo de la Primitiva — lottolyzer.com 爬蟲
    HTML 結構（已驗證 2026/07/23，跟 Japan Loto 6 相同格式）：
      <td class="sum-p1">2026-07-20</td>               ← Date
      <td class="sum-p1">6,12,13,23,29,31</td>          ← Numbers (comma-separated)
      <td class="sum-p1">2</td>                          ← Key number (Supp No.)
    Note: lottolyzer 的 Winning No. 包含 5 主號 + reintegro，Supp No. 是 key number
    """
    slug = "el-gordo"
    existing = load_existing(slug)
    try:
        url = "https://en.lottolyzer.com/history/spain/el-gordo-de-la-primitiva"
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.raise_for_status()
        html = r.text

        new_draws = []
        rows = re.findall(
            r'<td class="sum-p1">\s*(\d{4}-\d{2}-\d{2})\s*</td>\s*'
            r'<td class="sum-p1">\s*([\d,]+)\s*</td>\s*'
            r'<td class="sum-p1">\s*(\d+)\s*</td>',
            html
        )
        for dt, nums_str, bonus_str in rows:
            nums = sorted([int(n) for n in nums_str.split(",")])
            bonus = [int(bonus_str.strip())]
            if len(nums) >= 5:
                new_draws.append({"date": dt, "numbers": nums[:5], "bonus": bonus})

        if new_draws:
            _save_and_report(slug, new_draws, existing, 54, 9)
        else:
            print(f"  ⚠️ {slug}: lottolyzer scrape found no data, keeping {len(existing)} existing draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")
        if existing:
            print(f"      (keeping {len(existing)} existing draws)")


def fetch_superenalotto():
    """SuperEnalotto — superenalotto.net 爬蟲
    HTML 結構（已驗證 2026/07/23）：
      <a href="/en/results/21-07-2026" ...>Draw Details</a>    ← Date in href (DD-MM-YYYY)
      <ul class="balls">
        <li>13</li><li>14</li>...<li>63</li>                   ← 6 main numbers
      </ul>
      <ul class="balls">
        <li class="jolly">24</li>                              ← Jolly (bonus)
      </ul>
    """
    slug = "superenalotto"
    existing = load_existing(slug)
    try:
        url = "https://www.superenalotto.net/en/results"
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.raise_for_status()
        html = r.text

        new_draws = []

        # Extract each draw row as a block (drawNumber span → closing </tr>)
        # Then parse date, main numbers, and jolly from each block independently
        draw_blocks = re.findall(
            r'(<tr>\s*<td[^>]*>\s*<span class="drawNumber"[^>]*>\d+/\d+</span>.*?</tr>)',
            html, re.DOTALL
        )
        for block in draw_blocks:
            dt_match = re.search(r'/en/results/(\d{2}-\d{2}-\d{4})', block)
            main_nums = re.findall(r'<li>(\d+)</li>', block)
            jolly = re.findall(r'<li class="jolly">(\d+)</li>', block)
            if dt_match and len(main_nums) >= 6:
                dt_raw = dt_match.group(1)  # DD-MM-YYYY
                p = dt_raw.split("-")
                dt = f"{p[2]}-{p[1]}-{p[0]}"  # → YYYY-MM-DD
                numbers = sorted([int(n) for n in main_nums[:6]])
                bonus = [int(jolly[0])] if jolly else []
                new_draws.append({"date": dt, "numbers": numbers, "bonus": bonus})

        if new_draws:
            _save_and_report(slug, new_draws, existing, 90, 90)
        else:
            print(f"  ⚠️ {slug}: scrape found no data, keeping {len(existing)} existing draws")
    except Exception as e:
        print(f"  ❌ {slug}: {e}")
        if existing:
            print(f"      (keeping {len(existing)} existing draws)")


# ============================================================
# MAIN
# ============================================================
def main():
    print(f"=== Lottery Results Fetch — {datetime.now().strftime('%Y-%m-%d %H:%M UTC')} ===\n")

    # US (working)
    print("[US]")
    fetch_powerball()
    fetch_mega_millions()

    # Taiwan (working)
    print("\n[Taiwan]")
    fetch_taiwan("taiwan-bingo", "5134", 38, 8)
    fetch_taiwan("taiwan-lotto", "5118", 49, 49)
    fetch_taiwan("daily-cash", "1197", 39, 0)

    # Europe (fixed)
    print("\n[Europe]")
    fetch_euromillions()
    fetch_lotto_6aus49()
    fetch_lottolyzer("uk-lotto", "united-kingdom/lotto", 59, 0, expected_nums=6)
    fetch_el_gordo()
    fetch_superenalotto()

    # Americas (working + fixed)
    print("\n[Americas]")
    fetch_mega_sena()
    fetch_lottolyzer("lotto-max", "canada/lotto-max", 50, 0, expected_nums=7)

    # Asia (fixed)
    print("\n[Asia]")
    fetch_lottolyzer("korea-lotto", "south-korea/6_slash_45-lotto", 45, 45, expected_nums=6)
    fetch_japan_loto6()

    # Oceania
    print("\n[Oceania]")
    fetch_lottolyzer("oz-lotto", "australia/oz-lotto", 47, 47, expected_nums=7)

    print(f"\n{'='*50}")
    # Summary
    total = 0
    for slug in ["powerball", "mega-millions", "taiwan-bingo", "taiwan-lotto", "daily-cash",
                  "mega-sena", "euromillions", "lotto-6aus49", "uk-lotto", "el-gordo",
                  "superenalotto", "lotto-max", "korea-lotto", "japan-loto6", "oz-lotto"]:
        existing = load_existing(slug)
        total += len(existing)
    print(f"✅ Fetch complete! Total draws across all lotteries: {total}")


if __name__ == "__main__":
    main()
