#!/usr/bin/env python3
"""
SoftGlow Knowledge Engine — Content JSON Generator
====================================================
Calls Claude Haiku API to generate multilingual content JSON for candlestick patterns.

Reads:  pattern-catalog.json + locale-config.json
Writes: content/{slug}_{lang}.json

Usage:
    set ANTHROPIC_API_KEY=sk-ant-api03-...

    python generate_content.py                                    # all 50 × 10 = 500
    python generate_content.py --slug bullish-engulfing           # 1 pattern × 10 langs
    python generate_content.py --langs en,ja                      # 50 patterns × 2 langs
    python generate_content.py --slug hammer --langs zh-TW,en     # 1 × 2
    python generate_content.py --dry-run                          # show plan, no API calls
    python generate_content.py --force                            # overwrite existing cache

Features:
    - Cache: skips if content/{slug}_{lang}.json already exists (resume after interruption)
    - JSON repair: fixes truncated API responses
    - Retry: 429/5xx auto-retry with exponential backoff
    - Quality check: validates required fields, FAQ count, word count
    - Progress: real-time counter and cost estimate
    - Windows-safe: monkey-patches requests for latin-1 encoding issue
"""

import json
import os
import sys
import re
import time
import argparse
import traceback
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Fix Windows + Python 3.14 encoding issue
# ---------------------------------------------------------------------------
try:
    import email.utils
    _orig_parsedate_to_datetime = email.utils.parsedate_to_datetime
    def _patched_parsedate(s):
        try:
            return _orig_parsedate_to_datetime(s)
        except Exception:
            from datetime import datetime as _dt
            return _dt.now()
    email.utils.parsedate_to_datetime = _patched_parsedate
except Exception:
    pass

import requests

# Monkey-patch requests to avoid latin-1 encoding errors on Windows
_orig_build_response = None
try:
    from requests.adapters import HTTPAdapter
    _orig_send = HTTPAdapter.send
    def _patched_send(self, request, **kwargs):
        resp = _orig_send(self, request, **kwargs)
        if resp.encoding and resp.encoding.lower() == 'iso-8859-1':
            resp.encoding = 'utf-8'
        return resp
    HTTPAdapter.send = _patched_send
except Exception:
    pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(BASE_DIR, "pattern-catalog.json")
LOCALE_PATH = os.path.join(BASE_DIR, "locale-config.json")
CONTENT_DIR = os.path.join(BASE_DIR, "content")

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 8192
GENERATOR_VERSION = "1.0"

ALL_LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]

# CJK languages use character count, Latin use word count
CJK_LANGS = {"zh-TW", "zh-CN", "ja", "ko"}
MIN_WORDS_LATIN = 600
MAX_WORDS_LATIN = 1800
MIN_CHARS_CJK = 500
MAX_CHARS_CJK = 2500

# Approximate cost per call (Haiku input ~$0.80/MTok, output ~$4/MTok)
# ~2000 input tokens + ~2000 output tokens per call
EST_COST_PER_CALL = 0.01  # ~$0.01 USD

# Category names for prompt context
CATEGORY_NAMES = {
    "bullish-reversal": "Bullish Reversal",
    "bearish-reversal": "Bearish Reversal",
    "bullish-continuation": "Bullish Continuation",
    "bearish-continuation": "Bearish Continuation",
    "neutral": "Neutral / Indecision",
}

# Language display names for prompt
LANG_NAMES = {
    "zh-TW": "繁體中文 (Traditional Chinese)",
    "zh-CN": "简体中文 (Simplified Chinese)",
    "en": "English",
    "ja": "日本語 (Japanese)",
    "ko": "한국어 (Korean)",
    "de": "Deutsch (German)",
    "fr": "Français (French)",
    "es": "Español (Spanish)",
    "pt": "Português (Portuguese)",
    "id": "Bahasa Indonesia (Indonesian)",
}

# Trading rule key → human-readable description for prompt context
TRADING_RULE_DESCRIPTIONS = {
    "close_above_engulfing_high": "Enter when price closes above the engulfing candle's high",
    "close_above_hammer_high": "Enter when price closes above the hammer's high",
    "close_above_third_candle_midpoint": "Enter when price closes above the third candle's midpoint",
    "close_above_pattern_high": "Enter when price closes above the pattern's high",
    "close_above_third_candle_high": "Enter when price closes above the third candle's high",
    "close_above_second_candle_high": "Enter when price closes above the second candle's high",
    "close_above_doji_high": "Enter when price closes above the doji's high",
    "close_above_first_candle_high": "Enter when price closes above the first candle's high",
    "close_below_engulfing_low": "Enter short when price closes below the engulfing candle's low",
    "close_below_pattern_low": "Enter short when price closes below the pattern's low",
    "close_below_star_low": "Enter short when price closes below the star candle's low",
    "close_below_third_candle_low": "Enter short when price closes below the third candle's low",
    "close_below_second_candle_low": "Enter short when price closes below the second candle's low",
    "close_below_doji_low": "Enter short when price closes below the doji's low",
    "close_below_hanging_man_low": "Enter short when price closes below the hanging man's low",
    "close_below_first_candle_low": "Enter short when price closes below the first candle's low",
    "below_engulfing_low": "Place stop loss below the engulfing pattern's low",
    "below_hammer_low": "Place stop loss below the hammer's low",
    "below_second_candle_low": "Place stop loss below the second (star) candle's low",
    "below_pattern_low": "Place stop loss below the pattern's low",
    "below_first_candle_low": "Place stop loss below the first candle's low",
    "below_doji_low": "Place stop loss below the doji's low",
    "above_engulfing_high": "Place stop loss above the engulfing pattern's high",
    "above_pattern_high": "Place stop loss above the pattern's high",
    "above_star_high": "Place stop loss above the star candle's high",
    "above_first_candle_high": "Place stop loss above the first candle's high",
    "above_doji_high": "Place stop loss above the doji's high",
    "above_hanging_man_high": "Place stop loss above the hanging man's high",
    "nearest_resistance_or_2r": "Target the nearest resistance level or a 2:1 reward-to-risk ratio",
    "nearest_support_or_2r": "Target the nearest support level or a 2:1 reward-to-risk ratio",
    "close_below_first_candle_low": "Pattern invalidated if price closes below the first candle's low",
    "close_above_first_candle_high": "Pattern invalidated if price closes above the first candle's high",
    "close_below_second_candle_midpoint": "Pattern invalidated if price closes below the second candle's midpoint",
    "close_above_second_candle_midpoint": "Pattern invalidated if price closes above the second candle's midpoint",
    "bearish_engulfing_after": "Pattern invalidated if a bearish engulfing pattern forms immediately after",
    "bullish_engulfing_after": "Pattern invalidated if a bullish engulfing pattern forms immediately after",
    "close_below_second_candle_low": "Pattern invalidated if price closes below the second candle's low",
    "close_above_second_candle_high": "Pattern invalidated if price closes above the second candle's high",
    "close_above_doji_high": "Pattern invalidated if price closes above the doji's high",
    "close_below_doji_low": "Pattern invalidated if price closes below the doji's low",
    "close_below_breakaway_low": "Pattern invalidated if price closes below the breakaway's low",
    "close_above_breakaway_high": "Pattern invalidated if price closes above the breakaway's high",
    "continuation_fails_reversal": "Pattern invalidated if price reverses instead of continuing the trend",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def content_path(slug, lang):
    return os.path.join(CONTENT_DIR, f"{slug}_{lang}.json")


def repair_json(raw):
    """Attempt to extract valid JSON from potentially truncated API response."""
    raw = raw.strip()
    # Remove markdown code fences
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```\s*$', '', raw)
    raw = raw.strip()

    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Find outermost { }
    first = raw.find('{')
    last = raw.rfind('}')
    if first == -1:
        return None
    
    if last > first:
        candidate = raw[first:last+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Truncated: try to close open braces/brackets
    candidate = raw[first:]
    # Close any unclosed strings
    in_str = False
    escaped = False
    for ch in candidate:
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == '"':
            in_str = not in_str
    if in_str:
        candidate += '"'

    # Count open braces/brackets
    opens = 0
    open_sq = 0
    in_str = False
    escaped = False
    for ch in candidate:
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == '{': opens += 1
        elif ch == '}': opens -= 1
        elif ch == '[': open_sq += 1
        elif ch == ']': open_sq -= 1

    candidate += ']' * open_sq + '}' * opens

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def count_content_words(data):
    """Count total content words/chars across all text fields."""
    texts = []
    texts.append(data.get("summary", {}).get("text", ""))
    texts.append(data.get("structure", {}).get("html", ""))
    texts.append(data.get("psychology", {}).get("html", ""))
    for rule_key in ["entry", "stop_loss", "take_profit", "invalidation"]:
        texts.append(data.get("trading_rules", {}).get(rule_key, ""))
    texts.append(data.get("confirmation", {}).get("html", ""))
    for item in data.get("mistakes", {}).get("items", []):
        texts.append(item.get("text", ""))
    for item in data.get("checklist", {}).get("items", []):
        texts.append(item)
    for faq in data.get("faq", []):
        texts.append(faq.get("a", ""))

    combined = " ".join(texts)
    # Strip HTML tags for counting
    clean = re.sub(r'<[^>]+>', '', combined)
    return clean


def validate_content(data, lang):
    """Validate content JSON has all required fields and meets quality standards."""
    issues = []

    required_top = ["seo", "hero", "summary", "structure", "psychology",
                     "trading_rules", "confirmation", "mistakes", "checklist", "faq"]
    for key in required_top:
        if key not in data:
            issues.append(f"missing top-level key: {key}")

    if not issues:
        # SEO
        seo = data.get("seo", {})
        for k in ["title", "description", "h1"]:
            if not seo.get(k):
                issues.append(f"seo.{k} empty")

        # Hero
        if not data.get("hero", {}).get("one_liner"):
            issues.append("hero.one_liner empty")

        # Summary
        if not data.get("summary", {}).get("text"):
            issues.append("summary.text empty")

        # Structure + Psychology + Confirmation (HTML)
        for section in ["structure", "psychology", "confirmation"]:
            if not data.get(section, {}).get("html"):
                issues.append(f"{section}.html empty")

        # Trading rules
        tr = data.get("trading_rules", {})
        for k in ["entry", "stop_loss", "take_profit", "invalidation"]:
            if not tr.get(k):
                issues.append(f"trading_rules.{k} empty")

        # Mistakes
        mistakes = data.get("mistakes", {}).get("items", [])
        if len(mistakes) < 3:
            issues.append(f"mistakes.items only {len(mistakes)}, need ≥3")

        # Checklist
        checklist = data.get("checklist", {}).get("items", [])
        if len(checklist) < 5:
            issues.append(f"checklist.items only {len(checklist)}, need ≥5")

        # FAQ
        faq = data.get("faq", [])
        if len(faq) < 5:
            issues.append(f"faq only {len(faq)} items, need 5")

        # Word count
        clean_text = count_content_words(data)
        if lang in CJK_LANGS:
            char_count = len(clean_text.replace(" ", ""))
            if char_count < MIN_CHARS_CJK:
                issues.append(f"content too short: {char_count} chars (min {MIN_CHARS_CJK})")
        else:
            word_count = len(clean_text.split())
            if word_count < MIN_WORDS_LATIN:
                issues.append(f"content too short: {word_count} words (min {MIN_WORDS_LATIN})")

    return issues


def describe_trading_rule(key):
    """Convert trading rule key to human-readable description."""
    return TRADING_RULE_DESCRIPTIONS.get(key, key.replace("_", " "))


# ---------------------------------------------------------------------------
# API Call
# ---------------------------------------------------------------------------
def call_api(prompt, api_key, retries=3):
    """Call Claude Haiku API with retry logic."""
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
    }

    for attempt in range(retries):
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)

            if resp.status_code == 429:
                wait = min(60, 10 * (attempt + 1))
                print(f"    ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue

            if resp.status_code >= 500:
                wait = 15 * (attempt + 1)
                print(f"    ⏳ Server error {resp.status_code}, retrying in {wait}s...")
                time.sleep(wait)
                continue

            if resp.status_code != 200:
                return None, f"HTTP {resp.status_code}: {resp.text[:200]}"

            data = __import__("json").loads(resp.content.decode("utf-8"))
            text = ""
            for block in data.get("content", []):
                if block.get("type") == "text":
                    text += block.get("text", "")

            if not text:
                return None, "Empty response from API"

            return text, None

        except requests.exceptions.Timeout:
            wait = 15 * (attempt + 1)
            print(f"    ⏳ Timeout, retrying in {wait}s...")
            time.sleep(wait)
            continue
        except Exception as e:
            return None, str(e)

    return None, "Max retries exceeded"


# ---------------------------------------------------------------------------
# Prompt Builder
# ---------------------------------------------------------------------------
def build_prompt(slug, lang, catalog_entry, locale_cfg):
    """Build the API prompt for generating content JSON."""
    pattern_name = slug.replace("-", " ").title()
    signal = catalog_entry["signal"]
    reliability = catalog_entry["reliability"]
    difficulty = catalog_entry["difficulty"]
    candles = catalog_entry["candles"]
    category = catalog_entry["category"]
    category_name = CATEGORY_NAMES.get(category, category)
    best_market = ", ".join(catalog_entry["best_market"])
    lang_name = LANG_NAMES.get(lang, lang)
    ui = locale_cfg.get("ui", {})

    # Trading rules context
    tr = catalog_entry["trading_rules"]
    entry_desc = describe_trading_rule(tr["entry"])
    sl_desc = describe_trading_rule(tr["stop_loss"])
    tp_desc = describe_trading_rule(tr["take_profit"])
    inv_desc = describe_trading_rule(tr["invalidation"])

    # Related patterns for cross-reference context
    related = ", ".join(catalog_entry.get("related_patterns", [])[:3])

    prompt = f"""You are a professional financial content writer. Write content for the "{pattern_name}" candlestick pattern page in {lang_name}.

PATTERN DATA (fixed, do not contradict):
- Signal: {signal}
- Candles: {candles}
- Reliability: {reliability} (use ONLY high/medium/low — NEVER generate success rate percentages)
- Difficulty: {difficulty}
- Category: {category_name}
- Best Market: {best_market}
- Entry Rule: {entry_desc}
- Stop Loss: {sl_desc}
- Take Profit: {tp_desc}
- Invalidation: {inv_desc}
- Related Patterns: {related}

OUTPUT FORMAT: Return ONLY a valid JSON object (no markdown, no explanation, no preamble). The JSON must have this exact structure:

{{
  "seo": {{
    "title": "SEO page title with pattern name, 50-60 chars, in {lang_name}",
    "description": "Meta description, 140-160 chars, in {lang_name}",
    "h1": "Page heading — the pattern name in {lang_name}"
  }},
  "hero": {{
    "one_liner": "One sentence describing what this pattern means and when it appears, in {lang_name}"
  }},
  "summary": {{
    "text": "2-3 sentence summary a beginner can understand in 30 seconds, in {lang_name}"
  }},
  "structure": {{
    "html": "HTML paragraphs explaining the pattern's visual structure and identification criteria. Use <p>, <strong> tags. 2-4 paragraphs, in {lang_name}"
  }},
  "psychology": {{
    "html": "HTML paragraphs explaining the market psychology behind this pattern — what buyers/sellers are doing and why. 2-3 paragraphs, in {lang_name}"
  }},
  "trading_rules": {{
    "entry": "Plain-language explanation of when to enter, in {lang_name}",
    "stop_loss": "Plain-language explanation of where to set stop loss, in {lang_name}",
    "take_profit": "Plain-language explanation of take profit target, in {lang_name}",
    "invalidation": "Plain-language explanation of when the pattern is invalidated, in {lang_name}"
  }},
  "confirmation": {{
    "html": "HTML paragraphs explaining which indicators (RSI, MACD, volume, support/resistance) confirm this pattern. Mention 3-4 indicators. 2-3 paragraphs, in {lang_name}"
  }},
  "mistakes": {{
    "items": [
      {{"title": "Mistake name", "text": "2-3 sentence explanation"}},
      ... (3-5 common mistakes)
    ]
  }},
  "checklist": {{
    "items": [
      "Checklist item 1 (actionable, starts with verb or condition)",
      ... (5-7 items)
    ]
  }},
  "faq": [
    {{"q": "Pattern-specific question 1", "a": "Detailed answer, 2-4 sentences"}},
    {{"q": "Pattern-specific question 2", "a": "..."}},
    {{"q": "Pattern-specific question 3", "a": "..."}},
    {{"q": "General candlestick pattern question (category-level)", "a": "..."}},
    {{"q": "General candlestick pattern question (category-level)", "a": "..."}}
  ]
}}

RULES:
1. ALL text content must be in {lang_name} — do not mix languages.
2. NEVER generate success rate percentages. Use only high/medium/low for reliability.
3. HTML sections use <p> and <strong> tags only. No <h1>-<h6>, no <div>, no class attributes.
4. FAQ: exactly 5 items — first 3 are specific to {pattern_name}, last 2 are about candlestick patterns in general.
5. Mistakes: 3-5 items, each with title and text.
6. Checklist: 5-7 actionable items.
7. Total content: 800-1500 words (or 500-2500 characters for CJK languages).
8. Write for an intermediate trader audience — not too basic, not too academic.
9. Do NOT include _meta field — that is added by the generator.
10. Return ONLY the JSON object, nothing else."""

    return prompt


# ---------------------------------------------------------------------------
# Generate one content file
# ---------------------------------------------------------------------------
def generate_one(slug, lang, catalog_entry, locale_cfg, api_key, force=False):
    """Generate content JSON for one pattern+language. Returns (success, error_msg)."""
    out_path = content_path(slug, lang)

    # Check cache
    if not force and os.path.exists(out_path):
        try:
            existing = load_json(out_path)
            issues = validate_content(existing, lang)
            if not issues:
                return True, "cached"
            else:
                print(f"    ♻️  Re-generating (validation failed: {issues[0]})")
        except Exception:
            pass  # corrupt file, regenerate

    # Build prompt
    prompt = build_prompt(slug, lang, catalog_entry, locale_cfg)

    # Call API
    raw_text, err = call_api(prompt, api_key)
    if err:
        return False, err

    # Parse JSON
    data = repair_json(raw_text)
    if data is None:
        # Save raw for debugging
        debug_path = out_path.replace(".json", "_raw.txt")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(raw_text)
        return False, f"JSON parse failed (raw saved to {debug_path})"

    # Add _meta
    data["_meta"] = {
        "slug": slug,
        "lang": lang,
        "generator_version": GENERATOR_VERSION,
        "model": MODEL,
        "build_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # Validate
    issues = validate_content(data, lang)
    if issues:
        # Save anyway but warn
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return False, f"validation: {'; '.join(issues[:3])}"

    # Save
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return True, "ok"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate Content JSON via Haiku API")
    parser.add_argument("--slug", help="Generate for one pattern only")
    parser.add_argument("--langs", help="Comma-separated language codes (default: all 10)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing cache")
    parser.add_argument("--dry-run", action="store_true", help="Show plan, no API calls")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between API calls (default: 1.0)")
    args = parser.parse_args()

    # Load config
    catalog = load_json(CATALOG_PATH)
    locale_configs = load_json(LOCALE_PATH)

    # Filter patterns
    entries = {k: v for k, v in catalog.items() if not k.startswith("_")}
    if args.slug:
        if args.slug not in entries:
            print(f"❌ Pattern '{args.slug}' not found in catalog")
            sys.exit(1)
        entries = {args.slug: entries[args.slug]}

    # Filter languages
    langs = ALL_LANGS
    if args.langs:
        langs = [l.strip() for l in args.langs.split(",")]
        for l in langs:
            if l not in locale_configs:
                print(f"❌ Language '{l}' not found in locale-config.json")
                sys.exit(1)

    # Ensure content dir
    os.makedirs(CONTENT_DIR, exist_ok=True)

    # Count what needs to be done
    total = len(entries) * len(langs)
    cached = 0
    to_generate = 0
    for slug in entries:
        for lang in langs:
            p = content_path(slug, lang)
            if not args.force and os.path.exists(p):
                try:
                    d = load_json(p)
                    if not validate_content(d, lang):
                        cached += 1
                        continue
                except Exception:
                    pass
            to_generate += 1

    est_cost = to_generate * EST_COST_PER_CALL
    est_time_min = to_generate * (args.delay + 2) / 60  # ~2s per API call + delay

    print()
    print(f"SoftGlow Knowledge Engine — Content Generator v{GENERATOR_VERSION}")
    print(f"{'='*60}")
    print(f"Model: {MODEL}")
    print(f"Patterns: {len(entries)} | Languages: {len(langs)} | Total: {total}")
    print(f"Cached (skip): {cached} | To generate: {to_generate}")
    print(f"Estimated cost: ${est_cost:.2f} - ${est_cost*2:.2f} USD (with safety margin)")
    print(f"Estimated time: {est_time_min:.0f} - {est_time_min*1.5:.0f} minutes")
    print(f"Output: {CONTENT_DIR}")
    print(f"{'='*60}")

    if args.dry_run:
        print("\n🏁 Dry run — listing what would be generated:\n")
        for slug in sorted(entries.keys()):
            for lang in langs:
                p = content_path(slug, lang)
                exists = os.path.exists(p)
                status = "SKIP (cached)" if exists and not args.force else "GENERATE"
                print(f"  {slug}_{lang}.json → {status}")
        print(f"\nTotal API calls needed: {to_generate}")
        return

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key or "你的" in api_key or len(api_key) < 20:
        print("\n❌ ANTHROPIC_API_KEY not set or invalid!")
        print("Run: set ANTHROPIC_API_KEY=sk-ant-api03-...")
        sys.exit(1)

    print()
    generated = 0
    errors = 0
    skipped = 0
    error_list = []
    start_time = time.time()

    for slug_idx, slug in enumerate(sorted(entries.keys()), 1):
        entry = entries[slug]
        for lang_idx, lang in enumerate(langs, 1):
            progress = f"[{generated + skipped + errors + 1}/{total}]"

            # Check cache
            p = content_path(slug, lang)
            if not args.force and os.path.exists(p):
                try:
                    d = load_json(p)
                    if not validate_content(d, lang):
                        print(f"  {progress} ✅ {slug}_{lang} (cached)")
                        skipped += 1
                        continue
                except Exception:
                    pass

            locale_cfg = locale_configs.get(lang, {})
            print(f"  {progress} 🔄 {slug}_{lang}...", end="", flush=True)

            success, msg = generate_one(slug, lang, entry, locale_cfg, api_key, force=args.force)

            if msg == "cached":
                print(f" ✅ (cached)")
                skipped += 1
            elif success:
                print(f" ✅")
                generated += 1
                # Delay between API calls
                if args.delay > 0:
                    time.sleep(args.delay)
            else:
                print(f" ❌ {msg}")
                errors += 1
                error_list.append(f"{slug}_{lang}: {msg}")
                # Still delay to avoid rate limiting
                time.sleep(args.delay)

    elapsed = time.time() - start_time
    actual_cost = generated * EST_COST_PER_CALL

    print()
    print(f"{'='*60}")
    print(f"Generated: {generated} | Cached: {skipped} | Errors: {errors}")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"Estimated API cost: ${actual_cost:.2f} USD")
    print(f"Output: {CONTENT_DIR}")

    if error_list:
        print(f"\n⚠️  Errors ({len(error_list)}):")
        for e in error_list[:20]:
            print(f"  - {e}")
        if len(error_list) > 20:
            print(f"  ... and {len(error_list)-20} more")
        print(f"\nTip: Re-run the same command to retry failed ones (cached successes will be skipped)")

    print(f"{'='*60}")


if __name__ == "__main__":
    main()
