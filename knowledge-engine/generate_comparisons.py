#!/usr/bin/env python3
"""
SoftGlow Knowledge Engine — Comparison Page Generator
======================================================
Generates "X vs Y" comparison pages using Haiku API.
Same architecture as generate_content.py.

Usage:
    set ANTHROPIC_API_KEY=sk-ant-api03-...
    python generate_comparisons.py --dry-run
    python generate_comparisons.py
    python generate_comparisons.py --langs en,zh-TW

Output: content/comparisons/{slug}_{lang}.json
"""

import json
import os
import sys
import re
import time
import argparse
from datetime import datetime, timezone

# Reuse from generate_content.py
try:
    import email.utils
    _orig = email.utils.parsedate_to_datetime
    def _p(s):
        try: return _orig(s)
        except: return datetime.now()
    email.utils.parsedate_to_datetime = _p
except: pass

import requests
try:
    from requests.adapters import HTTPAdapter
    _orig_send = HTTPAdapter.send
    def _patched_send(self, req, **kw):
        r = _orig_send(self, req, **kw)
        if r.encoding and r.encoding.lower() == 'iso-8859-1': r.encoding = 'utf-8'
        return r
    HTTPAdapter.send = _patched_send
except: pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "content", "comparisons")
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 4096

ALL_LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
CJK_LANGS = {"zh-TW", "zh-CN", "ja", "ko"}

LANG_NAMES = {
    "zh-TW": "繁體中文", "zh-CN": "简体中文", "en": "English",
    "ja": "日本語", "ko": "한국어", "de": "Deutsch",
    "fr": "Français", "es": "Español", "pt": "Português", "id": "Bahasa Indonesia",
}

# ============================================================
# 30 Comparison Topics
# ============================================================
COMPARISONS = [
    # Technical Indicators
    {"slug": "rsi-vs-macd", "a": "RSI", "b": "MACD", "category": "technical-indicators",
     "tool_a": "rsi-calculator", "tool_b": "macd-calculator"},
    {"slug": "ema-vs-sma", "a": "EMA", "b": "SMA", "category": "technical-indicators",
     "tool_a": "ma-crossover", "tool_b": "ma-crossover"},
    {"slug": "macd-vs-kd", "a": "MACD", "b": "KD (Stochastic)", "category": "technical-indicators",
     "tool_a": "macd-calculator", "tool_b": "rsi-calculator"},
    {"slug": "rsi-vs-stochastic", "a": "RSI", "b": "Stochastic Oscillator", "category": "technical-indicators",
     "tool_a": "rsi-calculator", "tool_b": "rsi-calculator"},
    {"slug": "bollinger-vs-atr", "a": "Bollinger Bands", "b": "ATR", "category": "technical-indicators",
     "tool_a": "bollinger-bands", "tool_b": "atr-calculator"},
    {"slug": "fibonacci-vs-pivot", "a": "Fibonacci Retracement", "b": "Pivot Points", "category": "technical-indicators",
     "tool_a": "fibonacci-retracement", "tool_b": "pivot-point"},
    {"slug": "macd-vs-bollinger", "a": "MACD", "b": "Bollinger Bands", "category": "technical-indicators",
     "tool_a": "macd-calculator", "tool_b": "bollinger-bands"},
    {"slug": "rsi-vs-bollinger", "a": "RSI", "b": "Bollinger Bands", "category": "technical-indicators",
     "tool_a": "rsi-calculator", "tool_b": "bollinger-bands"},

    # Candlestick Patterns
    {"slug": "hammer-vs-doji", "a": "Hammer", "b": "Doji", "category": "candlestick-patterns",
     "tool_a": "candlestick-identifier", "tool_b": "candlestick-identifier"},
    {"slug": "engulfing-vs-harami", "a": "Engulfing", "b": "Harami", "category": "candlestick-patterns",
     "tool_a": "candlestick-identifier", "tool_b": "candlestick-identifier"},
    {"slug": "morning-star-vs-evening-star", "a": "Morning Star", "b": "Evening Star", "category": "candlestick-patterns",
     "tool_a": "candlestick-identifier", "tool_b": "candlestick-identifier"},
    {"slug": "hammer-vs-hanging-man", "a": "Hammer", "b": "Hanging Man", "category": "candlestick-patterns",
     "tool_a": "candlestick-identifier", "tool_b": "candlestick-identifier"},

    # Investment Strategies
    {"slug": "dca-vs-lump-sum", "a": "Dollar Cost Averaging", "b": "Lump Sum Investing", "category": "investment",
     "tool_a": "dca-calculator", "tool_b": "compound-interest"},
    {"slug": "growth-vs-value", "a": "Growth Investing", "b": "Value Investing", "category": "investment",
     "tool_a": "cagr", "tool_b": "intrinsic-value"},
    {"slug": "etf-vs-mutual-fund", "a": "ETF", "b": "Mutual Fund", "category": "investment",
     "tool_a": "roi-calculator", "tool_b": "roi-calculator"},
    {"slug": "stocks-vs-bonds", "a": "Stocks", "b": "Bonds", "category": "investment",
     "tool_a": "roi-calculator", "tool_b": "compound-interest"},

    # Financial Tools
    {"slug": "simple-vs-compound-interest", "a": "Simple Interest", "b": "Compound Interest", "category": "finance",
     "tool_a": "compound-interest", "tool_b": "compound-interest"},
    {"slug": "fixed-vs-variable-rate", "a": "Fixed Rate Mortgage", "b": "Variable Rate Mortgage", "category": "finance",
     "tool_a": "mortgage", "tool_b": "mortgage"},
    {"slug": "roth-vs-traditional-ira", "a": "Roth IRA", "b": "Traditional IRA", "category": "finance",
     "tool_a": "retirement", "tool_b": "retirement"},
    {"slug": "pe-vs-pb-ratio", "a": "P/E Ratio", "b": "P/B Ratio", "category": "finance",
     "tool_a": "pe-ratio", "tool_b": "pe-ratio"},

    # Risk Management
    {"slug": "stop-loss-vs-trailing-stop", "a": "Stop Loss", "b": "Trailing Stop", "category": "risk",
     "tool_a": "stop-loss", "tool_b": "stop-loss"},
    {"slug": "sharpe-vs-sortino", "a": "Sharpe Ratio", "b": "Sortino Ratio", "category": "risk",
     "tool_a": "sharpe-ratio", "tool_b": "sharpe-ratio"},
    {"slug": "market-vs-limit-order", "a": "Market Order", "b": "Limit Order", "category": "trading",
     "tool_a": "trading-fee", "tool_b": "trading-fee"},

    # Real Estate
    {"slug": "renting-vs-buying", "a": "Renting", "b": "Buying a Home", "category": "real-estate",
     "tool_a": "mortgage", "tool_b": "mortgage"},
    {"slug": "15yr-vs-30yr-mortgage", "a": "15-Year Mortgage", "b": "30-Year Mortgage", "category": "real-estate",
     "tool_a": "mortgage", "tool_b": "mortgage"},

    # Crypto / Modern
    {"slug": "technical-vs-fundamental", "a": "Technical Analysis", "b": "Fundamental Analysis", "category": "analysis",
     "tool_a": "rsi-calculator", "tool_b": "dcf-calculator"},
    {"slug": "day-trading-vs-swing", "a": "Day Trading", "b": "Swing Trading", "category": "trading",
     "tool_a": "position-size", "tool_b": "position-size"},
    {"slug": "active-vs-passive", "a": "Active Investing", "b": "Passive Investing", "category": "investment",
     "tool_a": "roi-calculator", "tool_b": "dca-calculator"},
    {"slug": "options-vs-futures", "a": "Options", "b": "Futures", "category": "derivatives",
     "tool_a": "options-profit", "tool_b": "margin-calculator"},
    {"slug": "cagr-vs-roi", "a": "CAGR", "b": "ROI", "category": "finance",
     "tool_a": "cagr", "tool_b": "roi-calculator"},
    {"slug": "dcf-vs-ddm", "a": "DCF Valuation", "b": "Dividend Discount Model", "category": "valuation",
     "tool_a": "dcf-calculator", "tool_b": "intrinsic-value"},
]


def repair_json(raw):
    raw = raw.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```\s*$', '', raw)
    raw = raw.strip()
    try: return json.loads(raw)
    except: pass
    first, last = raw.find('{'), raw.rfind('}')
    if first == -1: return None
    if last > first:
        try: return json.loads(raw[first:last+1])
        except: pass
    candidate = raw[first:]
    in_str = escaped = False
    for ch in candidate:
        if escaped: escaped = False; continue
        if ch == '\\': escaped = True; continue
        if ch == '"': in_str = not in_str
    if in_str: candidate += '"'
    opens = open_sq = 0
    in_str = escaped = False
    for ch in candidate:
        if escaped: escaped = False; continue
        if ch == '\\': escaped = True; continue
        if ch == '"': in_str = not in_str; continue
        if in_str: continue
        if ch == '{': opens += 1
        elif ch == '}': opens -= 1
        elif ch == '[': open_sq += 1
        elif ch == ']': open_sq -= 1
    candidate += ']' * open_sq + '}' * opens
    try: return json.loads(candidate)
    except: return None


def call_api(prompt, api_key, retries=3):
    headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    payload = {"model": MODEL, "max_tokens": MAX_TOKENS, "messages": [{"role": "user", "content": prompt}]}
    for attempt in range(retries):
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            if resp.status_code == 429:
                time.sleep(min(60, 10 * (attempt + 1))); continue
            if resp.status_code >= 500:
                time.sleep(15 * (attempt + 1)); continue
            if resp.status_code != 200:
                return None, f"HTTP {resp.status_code}"
            data = resp.json()
            text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
            return text, None
        except requests.exceptions.Timeout:
            time.sleep(15 * (attempt + 1)); continue
        except Exception as e:
            return None, str(e)
    return None, "Max retries"


def build_prompt(comp, lang):
    ln = LANG_NAMES.get(lang, lang)
    return f"""You are a professional financial content writer. Write a comparison article: "{comp['a']} vs {comp['b']}" in {ln}.

OUTPUT: Return ONLY a valid JSON object with this structure:
{{
  "seo": {{
    "title": "SEO title: {comp['a']} vs {comp['b']} comparison, 50-60 chars, in {ln}",
    "description": "Meta description, 140-160 chars, in {ln}",
    "h1": "{comp['a']} vs {comp['b']} — page heading in {ln}"
  }},
  "intro": {{
    "html": "2-3 paragraphs introducing both concepts and why traders compare them. HTML <p> tags. In {ln}"
  }},
  "comparison_table": {{
    "headers": ["Feature/Aspect header in {ln}", "{comp['a']}", "{comp['b']}"],
    "rows": [
      ["aspect 1", "description for A", "description for B"],
      ["aspect 2", "...", "..."],
      ... (6-8 rows covering: definition, calculation, signal type, best market, timeframe, strengths, weaknesses, difficulty)
    ]
  }},
  "when_to_use": {{
    "a": "2-3 sentences on when {comp['a']} is the better choice, in {ln}",
    "b": "2-3 sentences on when {comp['b']} is the better choice, in {ln}"
  }},
  "combined_strategy": {{
    "html": "2-3 paragraphs explaining how to use both together for better results. HTML <p> tags. In {ln}"
  }},
  "faq": [
    {{"q": "question 1 in {ln}", "a": "answer 1 in {ln}"}},
    {{"q": "question 2", "a": "answer 2"}},
    {{"q": "question 3", "a": "answer 3"}},
    {{"q": "question 4", "a": "answer 4"}},
    {{"q": "question 5", "a": "answer 5"}}
  ],
  "verdict": {{
    "html": "1-2 paragraphs with final recommendation — which to start with, when each shines. In {ln}"
  }}
}}

RULES:
1. ALL content in {ln}. Do not mix languages.
2. Comparison must be fair and balanced — no clear winner, each has strengths.
3. Use <p> and <strong> tags only in HTML fields. No <h1>-<h6>, no <div>.
4. FAQ: exactly 5 items.
5. comparison_table rows: 6-8 aspects.
6. Total content: 800-1500 words.
7. Return ONLY the JSON, nothing else."""


def content_path(slug, lang):
    return os.path.join(OUTPUT_DIR, f"{slug}_{lang}.json")


def main():
    parser = argparse.ArgumentParser(description="Generate comparison page content via Haiku API")
    parser.add_argument("--slug", help="Generate one comparison only")
    parser.add_argument("--langs", help="Comma-separated langs (default: all 10)")
    parser.add_argument("--force", action="store_true", help="Overwrite cache")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()

    comps = COMPARISONS
    if args.slug:
        comps = [c for c in COMPARISONS if c["slug"] == args.slug]
        if not comps:
            print(f"❌ Slug '{args.slug}' not found"); sys.exit(1)

    langs = ALL_LANGS
    if args.langs:
        langs = [l.strip() for l in args.langs.split(",")]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(comps) * len(langs)
    cached = sum(1 for c in comps for l in langs if not args.force and os.path.exists(content_path(c["slug"], l)))
    to_gen = total - cached

    print(f"\nSoftGlow — Comparison Page Generator")
    print(f"{'='*50}")
    print(f"Comparisons: {len(comps)} | Languages: {len(langs)} | Total: {total}")
    print(f"Cached: {cached} | To generate: {to_gen}")
    print(f"Est. cost: ${to_gen * 0.01:.2f} - ${to_gen * 0.02:.2f}")
    print(f"{'='*50}")

    if args.dry_run:
        for c in comps:
            for l in langs:
                st = "SKIP" if os.path.exists(content_path(c["slug"], l)) else "GENERATE"
                print(f"  {c['slug']}_{l} → {st}")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key or len(api_key) < 20:
        print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)

    generated = errors = skipped = 0
    for c in comps:
        for l in langs:
            p = content_path(c["slug"], l)
            if not args.force and os.path.exists(p):
                skipped += 1; continue

            print(f"  [{generated+skipped+errors+1}/{total}] 🔄 {c['slug']}_{l}...", end="", flush=True)
            raw, err = call_api(build_prompt(c, l), api_key)
            if err:
                print(f" ❌ {err}"); errors += 1; time.sleep(args.delay); continue

            data = repair_json(raw)
            if not data:
                print(f" ❌ JSON parse failed"); errors += 1; time.sleep(args.delay); continue

            data["_meta"] = {"slug": c["slug"], "lang": l, "a": c["a"], "b": c["b"],
                             "tool_a": c["tool_a"], "tool_b": c["tool_b"],
                             "category": c["category"], "model": MODEL,
                             "build_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f" ✅"); generated += 1
            time.sleep(args.delay)

    print(f"\n{'='*50}")
    print(f"Generated: {generated} | Cached: {skipped} | Errors: {errors}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
