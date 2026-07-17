#!/usr/bin/env python3
"""
fix_currency_live_rates.py
把 currency-converter 的靜態匯率改成即時 API（open.er-api.com，完全免費）
處理所有 10 語言版本

Usage:
  cd D:\\xian-shang-you-wei\\backend
  python fix_currency_live_rates.py
"""

import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "tools")

FILES = [
    os.path.join(BASE, "currency-converter.html"),           # zh-TW
    os.path.join(BASE, "en", "currency-converter.html"),
    os.path.join(BASE, "ja", "currency-converter.html"),
    os.path.join(BASE, "ko", "currency-converter.html"),
    os.path.join(BASE, "de", "currency-converter.html"),
    os.path.join(BASE, "fr", "currency-converter.html"),
    os.path.join(BASE, "es", "currency-converter.html"),
    os.path.join(BASE, "pt", "currency-converter.html"),
    os.path.join(BASE, "id", "currency-converter.html"),
    os.path.join(BASE, "zh-CN", "currency-converter.html"),
]

# 各語言的 UI 文字
LABELS = {
    "zh-TW": {"loading": "正在載入即時匯率...", "updated": "匯率更新時間", "error": "無法取得即時匯率，請稍後再試", "source": "資料來源：Open Exchange Rates"},
    "en":    {"loading": "Loading live rates...", "updated": "Rates updated", "error": "Unable to fetch live rates. Please try again later.", "source": "Source: Open Exchange Rates"},
    "ja":    {"loading": "リアルタイム為替レートを読み込み中...", "updated": "レート更新時刻", "error": "リアルタイムレートを取得できませんでした。後でもう一度お試しください。", "source": "データソース：Open Exchange Rates"},
    "ko":    {"loading": "실시간 환율 로딩 중...", "updated": "환율 업데이트", "error": "실시간 환율을 불러올 수 없습니다. 나중에 다시 시도해주세요.", "source": "출처: Open Exchange Rates"},
    "de":    {"loading": "Lade Live-Kurse...", "updated": "Kurse aktualisiert", "error": "Live-Kurse konnten nicht geladen werden. Bitte versuchen Sie es später erneut.", "source": "Quelle: Open Exchange Rates"},
    "fr":    {"loading": "Chargement des taux en direct...", "updated": "Taux mis à jour", "error": "Impossible de charger les taux en direct. Veuillez réessayer plus tard.", "source": "Source : Open Exchange Rates"},
    "es":    {"loading": "Cargando tasas en vivo...", "updated": "Tasas actualizadas", "error": "No se pudieron obtener las tasas en vivo. Inténtelo de nuevo más tarde.", "source": "Fuente: Open Exchange Rates"},
    "pt":    {"loading": "Carregando taxas ao vivo...", "updated": "Taxas atualizadas", "error": "Não foi possível obter taxas ao vivo. Tente novamente mais tarde.", "source": "Fonte: Open Exchange Rates"},
    "id":    {"loading": "Memuat kurs langsung...", "updated": "Kurs diperbarui", "error": "Tidak dapat memuat kurs langsung. Silakan coba lagi nanti.", "source": "Sumber: Open Exchange Rates"},
    "zh-CN": {"loading": "正在加载实时汇率...", "updated": "汇率更新时间", "error": "无法获取实时汇率，请稍后再试", "source": "数据来源：Open Exchange Rates"},
}

def detect_lang(filepath):
    """從路徑判斷語言"""
    parts = filepath.replace("\\", "/").split("/")
    for i, p in enumerate(parts):
        if p == "tools" and i + 1 < len(parts):
            next_part = parts[i + 1]
            if next_part in LABELS and next_part != "currency-converter.html":
                return next_part
    return "zh-TW"

def build_new_js(lang):
    """產生新的 JS，用即時 API 取代靜態匯率"""
    lb = LABELS.get(lang, LABELS["en"])
    
    return f'''var _liveRates = null;
var _ratesLoaded = false;

(function() {{
  var statusEl = document.createElement('div');
  statusEl.id = 'rateStatus';
  statusEl.style.cssText = 'text-align:center;padding:8px 16px;margin:-12px 0 16px;font-size:13px;color:#718096;';
  statusEl.textContent = '{lb["loading"]}';
  var calcCard = document.querySelector('.calc-card');
  if (calcCard) {{
    var btn = calcCard.querySelector('.btn-calc');
    if (btn) calcCard.insertBefore(statusEl, btn);
  }}

  fetch('https://open.er-api.com/v6/latest/USD')
    .then(function(r) {{ return r.json(); }})
    .then(function(data) {{
      if (data && data.result === 'success' && data.rates) {{
        _liveRates = data.rates;
        _ratesLoaded = true;
        var d = new Date(data.time_last_update_utc || Date.now());
        var timeStr = d.toLocaleString();
        statusEl.innerHTML = '<span style="color:#38A169">●</span> {lb["updated"]}: ' + timeStr + '<br><span style="font-size:11px;color:#A0AEC0">{lb["source"]}</span>';
        if (typeof calculate === 'function') calculate();
      }} else {{
        statusEl.innerHTML = '<span style="color:#E53E3E">●</span> {lb["error"]}';
      }}
    }})
    .catch(function() {{
      statusEl.innerHTML = '<span style="color:#E53E3E">●</span> {lb["error"]}';
    }});
}})();

function calculate() {{
  var amountInput = document.getElementById('amountInput');
  var fromCurrencyInput = document.getElementById('fromCurrency');
  var toCurrencyInput = document.getElementById('toCurrency');
  var convertedAmountResult = document.getElementById('convertedAmount');
  var exchangeRateResult = document.getElementById('exchangeRate');
  var resultsDiv = document.querySelector('.results');

  var amount = parseFloat(amountInput.value);
  var fromCurrency = fromCurrencyInput.value;
  var toCurrency = toCurrencyInput.value;

  if (!amount || amount <= 0) {{
    alert('Please enter a valid amount greater than zero');
    return;
  }}
  if (!fromCurrency || !toCurrency) {{
    alert('Please select both currencies');
    return;
  }}
  if (!_ratesLoaded || !_liveRates) {{
    var statusEl = document.getElementById('rateStatus');
    if (statusEl) statusEl.innerHTML = '<span style="color:#E53E3E">●</span> {lb["error"]}';
    return;
  }}

  var fromRate = _liveRates[fromCurrency];
  var toRate = _liveRates[toCurrency];

  if (fromRate === undefined || toRate === undefined) {{
    alert('Currency not supported');
    return;
  }}

  var rateValue = toRate / fromRate;
  var convertedValue = amount * rateValue;

  convertedAmountResult.textContent = convertedValue.toLocaleString('en-US', {{
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }}) + ' ' + toCurrency;

  exchangeRateResult.textContent = '1 ' + fromCurrency + ' = ' + rateValue.toFixed(6) + ' ' + toCurrency;

  resultsDiv.classList.add('show');
}}

document.getElementById('amountInput').addEventListener('keypress', function(e) {{
  if (e.key === 'Enter') calculate();
}});'''


def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lang = detect_lang(filepath)

    # 找到包含 calculate 函式的 <script> 區塊
    # 匹配從 <script> 開始，包含 function calculate，到 </script> 結束
    pattern = r'<script>\s*\n?function calculate\(\)[\s\S]*?</script>'
    match = re.search(pattern, content)
    
    if not match:
        # 嘗試另一種格式（沒有換行）
        pattern = r'<script>\s*function calculate\(\)[\s\S]*?</script>'
        match = re.search(pattern, content)
    
    if not match:
        print(f"  SKIP (no calculate function found): {filepath}")
        return False

    new_js = build_new_js(lang)
    new_block = f"<script>\n{new_js}\n</script>"
    
    content = content[:match.start()] + new_block + content[match.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  OK ({lang}): {filepath}")
    return True


def main():
    print("=" * 60)
    print("Currency Converter → Live API Migration")
    print("API: open.er-api.com (free, no key needed)")
    print("=" * 60)

    ok = 0
    fail = 0
    for filepath in FILES:
        if process_file(filepath):
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} files patched, {fail} skipped/failed")
    print("Deploy via git push to apply changes.")


if __name__ == "__main__":
    main()
