"""
批次下載國中教育會考歷屆試題（111-115年）
====================================
來源：cap.rcpet.edu.tw 官方網站，連結清單已用瀏覽器實際核對過
      （111-115年，共5年 × 8個檔案：參考答案/寫作測驗/國文科/
      英語閱讀/英語聽力/數學科/社會科/自然科 = 40個PDF）

用途：先把PDF全部下載到本機，之後才能進行拆題/OCR等後續處理。
      這一步只負責下載，不做內容解析。

執行方式：
    python download_cap_exams.py
    （會在同資料夾下建立 cap_exam_pdfs/ 存放下載結果）

放置位置：D:\\xian-shang-you-wei\\學測評量\\scripts\\download_cap_exams.py
"""

import csv
import time
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "exam_links.csv"
OUTPUT_DIR = SCRIPT_DIR / "cap_exam_pdfs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}


def download_one(file_id: str, dest_path: Path) -> bool:
    """用 Google Drive 直接下載連結抓取PDF"""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        # Google Drive對大檔案有時會先回傳一個「確認下載」的HTML頁面，
        # 不是真正的PDF內容，這裡簡單判斷一下開頭是不是PDF格式
        if resp.content[:4] != b"%PDF":
            print(f"    ⚠️ 疑似不是直接PDF內容（可能是Drive確認頁面），檔案仍會存檔，需人工確認")
        dest_path.write_bytes(resp.content)
        return True
    except requests.RequestException as e:
        print(f"    [失敗] {e}")
        return False


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"共 {len(rows)} 個檔案待下載\n")

    success_count = 0
    fail_list = []

    for i, row in enumerate(rows, 1):
        year, subject, file_id = row["year"], row["subject"], row["file_id"]
        safe_subject = subject.replace("（", "_").replace("）", "")
        filename = f"{year}_{safe_subject}.pdf"
        dest_path = OUTPUT_DIR / filename

        print(f"[{i}/{len(rows)}] 下載 {year}年 {subject} -> {filename}")
        ok = download_one(file_id, dest_path)
        if ok:
            success_count += 1
        else:
            fail_list.append(f"{year} {subject}")
        time.sleep(1.5)  # 禮貌性間隔

    print(f"\n完成！成功 {success_count}/{len(rows)}")
    if fail_list:
        print("以下下載失敗，需要人工重試：")
        for f in fail_list:
            print(f"  - {f}")

    print(f"\n⚠️ 重要提醒：Google Drive對「所有人都能瀏覽」的連結通常可以直接下載，"
          f"但少數大檔案可能會被要求「確認病毒掃描略過」，如果打開下載的PDF發現"
          f"內容是HTML網頁而不是真正的考卷，代表那幾份需要你自己手動點開瀏覽器"
          f"下載一次。")


if __name__ == "__main__":
    main()
