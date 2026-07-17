#!/usr/bin/env python3
"""
SoftGlow Glossary Generator v1.0
生成 300 個金融術語 × 10 語言 = 3,000 頁 SEO 長尾頁面
Usage:
  cd D:\\xian-shang-you-wei\\backend
  set ANTHROPIC_API_KEY=sk-ant-api03-...
  python generate_glossary.py --langs zh-TW,en,ja
  python generate_glossary.py                      # 跑全部 10 語言
  python generate_glossary.py --start 100          # 從第 100 個術語開始
"""

import os, sys, json, re, time, argparse, hashlib
from datetime import datetime
from pathlib import Path

# ── 設定 ──────────────────────────────────────────
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 4096
OUTPUT_DIR = Path("output/glossary")
CACHE_DIR = OUTPUT_DIR / ".cache"
VERSION = "glossary-v1.0"
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
LANG_CODES = {
    "zh-TW": "zh-TW", "en": "en", "ja": "ja", "ko": "ko",
    "de": "de", "fr": "fr", "es": "es", "pt": "pt", "id": "id", "zh-CN": "zh-CN"
}

LANG_NAMES = {
    "zh-TW": "繁中", "en": "EN", "ja": "日本語", "ko": "한국어",
    "de": "DE", "fr": "FR", "es": "ES", "pt": "PT", "id": "ID", "zh-CN": "简中"
}

LANG_LABELS = {
    "zh-TW": {"home": "首頁", "glossary": "術語百科", "tools": "工具",
              "patterns": "K棒型態", "blog": "教學文章", "faq_title": "常見問題",
              "related_terms": "相關術語", "related_tools": "相關工具",
              "more_terms": "更多術語", "reading": "延伸閱讀",
              "calculate_btn": "計算", "last_updated": "最後更新",
              "data_source": "資料來源"},
    "en": {"home": "Home", "glossary": "Glossary", "tools": "Tools",
            "patterns": "Candlestick", "blog": "Blog", "faq_title": "FAQ",
            "related_terms": "Related Terms", "related_tools": "Related Tools",
            "more_terms": "More Terms", "reading": "Further Reading",
            "calculate_btn": "Calculate", "last_updated": "Last Updated",
            "data_source": "Data Source"},
    "ja": {"home": "ホーム", "glossary": "用語集", "tools": "ツール",
            "patterns": "ローソク足", "blog": "ブログ", "faq_title": "よくある質問",
            "related_terms": "関連用語", "related_tools": "関連ツール",
            "more_terms": "その他の用語", "reading": "関連記事",
            "calculate_btn": "計算", "last_updated": "最終更新",
            "data_source": "データソース"},
    "ko": {"home": "홈", "glossary": "용어사전", "tools": "도구",
            "patterns": "캔들패턴", "blog": "블로그", "faq_title": "자주 묻는 질문",
            "related_terms": "관련 용어", "related_tools": "관련 도구",
            "more_terms": "더 많은 용어", "reading": "추가 읽기",
            "calculate_btn": "계산", "last_updated": "마지막 업데이트",
            "data_source": "데이터 출처"},
    "de": {"home": "Startseite", "glossary": "Glossar", "tools": "Tools",
            "patterns": "Kerzenmuster", "blog": "Blog", "faq_title": "FAQ",
            "related_terms": "Verwandte Begriffe", "related_tools": "Verwandte Tools",
            "more_terms": "Weitere Begriffe", "reading": "Weiterführende Artikel",
            "calculate_btn": "Berechnen", "last_updated": "Zuletzt aktualisiert",
            "data_source": "Datenquelle"},
    "fr": {"home": "Accueil", "glossary": "Glossaire", "tools": "Outils",
            "patterns": "Chandeliers", "blog": "Blog", "faq_title": "FAQ",
            "related_terms": "Termes associés", "related_tools": "Outils associés",
            "more_terms": "Plus de termes", "reading": "Articles connexes",
            "calculate_btn": "Calculer", "last_updated": "Dernière mise à jour",
            "data_source": "Source des données"},
    "es": {"home": "Inicio", "glossary": "Glosario", "tools": "Herramientas",
            "patterns": "Velas", "blog": "Blog", "faq_title": "Preguntas frecuentes",
            "related_terms": "Términos relacionados", "related_tools": "Herramientas relacionadas",
            "more_terms": "Más términos", "reading": "Lecturas adicionales",
            "calculate_btn": "Calcular", "last_updated": "Última actualización",
            "data_source": "Fuente de datos"},
    "pt": {"home": "Início", "glossary": "Glossário", "tools": "Ferramentas",
            "patterns": "Candlestick", "blog": "Blog", "faq_title": "Perguntas frequentes",
            "related_terms": "Termos relacionados", "related_tools": "Ferramentas relacionadas",
            "more_terms": "Mais termos", "reading": "Leitura adicional",
            "calculate_btn": "Calcular", "last_updated": "Última atualização",
            "data_source": "Fonte de dados"},
    "id": {"home": "Beranda", "glossary": "Glosarium", "tools": "Alat",
            "patterns": "Candlestick", "blog": "Blog", "faq_title": "FAQ",
            "related_terms": "Istilah Terkait", "related_tools": "Alat Terkait",
            "more_terms": "Istilah Lainnya", "reading": "Bacaan Lanjutan",
            "calculate_btn": "Hitung", "last_updated": "Terakhir diperbarui",
            "data_source": "Sumber data"},
    "zh-CN": {"home": "首页", "glossary": "术语百科", "tools": "工具",
              "patterns": "K线形态", "blog": "教学文章", "faq_title": "常见问题",
              "related_terms": "相关术语", "related_tools": "相关工具",
              "more_terms": "更多术语", "reading": "延伸阅读",
              "calculate_btn": "计算", "last_updated": "最后更新",
              "data_source": "数据来源"},
}

# ── 術語定義（300 個）──────────────────────────────
# category, slug, related_tools (list), related_terms (list)
GLOSSARY_TERMS = [
    # ── 投資基礎 (25) ──
    {"cat": "investment-basics", "slug": "compound-interest", "tools": ["compound-interest"], "terms": ["simple-interest", "annual-return", "rule-of-72"]},
    {"cat": "investment-basics", "slug": "simple-interest", "tools": ["compound-interest"], "terms": ["compound-interest", "annual-return", "apr"]},
    {"cat": "investment-basics", "slug": "annual-return", "tools": ["roi-calculator", "cagr"], "terms": ["cagr", "roi", "compound-interest"]},
    {"cat": "investment-basics", "slug": "roi", "tools": ["roi-calculator"], "terms": ["annual-return", "cagr", "irr"]},
    {"cat": "investment-basics", "slug": "cagr", "tools": ["cagr"], "terms": ["annual-return", "roi", "compound-interest"]},
    {"cat": "investment-basics", "slug": "rule-of-72", "tools": ["rule-of-72"], "terms": ["compound-interest", "annual-return", "inflation"]},
    {"cat": "investment-basics", "slug": "asset-allocation", "tools": ["asset-allocation"], "terms": ["diversification", "risk-tolerance", "portfolio-rebalancing"]},
    {"cat": "investment-basics", "slug": "diversification", "tools": ["asset-allocation"], "terms": ["asset-allocation", "risk-tolerance", "correlation"]},
    {"cat": "investment-basics", "slug": "risk-tolerance", "tools": ["asset-allocation"], "terms": ["diversification", "asset-allocation", "volatility"]},
    {"cat": "investment-basics", "slug": "dollar-cost-averaging", "tools": ["dca-calculator"], "terms": ["compound-interest", "asset-allocation", "market-timing"]},
    {"cat": "investment-basics", "slug": "market-timing", "tools": ["dca-calculator"], "terms": ["dollar-cost-averaging", "buy-and-hold", "volatility"]},
    {"cat": "investment-basics", "slug": "buy-and-hold", "tools": ["compound-interest"], "terms": ["dollar-cost-averaging", "market-timing", "annual-return"]},
    {"cat": "investment-basics", "slug": "inflation", "tools": ["inflation"], "terms": ["cpi", "purchasing-power", "real-return"]},
    {"cat": "investment-basics", "slug": "purchasing-power", "tools": ["inflation"], "terms": ["inflation", "cpi", "real-return"]},
    {"cat": "investment-basics", "slug": "real-return", "tools": ["inflation"], "terms": ["inflation", "nominal-return", "purchasing-power"]},
    {"cat": "investment-basics", "slug": "nominal-return", "tools": ["roi-calculator"], "terms": ["real-return", "inflation", "annual-return"]},
    {"cat": "investment-basics", "slug": "liquidity", "tools": [], "terms": ["bid-ask-spread", "market-depth", "trading-volume"]},
    {"cat": "investment-basics", "slug": "time-value-of-money", "tools": ["compound-interest"], "terms": ["present-value", "future-value", "discount-rate"]},
    {"cat": "investment-basics", "slug": "present-value", "tools": ["dcf-calculator"], "terms": ["future-value", "discount-rate", "time-value-of-money"]},
    {"cat": "investment-basics", "slug": "future-value", "tools": ["compound-interest"], "terms": ["present-value", "compound-interest", "time-value-of-money"]},
    {"cat": "investment-basics", "slug": "discount-rate", "tools": ["dcf-calculator"], "terms": ["present-value", "irr", "wacc"]},
    {"cat": "investment-basics", "slug": "irr", "tools": ["roi-calculator"], "terms": ["discount-rate", "npv", "roi"]},
    {"cat": "investment-basics", "slug": "npv", "tools": ["dcf-calculator"], "terms": ["irr", "discount-rate", "present-value"]},
    {"cat": "investment-basics", "slug": "opportunity-cost", "tools": [], "terms": ["roi", "time-value-of-money", "risk-tolerance"]},
    {"cat": "investment-basics", "slug": "portfolio-rebalancing", "tools": ["asset-allocation"], "terms": ["asset-allocation", "diversification", "risk-tolerance"]},

    # ── 股票交易 (25) ──
    {"cat": "stock-trading", "slug": "pe-ratio", "tools": ["pe-ratio"], "terms": ["eps", "peg-ratio", "market-cap"]},
    {"cat": "stock-trading", "slug": "eps", "tools": ["pe-ratio"], "terms": ["pe-ratio", "dividend-yield", "payout-ratio"]},
    {"cat": "stock-trading", "slug": "dividend-yield", "tools": ["dividend-yield"], "terms": ["eps", "payout-ratio", "ex-dividend-date"]},
    {"cat": "stock-trading", "slug": "payout-ratio", "tools": ["dividend-yield"], "terms": ["dividend-yield", "eps", "retained-earnings"]},
    {"cat": "stock-trading", "slug": "market-cap", "tools": [], "terms": ["pe-ratio", "enterprise-value", "shares-outstanding"]},
    {"cat": "stock-trading", "slug": "shares-outstanding", "tools": [], "terms": ["market-cap", "eps", "stock-split"]},
    {"cat": "stock-trading", "slug": "stock-split", "tools": ["stock-split"], "terms": ["shares-outstanding", "market-cap", "reverse-split"]},
    {"cat": "stock-trading", "slug": "reverse-split", "tools": ["stock-split"], "terms": ["stock-split", "shares-outstanding", "delisting"]},
    {"cat": "stock-trading", "slug": "bid-ask-spread", "tools": [], "terms": ["liquidity", "market-order", "limit-order"]},
    {"cat": "stock-trading", "slug": "market-order", "tools": [], "terms": ["limit-order", "bid-ask-spread", "slippage"]},
    {"cat": "stock-trading", "slug": "limit-order", "tools": [], "terms": ["market-order", "stop-order", "bid-ask-spread"]},
    {"cat": "stock-trading", "slug": "stop-order", "tools": ["stop-loss"], "terms": ["limit-order", "stop-loss", "trailing-stop"]},
    {"cat": "stock-trading", "slug": "trailing-stop", "tools": ["stop-loss"], "terms": ["stop-order", "stop-loss", "risk-management"]},
    {"cat": "stock-trading", "slug": "margin-trading", "tools": ["margin-calculator"], "terms": ["leverage", "margin-call", "short-selling"]},
    {"cat": "stock-trading", "slug": "margin-call", "tools": ["margin-calculator"], "terms": ["margin-trading", "leverage", "liquidation"]},
    {"cat": "stock-trading", "slug": "short-selling", "tools": [], "terms": ["margin-trading", "bear-market", "short-squeeze"]},
    {"cat": "stock-trading", "slug": "short-squeeze", "tools": [], "terms": ["short-selling", "trading-volume", "volatility"]},
    {"cat": "stock-trading", "slug": "trading-volume", "tools": [], "terms": ["liquidity", "average-volume", "volume-spike"]},
    {"cat": "stock-trading", "slug": "ex-dividend-date", "tools": ["dividend-yield"], "terms": ["dividend-yield", "record-date", "payout-ratio"]},
    {"cat": "stock-trading", "slug": "book-value", "tools": ["intrinsic-value"], "terms": ["pb-ratio", "net-asset-value", "intrinsic-value"]},
    {"cat": "stock-trading", "slug": "pb-ratio", "tools": ["intrinsic-value"], "terms": ["book-value", "pe-ratio", "market-cap"]},
    {"cat": "stock-trading", "slug": "enterprise-value", "tools": ["dcf-calculator"], "terms": ["market-cap", "ev-ebitda", "debt-to-equity"]},
    {"cat": "stock-trading", "slug": "peg-ratio", "tools": ["pe-ratio"], "terms": ["pe-ratio", "eps-growth", "valuation"]},
    {"cat": "stock-trading", "slug": "blue-chip", "tools": [], "terms": ["market-cap", "dividend-yield", "large-cap"]},
    {"cat": "stock-trading", "slug": "ipo", "tools": [], "terms": ["shares-outstanding", "market-cap", "underwriting"]},

    # ── 技術分析 (30) ──
    {"cat": "technical-analysis", "slug": "rsi", "tools": ["rsi-calculator"], "terms": ["overbought", "oversold", "macd"]},
    {"cat": "technical-analysis", "slug": "macd", "tools": ["macd-calculator"], "terms": ["rsi", "signal-line", "histogram"]},
    {"cat": "technical-analysis", "slug": "kd-indicator", "tools": [], "terms": ["rsi", "golden-cross", "death-cross"]},
    {"cat": "technical-analysis", "slug": "bollinger-bands", "tools": ["bollinger-bands"], "terms": ["standard-deviation", "volatility", "mean-reversion"]},
    {"cat": "technical-analysis", "slug": "moving-average", "tools": ["ma-crossover"], "terms": ["sma", "ema", "golden-cross"]},
    {"cat": "technical-analysis", "slug": "sma", "tools": ["ma-crossover"], "terms": ["ema", "moving-average", "ma-crossover"]},
    {"cat": "technical-analysis", "slug": "ema", "tools": ["ma-crossover"], "terms": ["sma", "moving-average", "macd"]},
    {"cat": "technical-analysis", "slug": "golden-cross", "tools": ["ma-crossover"], "terms": ["death-cross", "moving-average", "bull-market"]},
    {"cat": "technical-analysis", "slug": "death-cross", "tools": ["ma-crossover"], "terms": ["golden-cross", "moving-average", "bear-market"]},
    {"cat": "technical-analysis", "slug": "support-level", "tools": ["support-resistance"], "terms": ["resistance-level", "breakout", "fibonacci-retracement"]},
    {"cat": "technical-analysis", "slug": "resistance-level", "tools": ["support-resistance"], "terms": ["support-level", "breakout", "pivot-point"]},
    {"cat": "technical-analysis", "slug": "breakout", "tools": [], "terms": ["support-level", "resistance-level", "trading-volume"]},
    {"cat": "technical-analysis", "slug": "fibonacci-retracement", "tools": ["fibonacci-retracement"], "terms": ["support-level", "golden-ratio", "elliott-wave"]},
    {"cat": "technical-analysis", "slug": "pivot-point", "tools": ["pivot-point"], "terms": ["support-level", "resistance-level", "day-trading"]},
    {"cat": "technical-analysis", "slug": "atr", "tools": ["atr-calculator"], "terms": ["volatility", "stop-loss", "position-sizing"]},
    {"cat": "technical-analysis", "slug": "volatility", "tools": ["bollinger-bands"], "terms": ["standard-deviation", "atr", "vix"]},
    {"cat": "technical-analysis", "slug": "overbought", "tools": ["rsi-calculator"], "terms": ["oversold", "rsi", "mean-reversion"]},
    {"cat": "technical-analysis", "slug": "oversold", "tools": ["rsi-calculator"], "terms": ["overbought", "rsi", "mean-reversion"]},
    {"cat": "technical-analysis", "slug": "divergence", "tools": ["rsi-calculator", "macd-calculator"], "terms": ["rsi", "macd", "trend-reversal"]},
    {"cat": "technical-analysis", "slug": "trend-reversal", "tools": [], "terms": ["divergence", "head-and-shoulders", "double-bottom"]},
    {"cat": "technical-analysis", "slug": "trend-line", "tools": [], "terms": ["support-level", "resistance-level", "channel"]},
    {"cat": "technical-analysis", "slug": "volume-spike", "tools": [], "terms": ["trading-volume", "breakout", "accumulation"]},
    {"cat": "technical-analysis", "slug": "mean-reversion", "tools": ["bollinger-bands"], "terms": ["bollinger-bands", "overbought", "oversold"]},
    {"cat": "technical-analysis", "slug": "momentum", "tools": ["rsi-calculator"], "terms": ["rsi", "macd", "rate-of-change"]},
    {"cat": "technical-analysis", "slug": "ma-crossover", "tools": ["ma-crossover"], "terms": ["golden-cross", "death-cross", "moving-average"]},
    {"cat": "technical-analysis", "slug": "signal-line", "tools": ["macd-calculator"], "terms": ["macd", "histogram", "crossover"]},
    {"cat": "technical-analysis", "slug": "histogram", "tools": ["macd-calculator"], "terms": ["macd", "signal-line", "momentum"]},
    {"cat": "technical-analysis", "slug": "bull-market", "tools": [], "terms": ["bear-market", "golden-cross", "trend-line"]},
    {"cat": "technical-analysis", "slug": "bear-market", "tools": [], "terms": ["bull-market", "death-cross", "correction"]},
    {"cat": "technical-analysis", "slug": "day-trading", "tools": ["pivot-point"], "terms": ["swing-trading", "scalping", "pivot-point"]},

    # ── 債券固收 (15) ──
    {"cat": "bonds", "slug": "yield-curve", "tools": [], "terms": ["bond-yield", "interest-rate", "inverted-yield-curve"]},
    {"cat": "bonds", "slug": "coupon-rate", "tools": [], "terms": ["bond-yield", "face-value", "ytm"]},
    {"cat": "bonds", "slug": "ytm", "tools": [], "terms": ["coupon-rate", "bond-yield", "duration"]},
    {"cat": "bonds", "slug": "bond-yield", "tools": [], "terms": ["coupon-rate", "ytm", "yield-curve"]},
    {"cat": "bonds", "slug": "duration", "tools": [], "terms": ["bond-yield", "interest-rate-risk", "convexity"]},
    {"cat": "bonds", "slug": "credit-rating", "tools": [], "terms": ["default-risk", "bond-yield", "investment-grade"]},
    {"cat": "bonds", "slug": "face-value", "tools": [], "terms": ["coupon-rate", "par-value", "bond-yield"]},
    {"cat": "bonds", "slug": "inverted-yield-curve", "tools": [], "terms": ["yield-curve", "recession", "interest-rate"]},
    {"cat": "bonds", "slug": "corporate-bond", "tools": [], "terms": ["government-bond", "credit-rating", "bond-yield"]},
    {"cat": "bonds", "slug": "government-bond", "tools": [], "terms": ["corporate-bond", "treasury", "risk-free-rate"]},
    {"cat": "bonds", "slug": "treasury", "tools": [], "terms": ["government-bond", "risk-free-rate", "yield-curve"]},
    {"cat": "bonds", "slug": "risk-free-rate", "tools": ["sharpe-ratio"], "terms": ["treasury", "sharpe-ratio", "risk-premium"]},
    {"cat": "bonds", "slug": "risk-premium", "tools": [], "terms": ["risk-free-rate", "equity-risk-premium", "sharpe-ratio"]},
    {"cat": "bonds", "slug": "default-risk", "tools": [], "terms": ["credit-rating", "corporate-bond", "junk-bond"]},
    {"cat": "bonds", "slug": "junk-bond", "tools": [], "terms": ["credit-rating", "default-risk", "high-yield"]},

    # ── 基金 ETF (15) ──
    {"cat": "funds-etf", "slug": "nav", "tools": [], "terms": ["etf", "mutual-fund", "expense-ratio"]},
    {"cat": "funds-etf", "slug": "expense-ratio", "tools": [], "terms": ["nav", "management-fee", "total-return"]},
    {"cat": "funds-etf", "slug": "etf", "tools": [], "terms": ["mutual-fund", "index-fund", "tracking-error"]},
    {"cat": "funds-etf", "slug": "mutual-fund", "tools": [], "terms": ["etf", "nav", "expense-ratio"]},
    {"cat": "funds-etf", "slug": "index-fund", "tools": [], "terms": ["etf", "passive-investing", "benchmark"]},
    {"cat": "funds-etf", "slug": "tracking-error", "tools": [], "terms": ["etf", "index-fund", "benchmark"]},
    {"cat": "funds-etf", "slug": "benchmark", "tools": [], "terms": ["index-fund", "tracking-error", "alpha"]},
    {"cat": "funds-etf", "slug": "alpha", "tools": ["sharpe-ratio"], "terms": ["beta", "benchmark", "sharpe-ratio"]},
    {"cat": "funds-etf", "slug": "beta", "tools": [], "terms": ["alpha", "volatility", "systematic-risk"]},
    {"cat": "funds-etf", "slug": "passive-investing", "tools": ["dca-calculator"], "terms": ["index-fund", "active-investing", "dollar-cost-averaging"]},
    {"cat": "funds-etf", "slug": "active-investing", "tools": [], "terms": ["passive-investing", "alpha", "fund-manager"]},
    {"cat": "funds-etf", "slug": "leveraged-etf", "tools": [], "terms": ["etf", "leverage", "inverse-etf"]},
    {"cat": "funds-etf", "slug": "inverse-etf", "tools": [], "terms": ["leveraged-etf", "short-selling", "hedging"]},
    {"cat": "funds-etf", "slug": "total-return", "tools": ["roi-calculator"], "terms": ["dividend-yield", "capital-gain", "annual-return"]},
    {"cat": "funds-etf", "slug": "capital-gain", "tools": ["capital-gains-tax"], "terms": ["total-return", "capital-gains-tax", "unrealized-gain"]},

    # ── 房地產 (20) ──
    {"cat": "real-estate", "slug": "ltv", "tools": ["mortgage"], "terms": ["down-payment", "mortgage", "pmi"]},
    {"cat": "real-estate", "slug": "down-payment", "tools": ["mortgage"], "terms": ["ltv", "mortgage", "closing-costs"]},
    {"cat": "real-estate", "slug": "mortgage", "tools": ["mortgage"], "terms": ["down-payment", "interest-rate", "amortization"]},
    {"cat": "real-estate", "slug": "amortization", "tools": ["mortgage"], "terms": ["mortgage", "principal", "interest-payment"]},
    {"cat": "real-estate", "slug": "principal", "tools": ["mortgage"], "terms": ["amortization", "interest-payment", "loan-balance"]},
    {"cat": "real-estate", "slug": "refinance", "tools": ["mortgage-refinance"], "terms": ["mortgage", "interest-rate", "break-even-point"]},
    {"cat": "real-estate", "slug": "equity", "tools": [], "terms": ["ltv", "mortgage", "home-value"]},
    {"cat": "real-estate", "slug": "rental-yield", "tools": ["rental-yield"], "terms": ["cap-rate", "roi", "cash-flow"]},
    {"cat": "real-estate", "slug": "cap-rate", "tools": ["rental-yield"], "terms": ["rental-yield", "noi", "property-valuation"]},
    {"cat": "real-estate", "slug": "closing-costs", "tools": ["mortgage"], "terms": ["down-payment", "mortgage", "escrow"]},
    {"cat": "real-estate", "slug": "property-tax", "tools": [], "terms": ["closing-costs", "escrow", "assessed-value"]},
    {"cat": "real-estate", "slug": "pmi", "tools": ["mortgage"], "terms": ["ltv", "down-payment", "mortgage"]},
    {"cat": "real-estate", "slug": "fixed-rate-mortgage", "tools": ["mortgage"], "terms": ["adjustable-rate-mortgage", "interest-rate", "mortgage"]},
    {"cat": "real-estate", "slug": "adjustable-rate-mortgage", "tools": ["mortgage"], "terms": ["fixed-rate-mortgage", "interest-rate", "rate-cap"]},
    {"cat": "real-estate", "slug": "home-equity-loan", "tools": [], "terms": ["equity", "heloc", "refinance"]},
    {"cat": "real-estate", "slug": "rent-vs-buy", "tools": ["rent-vs-buy"], "terms": ["mortgage", "rental-yield", "opportunity-cost"]},
    {"cat": "real-estate", "slug": "appreciation", "tools": [], "terms": ["depreciation", "home-value", "roi"]},
    {"cat": "real-estate", "slug": "depreciation", "tools": [], "terms": ["appreciation", "tax-deduction", "useful-life"]},
    {"cat": "real-estate", "slug": "cash-on-cash-return", "tools": ["rental-yield"], "terms": ["cap-rate", "rental-yield", "roi"]},
    {"cat": "real-estate", "slug": "gross-rent-multiplier", "tools": [], "terms": ["cap-rate", "rental-yield", "property-valuation"]},

    # ── 貸款信用 (15) ──
    {"cat": "loans-credit", "slug": "apr", "tools": ["loan-comparison"], "terms": ["apy", "interest-rate", "effective-rate"]},
    {"cat": "loans-credit", "slug": "apy", "tools": ["compound-interest"], "terms": ["apr", "compound-interest", "effective-rate"]},
    {"cat": "loans-credit", "slug": "credit-score", "tools": [], "terms": ["credit-report", "credit-utilization", "apr"]},
    {"cat": "loans-credit", "slug": "credit-utilization", "tools": ["credit-card-payoff"], "terms": ["credit-score", "credit-limit", "debt-to-income"]},
    {"cat": "loans-credit", "slug": "debt-to-income", "tools": [], "terms": ["credit-score", "mortgage", "loan-qualification"]},
    {"cat": "loans-credit", "slug": "grace-period", "tools": ["credit-card-payoff"], "terms": ["interest-rate", "minimum-payment", "late-fee"]},
    {"cat": "loans-credit", "slug": "minimum-payment", "tools": ["credit-card-payoff"], "terms": ["grace-period", "interest-charge", "debt-snowball"]},
    {"cat": "loans-credit", "slug": "debt-snowball", "tools": ["debt-payoff"], "terms": ["debt-avalanche", "minimum-payment", "debt-free"]},
    {"cat": "loans-credit", "slug": "debt-avalanche", "tools": ["debt-payoff"], "terms": ["debt-snowball", "interest-rate", "debt-free"]},
    {"cat": "loans-credit", "slug": "secured-loan", "tools": [], "terms": ["unsecured-loan", "collateral", "interest-rate"]},
    {"cat": "loans-credit", "slug": "unsecured-loan", "tools": [], "terms": ["secured-loan", "credit-score", "personal-loan"]},
    {"cat": "loans-credit", "slug": "prepayment-penalty", "tools": ["mortgage"], "terms": ["refinance", "early-payoff", "mortgage"]},
    {"cat": "loans-credit", "slug": "consolidation-loan", "tools": ["loan-comparison"], "terms": ["debt-snowball", "interest-rate", "monthly-payment"]},
    {"cat": "loans-credit", "slug": "interest-rate", "tools": ["loan-comparison"], "terms": ["apr", "compound-interest", "central-bank-rate"]},
    {"cat": "loans-credit", "slug": "collateral", "tools": [], "terms": ["secured-loan", "mortgage", "default-risk"]},

    # ── 保險 (20) ──
    {"cat": "insurance", "slug": "premium", "tools": ["life-insurance-needs"], "terms": ["deductible", "coverage", "underwriting"]},
    {"cat": "insurance", "slug": "deductible", "tools": ["health-insurance-estimate"], "terms": ["premium", "copay", "out-of-pocket-max"]},
    {"cat": "insurance", "slug": "coverage", "tools": ["life-insurance-needs"], "terms": ["premium", "exclusion", "policy-limit"]},
    {"cat": "insurance", "slug": "term-life", "tools": ["life-insurance-needs"], "terms": ["whole-life", "premium", "death-benefit"]},
    {"cat": "insurance", "slug": "whole-life", "tools": ["life-insurance-needs"], "terms": ["term-life", "cash-value", "premium"]},
    {"cat": "insurance", "slug": "cash-value", "tools": [], "terms": ["whole-life", "surrender-value", "policy-loan"]},
    {"cat": "insurance", "slug": "death-benefit", "tools": ["life-insurance-needs"], "terms": ["term-life", "beneficiary", "coverage"]},
    {"cat": "insurance", "slug": "beneficiary", "tools": [], "terms": ["death-benefit", "estate-planning", "trust"]},
    {"cat": "insurance", "slug": "underwriting", "tools": [], "terms": ["premium", "risk-assessment", "coverage"]},
    {"cat": "insurance", "slug": "copay", "tools": ["health-insurance-estimate"], "terms": ["deductible", "coinsurance", "out-of-pocket-max"]},
    {"cat": "insurance", "slug": "coinsurance", "tools": ["health-insurance-estimate"], "terms": ["copay", "deductible", "out-of-pocket-max"]},
    {"cat": "insurance", "slug": "out-of-pocket-max", "tools": ["health-insurance-estimate"], "terms": ["deductible", "copay", "coinsurance"]},
    {"cat": "insurance", "slug": "waiting-period", "tools": [], "terms": ["pre-existing-condition", "coverage", "exclusion"]},
    {"cat": "insurance", "slug": "exclusion", "tools": [], "terms": ["coverage", "waiting-period", "claim"]},
    {"cat": "insurance", "slug": "claim", "tools": [], "terms": ["coverage", "deductible", "reimbursement"]},
    {"cat": "insurance", "slug": "liability-insurance", "tools": ["car-insurance-calc"], "terms": ["coverage", "premium", "negligence"]},
    {"cat": "insurance", "slug": "comprehensive-insurance", "tools": ["car-insurance-calc"], "terms": ["collision-insurance", "deductible", "premium"]},
    {"cat": "insurance", "slug": "annuity", "tools": ["annuity-income"], "terms": ["pension", "retirement-income", "lump-sum"]},
    {"cat": "insurance", "slug": "pension", "tools": ["retirement"], "terms": ["annuity", "defined-benefit", "retirement-income"]},
    {"cat": "insurance", "slug": "long-term-care", "tools": [], "terms": ["premium", "waiting-period", "benefit-period"]},

    # ── 稅務 (15) ──
    {"cat": "tax", "slug": "progressive-tax", "tools": ["income-tax"], "terms": ["tax-bracket", "marginal-rate", "effective-rate"]},
    {"cat": "tax", "slug": "tax-bracket", "tools": ["income-tax"], "terms": ["progressive-tax", "marginal-rate", "taxable-income"]},
    {"cat": "tax", "slug": "marginal-rate", "tools": ["income-tax"], "terms": ["effective-rate", "tax-bracket", "progressive-tax"]},
    {"cat": "tax", "slug": "effective-rate", "tools": ["income-tax"], "terms": ["marginal-rate", "tax-bracket", "total-tax"]},
    {"cat": "tax", "slug": "tax-deduction", "tools": ["income-tax"], "terms": ["tax-credit", "taxable-income", "standard-deduction"]},
    {"cat": "tax", "slug": "tax-credit", "tools": ["income-tax"], "terms": ["tax-deduction", "refund", "effective-rate"]},
    {"cat": "tax", "slug": "capital-gains-tax", "tools": ["capital-gains-tax"], "terms": ["capital-gain", "holding-period", "tax-bracket"]},
    {"cat": "tax", "slug": "taxable-income", "tools": ["income-tax"], "terms": ["gross-income", "tax-deduction", "adjusted-gross-income"]},
    {"cat": "tax", "slug": "estate-tax", "tools": [], "terms": ["inheritance-tax", "estate-planning", "exemption"]},
    {"cat": "tax", "slug": "gift-tax", "tools": [], "terms": ["estate-tax", "annual-exclusion", "lifetime-exemption"]},
    {"cat": "tax", "slug": "sales-tax", "tools": ["sales-tax"], "terms": ["vat", "consumption-tax", "tax-rate"]},
    {"cat": "tax", "slug": "vat", "tools": [], "terms": ["sales-tax", "consumption-tax", "input-tax-credit"]},
    {"cat": "tax", "slug": "withholding-tax", "tools": ["take-home-pay"], "terms": ["payroll-tax", "w4", "tax-refund"]},
    {"cat": "tax", "slug": "tax-loss-harvesting", "tools": [], "terms": ["capital-gains-tax", "wash-sale", "tax-efficiency"]},
    {"cat": "tax", "slug": "depreciation-tax", "tools": [], "terms": ["tax-deduction", "useful-life", "accelerated-depreciation"]},

    # ── 退休規劃 (15) ──
    {"cat": "retirement", "slug": "retirement-planning", "tools": ["retirement"], "terms": ["retirement-savings", "replacement-ratio", "social-security"]},
    {"cat": "retirement", "slug": "replacement-ratio", "tools": ["retirement"], "terms": ["retirement-planning", "retirement-income", "savings-rate"]},
    {"cat": "retirement", "slug": "401k", "tools": ["401k-contribution"], "terms": ["ira", "employer-match", "tax-deferred"]},
    {"cat": "retirement", "slug": "ira", "tools": ["retirement"], "terms": ["401k", "roth-ira", "traditional-ira"]},
    {"cat": "retirement", "slug": "roth-ira", "tools": ["retirement"], "terms": ["ira", "traditional-ira", "tax-free-growth"]},
    {"cat": "retirement", "slug": "employer-match", "tools": ["401k-contribution"], "terms": ["401k", "vesting", "free-money"]},
    {"cat": "retirement", "slug": "vesting", "tools": ["401k-contribution"], "terms": ["employer-match", "cliff-vesting", "graded-vesting"]},
    {"cat": "retirement", "slug": "required-minimum-distribution", "tools": ["retirement"], "terms": ["401k", "ira", "tax-penalty"]},
    {"cat": "retirement", "slug": "social-security", "tools": ["retirement"], "terms": ["retirement-planning", "full-retirement-age", "benefit-calculation"]},
    {"cat": "retirement", "slug": "fire-movement", "tools": ["retirement"], "terms": ["savings-rate", "safe-withdrawal-rate", "financial-independence"]},
    {"cat": "retirement", "slug": "safe-withdrawal-rate", "tools": ["retirement"], "terms": ["fire-movement", "four-percent-rule", "sequence-of-returns"]},
    {"cat": "retirement", "slug": "four-percent-rule", "tools": ["retirement"], "terms": ["safe-withdrawal-rate", "retirement-income", "portfolio-longevity"]},
    {"cat": "retirement", "slug": "tax-deferred", "tools": ["401k-contribution"], "terms": ["401k", "ira", "tax-free-growth"]},
    {"cat": "retirement", "slug": "catch-up-contribution", "tools": ["401k-contribution"], "terms": ["401k", "ira", "contribution-limit"]},
    {"cat": "retirement", "slug": "annuity-income", "tools": ["annuity-income"], "terms": ["pension", "retirement-income", "lump-sum-vs-annuity"]},

    # ── 總體經濟 (20) ──
    {"cat": "macro", "slug": "gdp", "tools": [], "terms": ["gnp", "economic-growth", "recession"]},
    {"cat": "macro", "slug": "cpi", "tools": ["inflation"], "terms": ["inflation", "ppi", "core-inflation"]},
    {"cat": "macro", "slug": "core-inflation", "tools": ["inflation"], "terms": ["cpi", "inflation", "fed-funds-rate"]},
    {"cat": "macro", "slug": "fed-funds-rate", "tools": [], "terms": ["interest-rate", "monetary-policy", "central-bank"]},
    {"cat": "macro", "slug": "monetary-policy", "tools": [], "terms": ["fed-funds-rate", "quantitative-easing", "central-bank"]},
    {"cat": "macro", "slug": "quantitative-easing", "tools": [], "terms": ["monetary-policy", "bond-buying", "inflation"]},
    {"cat": "macro", "slug": "recession", "tools": [], "terms": ["gdp", "bear-market", "unemployment"]},
    {"cat": "macro", "slug": "unemployment-rate", "tools": [], "terms": ["gdp", "recession", "labor-force"]},
    {"cat": "macro", "slug": "fiscal-policy", "tools": [], "terms": ["monetary-policy", "government-spending", "national-debt"]},
    {"cat": "macro", "slug": "trade-deficit", "tools": [], "terms": ["trade-surplus", "current-account", "exchange-rate"]},
    {"cat": "macro", "slug": "exchange-rate", "tools": ["currency-converter"], "terms": ["forex", "purchasing-power-parity", "trade-deficit"]},
    {"cat": "macro", "slug": "purchasing-power-parity", "tools": [], "terms": ["exchange-rate", "big-mac-index", "inflation"]},
    {"cat": "macro", "slug": "central-bank", "tools": [], "terms": ["fed-funds-rate", "monetary-policy", "interest-rate"]},
    {"cat": "macro", "slug": "yield-spread", "tools": [], "terms": ["yield-curve", "credit-spread", "risk-premium"]},
    {"cat": "macro", "slug": "stagflation", "tools": [], "terms": ["inflation", "recession", "unemployment-rate"]},
    {"cat": "macro", "slug": "deflation", "tools": [], "terms": ["inflation", "cpi", "monetary-policy"]},
    {"cat": "macro", "slug": "hyperinflation", "tools": ["inflation"], "terms": ["inflation", "monetary-policy", "currency-devaluation"]},
    {"cat": "macro", "slug": "national-debt", "tools": [], "terms": ["fiscal-policy", "debt-to-gdp", "government-bond"]},
    {"cat": "macro", "slug": "supply-and-demand", "tools": [], "terms": ["equilibrium-price", "market-economy", "price-elasticity"]},
    {"cat": "macro", "slug": "business-cycle", "tools": [], "terms": ["recession", "expansion", "gdp"]},

    # ── 風險管理 (15) ──
    {"cat": "risk-management", "slug": "sharpe-ratio", "tools": ["sharpe-ratio"], "terms": ["risk-free-rate", "standard-deviation", "sortino-ratio"]},
    {"cat": "risk-management", "slug": "sortino-ratio", "tools": ["sharpe-ratio"], "terms": ["sharpe-ratio", "downside-risk", "standard-deviation"]},
    {"cat": "risk-management", "slug": "max-drawdown", "tools": [], "terms": ["risk-management", "volatility", "recovery-time"]},
    {"cat": "risk-management", "slug": "var", "tools": [], "terms": ["risk-management", "confidence-interval", "portfolio-risk"]},
    {"cat": "risk-management", "slug": "stop-loss", "tools": ["stop-loss"], "terms": ["risk-reward-ratio", "trailing-stop", "position-sizing"]},
    {"cat": "risk-management", "slug": "risk-reward-ratio", "tools": ["risk-reward"], "terms": ["stop-loss", "take-profit", "win-rate"]},
    {"cat": "risk-management", "slug": "position-sizing", "tools": ["position-size"], "terms": ["risk-management", "kelly-criterion", "stop-loss"]},
    {"cat": "risk-management", "slug": "hedging", "tools": [], "terms": ["diversification", "options", "inverse-etf"]},
    {"cat": "risk-management", "slug": "correlation", "tools": [], "terms": ["diversification", "portfolio-risk", "beta"]},
    {"cat": "risk-management", "slug": "systematic-risk", "tools": [], "terms": ["unsystematic-risk", "beta", "market-risk"]},
    {"cat": "risk-management", "slug": "unsystematic-risk", "tools": [], "terms": ["systematic-risk", "diversification", "company-specific-risk"]},
    {"cat": "risk-management", "slug": "standard-deviation", "tools": ["sharpe-ratio"], "terms": ["volatility", "variance", "normal-distribution"]},
    {"cat": "risk-management", "slug": "risk-management", "tools": ["position-size", "stop-loss"], "terms": ["position-sizing", "stop-loss", "diversification"]},
    {"cat": "risk-management", "slug": "leverage", "tools": ["margin-calculator"], "terms": ["margin-trading", "risk-reward-ratio", "margin-call"]},
    {"cat": "risk-management", "slug": "win-rate", "tools": ["risk-reward"], "terms": ["risk-reward-ratio", "expectancy", "trading-journal"]},

    # ── 企業財務 (15) ──
    {"cat": "corporate-finance", "slug": "cash-flow", "tools": [], "terms": ["operating-cash-flow", "free-cash-flow", "cash-flow-statement"]},
    {"cat": "corporate-finance", "slug": "free-cash-flow", "tools": ["dcf-calculator"], "terms": ["cash-flow", "operating-cash-flow", "dcf"]},
    {"cat": "corporate-finance", "slug": "income-statement", "tools": [], "terms": ["balance-sheet", "revenue", "net-income"]},
    {"cat": "corporate-finance", "slug": "balance-sheet", "tools": [], "terms": ["income-statement", "assets", "liabilities"]},
    {"cat": "corporate-finance", "slug": "ebitda", "tools": [], "terms": ["ev-ebitda", "operating-income", "net-income"]},
    {"cat": "corporate-finance", "slug": "ev-ebitda", "tools": [], "terms": ["ebitda", "enterprise-value", "pe-ratio"]},
    {"cat": "corporate-finance", "slug": "revenue", "tools": [], "terms": ["net-income", "gross-profit", "top-line"]},
    {"cat": "corporate-finance", "slug": "net-income", "tools": [], "terms": ["revenue", "eps", "profit-margin"]},
    {"cat": "corporate-finance", "slug": "profit-margin", "tools": ["profit-margin"], "terms": ["gross-margin", "operating-margin", "net-income"]},
    {"cat": "corporate-finance", "slug": "gross-margin", "tools": ["profit-margin"], "terms": ["profit-margin", "cogs", "revenue"]},
    {"cat": "corporate-finance", "slug": "debt-to-equity", "tools": [], "terms": ["leverage", "balance-sheet", "financial-health"]},
    {"cat": "corporate-finance", "slug": "current-ratio", "tools": [], "terms": ["quick-ratio", "liquidity", "working-capital"]},
    {"cat": "corporate-finance", "slug": "working-capital", "tools": [], "terms": ["current-ratio", "cash-flow", "accounts-receivable"]},
    {"cat": "corporate-finance", "slug": "wacc", "tools": ["dcf-calculator"], "terms": ["discount-rate", "cost-of-equity", "cost-of-debt"]},
    {"cat": "corporate-finance", "slug": "dcf", "tools": ["dcf-calculator"], "terms": ["free-cash-flow", "discount-rate", "intrinsic-value"]},

    # ── 創業商務 (10) ──
    {"cat": "business", "slug": "break-even-point", "tools": ["break-even"], "terms": ["fixed-costs", "variable-costs", "contribution-margin"]},
    {"cat": "business", "slug": "fixed-costs", "tools": ["break-even"], "terms": ["variable-costs", "break-even-point", "overhead"]},
    {"cat": "business", "slug": "variable-costs", "tools": ["break-even"], "terms": ["fixed-costs", "break-even-point", "marginal-cost"]},
    {"cat": "business", "slug": "burn-rate", "tools": ["startup-cost-estimator"], "terms": ["runway", "cash-flow", "startup-funding"]},
    {"cat": "business", "slug": "runway", "tools": ["startup-cost-estimator"], "terms": ["burn-rate", "funding-round", "break-even-point"]},
    {"cat": "business", "slug": "seed-funding", "tools": ["startup-valuation"], "terms": ["series-a", "angel-investor", "valuation"]},
    {"cat": "business", "slug": "series-a", "tools": ["startup-valuation"], "terms": ["seed-funding", "venture-capital", "valuation"]},
    {"cat": "business", "slug": "valuation", "tools": ["startup-valuation"], "terms": ["pe-ratio", "dcf", "revenue-multiple"]},
    {"cat": "business", "slug": "angel-investor", "tools": [], "terms": ["seed-funding", "venture-capital", "equity"]},
    {"cat": "business", "slug": "venture-capital", "tools": [], "terms": ["series-a", "angel-investor", "ipo"]},

    # ── 外匯 (15) ──
    {"cat": "forex", "slug": "forex", "tools": ["currency-converter"], "terms": ["exchange-rate", "pip", "lot-size"]},
    {"cat": "forex", "slug": "pip", "tools": ["pip-value"], "terms": ["forex", "spread", "lot-size"]},
    {"cat": "forex", "slug": "lot-size", "tools": ["pip-value"], "terms": ["pip", "micro-lot", "standard-lot"]},
    {"cat": "forex", "slug": "spread", "tools": ["pip-value"], "terms": ["pip", "bid-ask-spread", "forex"]},
    {"cat": "forex", "slug": "carry-trade", "tools": [], "terms": ["interest-rate-differential", "forex", "leverage"]},
    {"cat": "forex", "slug": "currency-pair", "tools": ["currency-converter"], "terms": ["forex", "base-currency", "quote-currency"]},
    {"cat": "forex", "slug": "base-currency", "tools": ["currency-converter"], "terms": ["quote-currency", "currency-pair", "exchange-rate"]},
    {"cat": "forex", "slug": "forex-leverage", "tools": ["margin-calculator"], "terms": ["margin-trading", "leverage", "margin-call"]},
    {"cat": "forex", "slug": "forward-contract", "tools": [], "terms": ["futures-contract", "hedging", "exchange-rate"]},
    {"cat": "forex", "slug": "futures-contract", "tools": [], "terms": ["forward-contract", "options", "derivatives"]},
    {"cat": "forex", "slug": "options", "tools": ["options-profit"], "terms": ["call-option", "put-option", "derivatives"]},
    {"cat": "forex", "slug": "call-option", "tools": ["options-profit"], "terms": ["put-option", "strike-price", "premium"]},
    {"cat": "forex", "slug": "put-option", "tools": ["options-profit"], "terms": ["call-option", "strike-price", "hedging"]},
    {"cat": "forex", "slug": "strike-price", "tools": ["options-profit"], "terms": ["call-option", "put-option", "intrinsic-value"]},
    {"cat": "forex", "slug": "derivatives", "tools": [], "terms": ["options", "futures-contract", "forward-contract"]},

    # ── 加密貨幣 (15) ──
    {"cat": "crypto", "slug": "blockchain", "tools": [], "terms": ["cryptocurrency", "decentralization", "consensus-mechanism"]},
    {"cat": "crypto", "slug": "cryptocurrency", "tools": [], "terms": ["blockchain", "bitcoin", "altcoin"]},
    {"cat": "crypto", "slug": "bitcoin", "tools": [], "terms": ["cryptocurrency", "blockchain", "mining"]},
    {"cat": "crypto", "slug": "mining", "tools": [], "terms": ["proof-of-work", "hash-rate", "blockchain"]},
    {"cat": "crypto", "slug": "staking", "tools": [], "terms": ["proof-of-stake", "yield-farming", "defi"]},
    {"cat": "crypto", "slug": "defi", "tools": [], "terms": ["staking", "yield-farming", "smart-contract"]},
    {"cat": "crypto", "slug": "smart-contract", "tools": [], "terms": ["defi", "ethereum", "blockchain"]},
    {"cat": "crypto", "slug": "gas-fee", "tools": [], "terms": ["ethereum", "transaction-fee", "blockchain"]},
    {"cat": "crypto", "slug": "cold-wallet", "tools": [], "terms": ["hot-wallet", "private-key", "security"]},
    {"cat": "crypto", "slug": "hot-wallet", "tools": [], "terms": ["cold-wallet", "exchange", "private-key"]},
    {"cat": "crypto", "slug": "nft", "tools": [], "terms": ["blockchain", "smart-contract", "digital-asset"]},
    {"cat": "crypto", "slug": "altcoin", "tools": [], "terms": ["bitcoin", "cryptocurrency", "market-cap"]},
    {"cat": "crypto", "slug": "stablecoin", "tools": [], "terms": ["cryptocurrency", "peg", "defi"]},
    {"cat": "crypto", "slug": "tokenomics", "tools": [], "terms": ["cryptocurrency", "supply-and-demand", "market-cap"]},
    {"cat": "crypto", "slug": "proof-of-stake", "tools": [], "terms": ["proof-of-work", "staking", "consensus-mechanism"]},

    # ── 數學統計 (10) ──
    {"cat": "math-stats", "slug": "variance", "tools": [], "terms": ["standard-deviation", "mean", "normal-distribution"]},
    {"cat": "math-stats", "slug": "normal-distribution", "tools": [], "terms": ["standard-deviation", "mean", "confidence-interval"]},
    {"cat": "math-stats", "slug": "confidence-interval", "tools": [], "terms": ["normal-distribution", "sample-size", "margin-of-error"]},
    {"cat": "math-stats", "slug": "median", "tools": [], "terms": ["mean", "mode", "percentile"]},
    {"cat": "math-stats", "slug": "mean", "tools": [], "terms": ["median", "mode", "weighted-average"]},
    {"cat": "math-stats", "slug": "percentile", "tools": [], "terms": ["median", "quartile", "normal-distribution"]},
    {"cat": "math-stats", "slug": "regression-analysis", "tools": [], "terms": ["correlation", "r-squared", "linear-regression"]},
    {"cat": "math-stats", "slug": "r-squared", "tools": [], "terms": ["regression-analysis", "correlation", "goodness-of-fit"]},
    {"cat": "math-stats", "slug": "compound-annual-growth", "tools": ["cagr"], "terms": ["cagr", "annual-return", "geometric-mean"]},
    {"cat": "math-stats", "slug": "weighted-average", "tools": ["average-down"], "terms": ["mean", "portfolio-weighting", "average-down"]},
]

CATEGORY_NAMES = {
    "investment-basics": {"zh-TW": "投資基礎", "en": "Investment Basics", "ja": "投資の基礎", "ko": "투자 기초",
                          "de": "Anlage-Grundlagen", "fr": "Bases de l'investissement", "es": "Fundamentos de inversión",
                          "pt": "Fundamentos de investimento", "id": "Dasar Investasi", "zh-CN": "投资基础"},
    "stock-trading": {"zh-TW": "股票交易", "en": "Stock Trading", "ja": "株式取引", "ko": "주식 거래",
                      "de": "Aktienhandel", "fr": "Trading d'actions", "es": "Trading de acciones",
                      "pt": "Negociação de ações", "id": "Perdagangan Saham", "zh-CN": "股票交易"},
    "technical-analysis": {"zh-TW": "技術分析", "en": "Technical Analysis", "ja": "テクニカル分析", "ko": "기술적 분석",
                           "de": "Technische Analyse", "fr": "Analyse technique", "es": "Análisis técnico",
                           "pt": "Análise técnica", "id": "Analisis Teknikal", "zh-CN": "技术分析"},
    "bonds": {"zh-TW": "債券固收", "en": "Bonds & Fixed Income", "ja": "債券", "ko": "채권",
              "de": "Anleihen", "fr": "Obligations", "es": "Bonos", "pt": "Títulos", "id": "Obligasi", "zh-CN": "债券固收"},
    "funds-etf": {"zh-TW": "基金 ETF", "en": "Funds & ETFs", "ja": "ファンド・ETF", "ko": "펀드·ETF",
                  "de": "Fonds & ETFs", "fr": "Fonds & ETFs", "es": "Fondos y ETFs",
                  "pt": "Fundos e ETFs", "id": "Dana & ETF", "zh-CN": "基金ETF"},
    "real-estate": {"zh-TW": "房地產", "en": "Real Estate", "ja": "不動産", "ko": "부동산",
                    "de": "Immobilien", "fr": "Immobilier", "es": "Bienes raíces",
                    "pt": "Imóveis", "id": "Properti", "zh-CN": "房地产"},
    "loans-credit": {"zh-TW": "貸款信用", "en": "Loans & Credit", "ja": "ローン・クレジット", "ko": "대출·신용",
                     "de": "Kredite", "fr": "Prêts & Crédit", "es": "Préstamos y crédito",
                     "pt": "Empréstimos e crédito", "id": "Pinjaman & Kredit", "zh-CN": "贷款信用"},
    "insurance": {"zh-TW": "保險", "en": "Insurance", "ja": "保険", "ko": "보험",
                  "de": "Versicherung", "fr": "Assurance", "es": "Seguros",
                  "pt": "Seguros", "id": "Asuransi", "zh-CN": "保险"},
    "tax": {"zh-TW": "稅務", "en": "Tax", "ja": "税金", "ko": "세금",
            "de": "Steuern", "fr": "Fiscalité", "es": "Impuestos",
            "pt": "Impostos", "id": "Pajak", "zh-CN": "税务"},
    "retirement": {"zh-TW": "退休規劃", "en": "Retirement Planning", "ja": "退職計画", "ko": "은퇴 계획",
                   "de": "Altersvorsorge", "fr": "Retraite", "es": "Jubilación",
                   "pt": "Aposentadoria", "id": "Pensiun", "zh-CN": "退休规划"},
    "macro": {"zh-TW": "總體經濟", "en": "Macroeconomics", "ja": "マクロ経済", "ko": "거시경제",
              "de": "Makroökonomie", "fr": "Macroéconomie", "es": "Macroeconomía",
              "pt": "Macroeconomia", "id": "Ekonomi Makro", "zh-CN": "宏观经济"},
    "risk-management": {"zh-TW": "風險管理", "en": "Risk Management", "ja": "リスク管理", "ko": "위험 관리",
                        "de": "Risikomanagement", "fr": "Gestion des risques", "es": "Gestión de riesgos",
                        "pt": "Gestão de riscos", "id": "Manajemen Risiko", "zh-CN": "风险管理"},
    "corporate-finance": {"zh-TW": "企業財務", "en": "Corporate Finance", "ja": "企業財務", "ko": "기업 재무",
                          "de": "Unternehmensfinanzierung", "fr": "Finance d'entreprise", "es": "Finanzas corporativas",
                          "pt": "Finanças corporativas", "id": "Keuangan Perusahaan", "zh-CN": "企业财务"},
    "business": {"zh-TW": "創業商務", "en": "Business & Startups", "ja": "ビジネス・起業", "ko": "비즈니스·창업",
                 "de": "Unternehmensgründung", "fr": "Entrepreneuriat", "es": "Emprendimiento",
                 "pt": "Empreendedorismo", "id": "Bisnis & Startup", "zh-CN": "创业商务"},
    "forex": {"zh-TW": "外匯", "en": "Forex", "ja": "外国為替", "ko": "외환",
              "de": "Devisenhandel", "fr": "Forex", "es": "Forex",
              "pt": "Câmbio", "id": "Forex", "zh-CN": "外汇"},
    "crypto": {"zh-TW": "加密貨幣", "en": "Cryptocurrency", "ja": "暗号資産", "ko": "암호화폐",
               "de": "Kryptowährung", "fr": "Cryptomonnaie", "es": "Criptomonedas",
               "pt": "Criptomoedas", "id": "Kripto", "zh-CN": "加密货币"},
    "math-stats": {"zh-TW": "數學統計", "en": "Math & Statistics", "ja": "数学・統計", "ko": "수학·통계",
                   "de": "Mathematik & Statistik", "fr": "Maths & Statistiques", "es": "Matemáticas y estadística",
                   "pt": "Matemática e estatística", "id": "Matematika & Statistik", "zh-CN": "数学统计"},
}

print(f"Total terms defined: {len(GLOSSARY_TERMS)}")

# ── URL / Path helpers ──────────────────────────────

def glossary_url(slug, lang):
    if lang == "zh-TW":
        return f"/glossary/{slug}.html"
    return f"/glossary/{lang}/{slug}.html"

def glossary_path(slug, lang):
    if lang == "zh-TW":
        return OUTPUT_DIR / f"{slug}.html"
    return OUTPUT_DIR / lang / f"{slug}.html"

def tool_url(slug, lang):
    if lang == "zh-TW":
        return f"/tools/{slug}.html"
    return f"/tools/{lang}/{slug}.html"

def build_hreflang(slug):
    tags = []
    for l in LANGS:
        url = f"https://softglow-ai.com{glossary_url(slug, l)}"
        tags.append(f'<link rel="alternate" hreflang="{LANG_CODES[l]}" href="{url}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com{glossary_url(slug, "en")}">')
    return "\n".join(tags)

def build_lang_switcher(slug, current_lang):
    options = []
    for l in LANGS:
        sel = " selected" if l == current_lang else ""
        options.append(f'<option value="{glossary_url(slug, l)}"{sel}>{LANG_NAMES[l]}</option>')
    return '<select class="lang-select" onchange="location.href=this.value">' + "".join(options) + '</select>'

# ── API 呼叫 ──────────────────────────────────────

def call_api(slug, lang, cat):
    import requests
    cat_name = CATEGORY_NAMES.get(cat, {}).get(lang, cat)

    lang_instructions = {
        "zh-TW": "用繁體中文撰寫。金額格式 $1,234,567。日期 2026/07/17。使用台灣常用金融術語。",
        "en": "Write in English. Currency $1,234,567.89. Date Jul 17, 2026. Use US financial conventions.",
        "ja": "日本語で書いてください。金額 ¥1,234,567。日付 2026年7月17日。日本の金融用語を使用。",
        "ko": "한국어로 작성하세요. 금액 ₩1,234,567. 날짜 2026. 07. 17. 한국 금융 용어 사용.",
        "de": "Auf Deutsch schreiben. Währung 1.234.567,89 €. Datum 17.07.2026. Deutsche Finanzterminologie.",
        "fr": "Écrire en français. Devise 1 234 567,89 €. Date 17/07/2026. Terminologie financière française.",
        "es": "Escribir en español. Moneda 1.234.567,89 €. Fecha 17/07/2026. Terminología financiera española.",
        "pt": "Escrever em português. Moeda R$ 1.234.567,89. Data 17/07/2026. Terminologia financeira brasileira.",
        "id": "Tulis dalam Bahasa Indonesia. Mata uang Rp 1.234.567,89. Tanggal 17-07-2026.",
        "zh-CN": "用简体中文撰写。金额 ¥1,234,567。日期 2026年7月17日。使用中国大陆金融术语。",
    }

    is_cjk = lang in ("zh-TW", "zh-CN", "ja", "ko")
    word_target = "800-1000 characters" if is_cjk else "1200-1500 words"

    prompt = f"""You are a financial education writer. Write a glossary entry for the term "{slug}" (category: {cat_name}).

{lang_instructions.get(lang, lang_instructions["en"])}

Return ONLY valid JSON with these keys (no markdown, no backticks):
{{
  "term_name": "localized term name",
  "seo_title": "SEO page title - {('25-30 chars' if is_cjk else '55-60 chars')}, pure search intent, include the term",
  "seo_desc": "meta description, 120-155 chars, mention related concepts",
  "one_line": "one sentence definition, clear and concise",
  "explanation": "detailed explanation covering definition, context, and why it matters. 250+ words or 400+ CJK chars",
  "example": "concrete calculation or real-world example with actual numbers. 200+ words or 300+ CJK chars",
  "application": "practical use cases, when and how to use this concept. 200+ words or 300+ CJK chars",
  "mistakes": "common mistakes or misconceptions, what beginners get wrong. 150+ words or 200+ CJK chars",
  "comparison": "HTML table comparing this term with a commonly confused similar term. Use <table><thead><tr><th>...</th></tr></thead><tbody>...</tbody></table> format. 3-5 comparison dimensions.",
  "faq": [
    {{"q": "question 1", "a": "detailed answer 1 (50+ words)"}},
    {{"q": "question 2", "a": "detailed answer 2 (50+ words)"}},
    {{"q": "question 3", "a": "detailed answer 3 (50+ words)"}},
    {{"q": "question 4", "a": "detailed answer 4 (50+ words)"}},
    {{"q": "question 5", "a": "detailed answer 5 (50+ words)"}}
  ]
}}

Total content should be {word_target} (excluding HTML tags). Write educational, authoritative content. Do NOT include any markdown formatting."""

    headers = {
        "x-api-key": API_KEY,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    body = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}]
    }

    for attempt in range(3):
        try:
            resp = requests.post("https://api.anthropic.com/v1/messages",
                                 headers=headers, json=body, timeout=60)
            if resp.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                print(f"  API error {resp.status_code}: {resp.text[:200]}")
                time.sleep(5)
                continue

            text = resp.json()["content"][0]["text"].strip()
            # Fix truncated JSON
            text = fix_json(text)
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}")
            time.sleep(3)
        except Exception as e:
            print(f"  Request error: {e}")
            time.sleep(5)
    return None


def fix_json(text):
    """Fix truncated or wrapped JSON from API response."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r'^```\w*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
        text = text.strip()
    # Find outermost braces
    start = text.find('{')
    if start == -1:
        return text
    depth = 0
    end = -1
    for i in range(start, len(text)):
        if text[i] == '{': depth += 1
        elif text[i] == '}': depth -= 1
        if depth == 0:
            end = i
            break
    if end == -1:
        # Truncated - try to close it
        text = text + ']}' * 3 + '}'
        depth = 0
        for i in range(start, len(text)):
            if text[i] == '{': depth += 1
            elif text[i] == '}': depth -= 1
            if depth == 0:
                end = i
                break
    return text[start:end+1] if end > start else text


# ── HTML 生成 ──────────────────────────────────────

def build_html(term, lang, data):
    slug = term["slug"]
    cat = term["cat"]
    labels = LANG_LABELS[lang]
    cat_name = CATEGORY_NAMES.get(cat, {}).get(lang, cat)

    # Related terms links
    related_terms_html = ""
    for t in term.get("terms", [])[:5]:
        url = glossary_url(t, lang)
        related_terms_html += f'<a class="tool-pill" href="{url}">{t.replace("-", " ").title()}</a>\n'

    # Related tools links
    related_tools_html = ""
    for t in term.get("tools", [])[:5]:
        url = tool_url(t, lang)
        related_tools_html += f'<a class="tool-pill" href="{url}">{t.replace("-", " ").title()}</a>\n'

    # FAQ HTML + Schema
    faq_html = ""
    faq_schema_entries = []
    for item in data.get("faq", []):
        q = item.get("q", "")
        a = item.get("a", "")
        faq_html += f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>\n'
        faq_schema_entries.append({"@type": "Question", "name": q,
                                   "acceptedAnswer": {"@type": "Answer", "text": a}})

    faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                              "mainEntity": faq_schema_entries}, ensure_ascii=False)

    # Lottery banner lang
    lottery_langs = {"zh-TW": "zh-TW", "ja": "ja", "ko": "ko", "en": "en",
                     "de": "en", "fr": "en", "es": "en", "pt": "en", "id": "en", "zh-CN": "zh-TW"}
    lottery_l = lottery_langs.get(lang, "en")

    canonical = f"https://softglow-ai.com{glossary_url(slug, lang)}"
    page_lang = LANG_CODES[lang]

    html = f'''<!DOCTYPE html>
<html lang="{page_lang}">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://securepubads.g.doubleclick.net">
<link rel="preconnect" href="https://pagead2.googlesyndication.com">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data.get("seo_title", slug)}</title>
<meta name="description" content="{data.get("seo_desc", "")}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{build_hreflang(slug)}
<script type="application/ld+json">{faq_schema}</script>
<link rel="stylesheet" href="/tools/tools.css">
<link rel="stylesheet" href="/common/softglow-common.css">
<meta name="sg-slug" content="{slug}">
<meta name="sg-type" content="glossary">
<meta name="sg-lang" content="{lang}">
<link rel="stylesheet" href="/js/cookie-consent.css">
</head>
<body>
<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="/glossary/{'' if lang == 'zh-TW' else lang + '/'}">{labels["glossary"]}</a>
    <a href="/tools/{'' if lang == 'zh-TW' else lang + '/'}">{labels["tools"]}</a>
    <a href="/blog/">{labels["blog"]}</a>
    <a href="/">{labels["home"]}</a>
  </div>
  <div class="nav-actions">
    {build_lang_switcher(slug, lang)}
    <button class="act-btn primary" onclick="sgOpenSearch()" title="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="act-btn primary" id="sgBmBtn" onclick="sgToggleBookmark()" ondblclick="sgToggleBmPanel()" title="Bookmark"><svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></button>
  </div>
</div>
</nav>
<div class="breadcrumb"><a href="/">{labels["home"]}</a> &gt; <a href="/glossary/{'' if lang == 'zh-TW' else lang + '/'}">{labels["glossary"]}</a> &gt; {data.get("term_name", slug)}</div>
<div class="container">
<div class="layout">
<div class="main">

  <div class="calc-card">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
      <span style="background:#EBF5FF;color:#2563EB;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600">{cat_name}</span>
    </div>
    <h1>{data.get("term_name", slug)}</h1>
    <p class="calc-subtitle" style="font-size:16px;line-height:1.7;color:#2D3748;font-weight:500;margin-top:12px">{data.get("one_line", "")}</p>
  </div>

  <div class="ad-container ad-container-lg" id="ad-calc"><ins class="adsbygoogle" style="min-width:160px;min-height:250px;display:block;min-height:250px;" data-ad-client="ca-pub-1768270548115739" data-ad-slot="4182262477" data-ad-format="auto" data-full-width-responsive="true"></ins></div>

  <article class="article">
    <h2>{data.get("term_name", slug)}</h2>
    <p>{data.get("explanation", "")}</p>

    <h2>{"計算範例" if lang in ("zh-TW", "zh-CN") else "Example" if lang == "en" else "例"}</h2>
    <p>{data.get("example", "")}</p>

    <h2>{"實戰應用" if lang in ("zh-TW", "zh-CN") else "Practical Application" if lang == "en" else "応用"}</h2>
    <p>{data.get("application", "")}</p>
  </article>

  <div class="ad-container" id="ad-mid"><ins class="adsbygoogle" style="min-width:160px;min-height:250px;display:block;text-align:center;min-height:100px;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-1768270548115739" data-ad-slot="2793159185"></ins></div>

  <article class="article">
    <h2>{"常見錯誤" if lang in ("zh-TW", "zh-CN") else "Common Mistakes" if lang == "en" else "よくある間違い"}</h2>
    <p>{data.get("mistakes", "")}</p>

    <h2>{"比較表" if lang in ("zh-TW", "zh-CN") else "Comparison" if lang == "en" else "比較"}</h2>
    {data.get("comparison", "")}
  </article>

  <div style="margin:20px 0;padding:16px 20px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:12px;text-align:center"><a href="https://lottery.softglow-ai.com/{lottery_l}/" target="_blank" rel="noopener" style="text-decoration:none;color:#fff"><div style="font-size:16px;font-weight:700;margin-bottom:4px">🎰 Global Lottery Results + Smart Number Picker</div><div style="font-size:12px;opacity:0.9">Powerball · Mega Millions · EuroMillions — 12 ways to pick numbers</div></a></div>

  <section class="faq">
    <h2>{labels["faq_title"]}</h2>
    {faq_html}
  </section>

  {"" if not related_tools_html else f'<div class="more-tools"><h3>{labels["related_tools"]}</h3><div class="tools-grid">{related_tools_html}</div></div>'}
  {"" if not related_terms_html else f'<div class="more-tools"><h3>{labels["related_terms"]}</h3><div class="tools-grid">{related_terms_html}</div></div>'}

  <div class="ad-container ad-container-lg" id="ad-bottom"><ins class="adsbygoogle" style="min-width:160px;min-height:250px;display:block;min-height:250px;" data-ad-client="ca-pub-1768270548115739" data-ad-slot="4182262477" data-ad-format="auto" data-full-width-responsive="true"></ins></div>

</div>
<aside class="sidebar">
  <div class="ad-container ad-container-lg" id="ad-side"><ins class="adsbygoogle" style="min-width:160px;min-height:250px;display:block;min-height:250px;" data-ad-client="ca-pub-1768270548115739" data-ad-slot="1655301946" data-ad-format="auto" data-full-width-responsive="true"></ins></div>
  <div class="related-card"><h3>{labels["related_terms"]}</h3></div>
  <div class="ad-container" id="ad-side2"><ins class="adsbygoogle" style="min-width:160px;min-height:250px;display:block;text-align:center;min-height:100px;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-1768270548115739" data-ad-slot="2793159185"></ins></div>
</aside>
</div></div>
<footer class="footer"><div class="footer-inner"><a href="/about.html">About</a><a href="/contact.html">Contact</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a><span style="margin-left:auto">&copy; 2026 SoftGlow</span></div></footer>
<script>
document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{this.parentElement.classList.toggle('open');}});}});
</script>
<script>
setTimeout(function(){{var s=document.createElement('script');s.async=true;s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739';s.crossOrigin='anonymous';document.head.appendChild(s);s.onload=function(){{document.querySelectorAll('ins.adsbygoogle').forEach(function(ad){{if(ad.offsetWidth>0){{try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}}}}});}}}},2000);
</script>
<div class="search-overlay" id="sgSearchOverlay">
  <div class="search-box">
    <div class="search-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input class="search-input" id="sgSearchInput" type="text" placeholder="Search..." autocomplete="off">
    </div>
    <div class="search-results" id="sgSearchResults"></div>
  </div>
</div>
<div class="bm-panel" id="sgBmPanel">
  <div class="bm-header"><h3>Bookmarks</h3><button class="bm-clear" onclick="window._sgClearBm()">Clear All</button></div>
  <div class="bm-list" id="sgBmList"></div>
</div>
<script src="/common/softglow-common.js"></script>
<script src="/js/softglow-cookies.js" defer></script>
</body>
</html>

<!-- {VERSION}|{lang}|{slug}|{BUILD_DATE} -->
'''
    return html


# ── 主程式 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SoftGlow Glossary Generator")
    parser.add_argument("--langs", default=",".join(LANGS), help="Comma-separated langs")
    parser.add_argument("--start", type=int, default=0, help="Start from term index")
    parser.add_argument("--limit", type=int, default=0, help="Max terms to process (0=all)")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without calling API")
    args = parser.parse_args()

    if not API_KEY and not args.dry_run:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    langs = [l.strip() for l in args.langs.split(",")]
    terms = GLOSSARY_TERMS[args.start:]
    if args.limit > 0:
        terms = terms[:args.limit]

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for lang in langs:
        (OUTPUT_DIR / lang).mkdir(parents=True, exist_ok=True)

    total = len(terms) * len(langs)
    print(f"\n{'='*60}")
    print(f"SoftGlow Glossary Generator {VERSION}")
    print(f"Terms: {len(terms)} | Langs: {len(langs)} | Total pages: {total}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    if args.dry_run:
        for i, term in enumerate(terms):
            print(f"  [{i+args.start:3d}] {term['slug']} ({term['cat']})")
        print(f"\nDry run complete. {total} pages would be generated.")
        return

    done = 0
    skipped = 0
    errors = 0

    for i, term in enumerate(terms):
        slug = term["slug"]
        for lang in langs:
            cache_file = CACHE_DIR / f"{slug}_{lang}.json"
            out_file = glossary_path(slug, lang)

            # Check cache
            if cache_file.exists() and out_file.exists():
                skipped += 1
                continue

            # Check cache only (API done but HTML not built)
            data = None
            if cache_file.exists():
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except:
                    pass

            # Call API if needed
            if data is None:
                idx = i + args.start
                print(f"[{idx:3d}/{len(GLOSSARY_TERMS)}] {slug} ({lang}) ...", end=" ", flush=True)
                data = call_api(slug, lang, term["cat"])
                if data is None:
                    print("FAILED")
                    errors += 1
                    continue
                # Save cache
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("OK")
                time.sleep(0.5)  # Rate limit buffer

            # Build HTML
            html = build_html(term, lang, data)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(html)
            done += 1

    print(f"\n{'='*60}")
    print(f"Done: {done} | Skipped (cached): {skipped} | Errors: {errors}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    # Fix requests encoding issue on Windows
    try:
        import requests
        _orig = requests.models.Response.apparent_encoding.__get__
        requests.models.Response.apparent_encoding = property(lambda self: "utf-8")
    except:
        pass

    main()
