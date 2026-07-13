#!/usr/bin/env python3
"""
SoftGlow — Comprehensive Search Index Generator v2.0
Scans all HTML pages (tools, patterns, comparisons) and builds search-index.json.
No API calls needed. Pure local file scanning.

Usage:
  cd the frontend directory
  python generate_search_index.py

Output: common\search-index.json
"""

import os
import re
import json
import sys

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "common", "search-index.json")

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]

# Directories to scan
SCAN_DIRS = {
    "tool":       os.path.join(BASE_DIR, "tools"),
    "pattern":    os.path.join(BASE_DIR, "patterns"),
    "comparison": os.path.join(BASE_DIR, "comparisons"),
}

# Index pages to skip (not individual content pages)
SKIP_FILES = {
    "index.html", "en.html", "ja.html", "ko.html",
    "de.html", "fr.html", "es.html", "pt.html", "id.html", "zh-CN.html",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_RE = re.compile(
    r'<meta\s+name=["\']sg-(\w+)["\']\s+content=["\']([^"\']*)["\']',
    re.IGNORECASE,
)


def extract_from_html(filepath):
    """Extract title and sg-* meta values from an HTML file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # Read only the first 3KB (head section) for speed
            head = f.read(3072)
    except Exception:
        return None, {}

    title = None
    m = TITLE_RE.search(head)
    if m:
        title = m.group(1).strip()
        # Clean up common suffixes
        for sep in [" | ", " — ", " - "]:
            if sep in title:
                title = title.split(sep)[0].strip()

    metas = {}
    for mm in META_RE.finditer(head):
        metas[mm.group(1)] = mm.group(2)

    return title, metas


def detect_lang_from_path(filepath, content_type):
    """Detect language from file path structure.

    zh-TW files: /tools/{slug}.html or /patterns/{slug}.html
    Other langs:  /tools/{lang}/{slug}.html or /patterns/{lang}/{slug}.html
    """
    parts = filepath.replace("\\", "/").split("/")

    # Check if parent directory is a language code
    parent = parts[-2] if len(parts) >= 2 else ""

    # Map directory names to lang codes
    lang_map = {
        "en": "en", "ja": "ja", "ko": "ko",
        "de": "de", "fr": "fr", "es": "es",
        "pt": "pt", "id": "id", "zh-CN": "zh-CN",
    }

    if parent in lang_map:
        return lang_map[parent]

    # If parent is the content type directory itself (tools/patterns/comparisons),
    # it's zh-TW (default language at root level)
    type_dirs = {"tools", "patterns", "comparisons"}
    if parent in type_dirs:
        return "zh-TW"

    # Check sg-lang meta (fallback)
    return None


def extract_slug_from_filename(filename):
    """Get slug from filename like 'compound-interest.html' -> 'compound-interest'."""
    return filename.replace(".html", "")


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------
def scan_all():
    """Scan all content directories and build the search index."""
    # slug -> { type, category, titles: {lang: title} }
    entries = {}

    for content_type, scan_dir in SCAN_DIRS.items():
        if not os.path.isdir(scan_dir):
            print(f"  SKIP {content_type}: directory not found ({scan_dir})")
            continue

        count = 0
        for root, _dirs, files in os.walk(scan_dir):
            for fname in files:
                if not fname.endswith(".html"):
                    continue
                if fname in SKIP_FILES:
                    continue

                filepath = os.path.join(root, fname)
                slug = extract_slug_from_filename(fname)
                lang = detect_lang_from_path(filepath, content_type)

                if lang is None:
                    # Try sg-lang meta
                    _, metas = extract_from_html(filepath)
                    lang = metas.get("lang", "zh-TW")

                title, metas = extract_from_html(filepath)
                if not title:
                    continue

                # Use sg-slug if available, otherwise filename
                actual_slug = metas.get("slug", slug)
                actual_type = metas.get("type", content_type)
                category = metas.get("category", content_type)

                # Create or update entry
                key = f"{actual_type}:{actual_slug}"
                if key not in entries:
                    entries[key] = {
                        "slug": actual_slug,
                        "type": actual_type,
                        "category": category,
                        "titles": {},
                    }

                entries[key]["titles"][lang] = title
                count += 1

        print(f"  {content_type}: scanned {count} files")

    return list(entries.values())


def build_urls(entry):
    """Add URL template info so JS can build links."""
    t = entry["type"]
    slug = entry["slug"]

    if t == "pattern":
        entry["url_zhTW"] = f"/patterns/{slug}.html"
        entry["url_tpl"] = f"/patterns/{{lang}}/{slug}.html"
    elif t == "comparison":
        entry["url_zhTW"] = f"/comparisons/{slug}.html"
        entry["url_tpl"] = f"/comparisons/{{lang}}/{slug}.html"
    else:  # tool
        entry["url_zhTW"] = f"/tools/{slug}.html"
        entry["url_tpl"] = f"/tools/{{lang}}/{slug}.html"

    return entry


def main():
    print("SoftGlow Search Index Generator v2.0")
    print("=" * 50)

    entries = scan_all()

    # Add URL templates
    for e in entries:
        build_urls(e)

    # Sort: patterns first, then comparisons, then tools (alphabetical within)
    type_order = {"pattern": 0, "comparison": 1, "tool": 2}
    entries.sort(key=lambda e: (type_order.get(e["type"], 9), e["slug"]))

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

    print(f"\n{'=' * 50}")
    print(f"Total entries: {len(entries)}")

    # Stats by type
    by_type = {}
    for e in entries:
        by_type[e["type"]] = by_type.get(e["type"], 0) + 1
    for t, c in sorted(by_type.items()):
        print(f"  {t}: {c}")

    # Check language coverage
    lang_counts = {}
    for e in entries:
        for lang in e["titles"]:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
    print(f"\nLanguage coverage:")
    for lang in LANGS:
        print(f"  {lang}: {lang_counts.get(lang, 0)} titles")

    print(f"\nOutput: {OUTPUT_PATH}")
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"File size: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
