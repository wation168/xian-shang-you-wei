"""
教育百科生字詞彙表 批次抓取腳本（v2：自動嘗試多個學年度）
====================================
用途：一次抓完國小1-6年級 × 南一/康軒/翰林 三版本 × 上/下學期
      的生字/詞彙表，輸出成CSV，供後續轉成SQL匯入資料庫。
      支援國語、數學、自然科學、社會、藝術、健康與體育、
      綜合活動、生活課程等科目（同一個網站都查得到）。

來源：pedia.cloud.edu.tw（教育部教育雲「教育百科」，公開查詢）
      重要：這個系統是「老師會員上傳貢獻」的生字詞彙表，
      不是出版社官方逐字校對的資料，紮根於真實課本沒問題，
      但涵蓋率不一定齊全（可能有些課次還沒有老師上傳），
      每個科目/年級/版本能查到的「最新學年度」也差很多
      （國語普遍到113-114學年度，其他科目有些只到109學年度）。

v2改動：不再要求人工一個個設定學年度，改成自動從最新往舊
        依序嘗試（114_2 -> 114_1 -> 113_2 -> ... -> 109_1），
        抓到第一個有資料的學年度就停下來用那筆，並把「實際
        用了哪個學年度」記錄在輸出CSV的year欄位，方便之後
        核對品質。

執行方式：
    python fetch_word_lists.py --subject 國語 --dry-run   # 先看會抓幾組
    python fetch_word_lists.py --subject 國語             # 正式抓
    python fetch_word_lists.py --subject 社會 --test-one   # 快速測1組

    支援科目：國語、數學、自然科學、社會、藝術、健康與體育、
             綜合活動、生活課程（依教育百科實際選單，逐一測試過)

放置位置：D:\\xian-shang-you-wei\\scripts\\fetch_word_lists.py
（不要放進 backend，這是資料蒐集腳本，跟正式服務程式碼分開）

注意事項：
- 每個組合最多會嘗試12個學年度學期（109上~114下），抓到有資料
  就停，抓不到才會繼續往舊嘗試，所以有資料的組合不會拖慢速度，
  真正查無資料的組合會嘗試完12次才回報失敗，會比較慢屬正常現象。
- 這支腳本只抓「列表頁」顯示的生字預覽（前5個詞+刪節號），
  不會逐課點進「前往」連結抓完整生字清單，避免對網站發送
  過多請求。若確認預覽字數不夠用，之後再另外處理。
- 請求之間有間隔（time.sleep），不要移除，避免對公開服務造成負擔。
- 建議一次只抓一個科目（--subject 指定），抓完核對品質沒問題
  再換下一個科目，不要一次全部科目一起跑，方便抓到異常時
  能定位是哪個科目的問題。
"""

import argparse
import csv
import re
import time
from pathlib import Path

import requests
import urllib3
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# 已知問題處理：pedia.cloud.edu.tw 的憑證鏈缺少 Subject Key
# Identifier，瀏覽器(Chrome)容忍這個結構問題正常顯示網頁，
# 但Python的OpenSSL驗證比較嚴格會直接判定失敗（SSLError）。
# 這不是資料或連線本身有問題，是這個政府網站憑證設定的已知瑕疵。
# 因為這裡只是「讀取」公開查詢頁面（不送出任何帳密/個資），
# 風險可控，所以這裡刻意關閉SSL憑證驗證繼續抓取，
# 並關閉對應的警告訊息，避免洗版。
# ------------------------------------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://pedia.cloud.edu.tw/Bookmark/Textword"

# v3改動：上一版邏輯「不分上下學期，由新到舊試到第一個有資料就停」，
# 導致抓到114下學期就不會再去找114上學期，造成資料庫裡只有下學期。
# 這版改成「上學期、下學期分開各自找最新的一筆」，確保一學年兩學期
# 都會被抓到，不會因為其中一學期先命中就漏掉另一學期。
CANDIDATE_YEARS_XIA = ["114_2", "113_2", "112_2", "111_2", "110_2", "109_2"]  # 下學期候選
CANDIDATE_YEARS_SHANG = ["114_1", "113_1", "112_1", "111_1", "110_1", "109_1"]  # 上學期候選

GRADES = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # 1-6國小，7-9國中（教育百科年級選單確認有到九年級）
PRESSES = ["南一版", "康軒版", "翰林版"]

ALL_SUBJECTS = ["國語", "數學", "自然科學", "社會", "藝術", "健康與體育", "生活課程", "綜合活動"]

OUTPUT_DIR = Path(__file__).parent / "word_list_output"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}


def fetch_one_year(subject: str, year: str, grade: int, press: str, debug: bool = False):
    """抓單一（科目,學年度,年級,版本）組合，回傳list of dict（可能為空）"""
    params = {
        "category": subject,
        "year": year,
        "degree": grade,
        "press": press,
    }
    try:
        resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15, verify=False)
        if debug:
            print(f"    [除錯] 實際請求網址：{resp.url}")
            print(f"    [除錯] HTTP狀態碼：{resp.status_code}")
            print(f"    [除錯] 回應長度：{len(resp.text)} 字元")
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"    [連線錯誤] {year}：{e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.select("table tr")
    if debug:
        print(f"    [除錯] 頁面裡找到 {len(rows)} 個<tr>列")
    results = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        lesson_cell_text = cells[0].get_text(strip=True)
        vocab_cell_text = cells[1].get_text(strip=True)

        # 課名格式有兩種：
        # 1. 國語常見格式：第一課：一束鮮花113學年度|四年級|國語|康軒版
        # 2. 社會/自然/藝術等科目常見格式（沒有「第X課」編號）：
        #    家鄉的地形與氣候114學年度|四年級|社會|南一版
        m = re.match(r"(.+?)(\d+)學年度", lesson_cell_text)
        if not m:
            continue
        full_label = m.group(1).strip()

        # 嘗試拆出「第X課：」這個編號前綴，有就拆開，沒有就整段當課名、
        # 課次編號留空（表示這個科目的課本本身不是用「第幾課」編號）
        m2 = re.match(r"第(.+?)課[：:](.+)", full_label)
        if m2:
            lesson_num_cn, lesson_name = m2.group(1), m2.group(2).strip()
        else:
            lesson_num_cn, lesson_name = "", full_label
        vocab_preview = vocab_cell_text.replace("前往", "").strip()

        results.append({
            "subject": subject,
            "grade": grade,
            "press": press,
            "year": year,
            "lesson_number_cn": lesson_num_cn,
            "lesson_name": lesson_name,
            "vocab_preview": vocab_preview,
        })
    return results


def _search_one_semester(subject, grade, press, candidate_list, debug=False):
    """在一組候選學年度清單裡由新到舊找，抓到第一個有資料的就回傳"""
    for year in candidate_list:
        rows = fetch_one_year(subject, year, grade, press, debug=debug)
        time.sleep(1)  # 禮貌性間隔，不要移除
        if rows:
            return rows, year
        if debug:
            return [], None  # debug模式只測第一個就好，不要浪費時間
    return [], None


def fetch_lesson_list_auto_year(subject: str, grade: int, press: str, debug: bool = False):
    """上學期、下學期分開找，各自找到最新一筆有資料的學年度，合併回傳，
    確保一學年兩學期都會被抓到（不會因為下學期先找到就漏了上學期）"""
    xia_rows, xia_year = _search_one_semester(subject, grade, press, CANDIDATE_YEARS_XIA, debug)
    shang_rows, shang_year = _search_one_semester(subject, grade, press, CANDIDATE_YEARS_SHANG, debug)

    all_rows = xia_rows + shang_rows
    years_used = [y for y in (xia_year, shang_year) if y]
    return all_rows, years_used


def main():
    parser = argparse.ArgumentParser(description="批次抓取教育百科生字/詞彙表（自動嘗試多個學年度）")
    parser.add_argument("--dry-run", action="store_true", help="只顯示會抓哪些組合，不實際發送請求")
    parser.add_argument("--subject", default="國語",
                         help=f"要抓的科目，可用：{'、'.join(ALL_SUBJECTS)}")
    parser.add_argument("--test-one", action="store_true",
                         help="只測試一組（4年級康軒版），快速確認這個科目有沒有真的抓到內容")
    parser.add_argument("--all-subjects", action="store_true",
                         help=f"一次跑完全部科目（{'、'.join(ALL_SUBJECTS)}），"
                              "會依序各自輸出一份CSV，不用一科一科下指令")
    parser.add_argument("--debug", action="store_true",
                         help="除錯模式：印出實際請求網址、HTTP狀態碼、回應內容長度，"
                              "並且每組只試第一個學年度就停（不會浪費時間試完12個），"
                              "用來診斷抓不到資料的組合")
    parser.add_argument("--grade", type=int, default=4,
                         help="搭配 --test-one 使用，指定要測試哪個年級（1-9），預設4年級")
    args = parser.parse_args()

    subjects_to_run = ALL_SUBJECTS if args.all_subjects else [args.subject]

    summary = []  # (subject, 取得筆數, 失敗組合數)
    for subject in subjects_to_run:
        print(f"\n{'='*50}")
        print(f"開始處理科目：{subject}")
        print('='*50)
        got, failed = run_one_subject(subject, args)
        summary.append((subject, got, failed))

    if len(subjects_to_run) > 1 and not args.dry_run:
        print(f"\n\n{'='*50}")
        print("全部科目跑完，總結：")
        print('='*50)
        for subject, got, failed in summary:
            print(f"  {subject}：取得 {got} 筆課次，{failed} 組查無資料")


def run_one_subject(subject: str, args):

    if args.test_one:
        combos = [(args.grade, "康軒版")]
        print(f"[測試模式] 只抓 科目={subject} / {args.grade}年級 / 康軒版")
    else:
        combos = [(grade, press) for grade in GRADES for press in PRESSES]

    print(f"科目：{subject}")
    print(f"共 {len(combos)} 個（年級×版本）組合待抓取，每組會自動嘗試最新到最舊的學年度：")
    for grade, press in combos:
        print(f"  - {grade}年級 / {press}")

    if args.dry_run:
        print("\n[dry-run模式] 以上為預計抓取清單，未實際發送任何請求。")
        return 0, 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_csv = OUTPUT_DIR / f"word_lists_{subject}.csv"
    all_rows = []
    failed_combos = []

    for i, (grade, press) in enumerate(combos, 1):
        print(f"[{i}/{len(combos)}] 抓取 {grade}年級 / {press} ...")
        rows, used_years = fetch_lesson_list_auto_year(subject, grade, press, debug=args.debug)
        if not rows:
            failed_combos.append((grade, press))
            print(f"  -> 上下學期共{len(CANDIDATE_YEARS_XIA)+len(CANDIDATE_YEARS_SHANG)}個學年度都查無資料")
        else:
            all_rows.extend(rows)
            print(f"  -> 取得 {len(rows)} 課（用學年度 {'、'.join(used_years)}）")

    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "subject", "grade", "press", "year",
            "lesson_number_cn", "lesson_name", "vocab_preview"
        ])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n完成！共寫入 {len(all_rows)} 筆課次資料到：{output_csv}")

    if failed_combos:
        print(f"\n⚠️ 以下 {len(failed_combos)} 個組合真的查無資料（12個學年度都試過）：")
        for grade, press in failed_combos:
            print(f"  - {grade}年級 / {press}")

    return len(all_rows), len(failed_combos)


if __name__ == "__main__":
    main()
