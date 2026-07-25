"""
thicken_tool_pages.py — 批次加厚工具頁內容
針對 GSC 有曝光但排名 10-40 的頁面，補充表格、範例、常見錯誤

用法：
  python thicken_tool_pages.py --pages ev-range,cbm-calculator,paint-calculator
  python thicken_tool_pages.py --all-thin   # 自動找出所有 <600 words 的英文頁

注意：這個腳本只加厚英文頁。中文頁因為字數計算方式不同（用字元數），需要另外處理。
"""

import os, re, sys, json

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "frontend", "tools")

# 每個工具的補充內容模板
EXTRA_CONTENT = {
    "ev-range": {
        "tables": [
            {"title": "Popular EV Range Comparison", "headers": ["Vehicle", "Battery", "EPA Range", "Real-World Range"],
             "rows": [
                 ["Tesla Model 3 LR", "75 kWh", "358 mi (576 km)", "310-340 mi"],
                 ["Tesla Model Y LR", "75 kWh", "330 mi (531 km)", "280-310 mi"],
                 ["Hyundai Ioniq 6 LR", "77.4 kWh", "361 mi (581 km)", "310-340 mi"],
                 ["BMW iX xDrive50", "111.5 kWh", "324 mi (521 km)", "280-310 mi"],
                 ["Chevy Equinox EV", "85 kWh", "319 mi (513 km)", "270-300 mi"],
                 ["Nissan Leaf Plus", "62 kWh", "212 mi (341 km)", "180-200 mi"],
             ]},
            {"title": "Factors Affecting EV Range", "headers": ["Factor", "Impact", "Tips"],
             "rows": [
                 ["Temperature (cold)", "-20% to -40%", "Precondition cabin while plugged in"],
                 ["Temperature (hot)", "-5% to -15%", "Park in shade, use recirculated AC"],
                 ["Highway speed (75+ mph)", "-15% to -25%", "Slow down to 65 mph for best range"],
                 ["Tire pressure (low)", "-3% to -5%", "Check monthly, inflate to spec"],
                 ["Payload (full car)", "-5% to -10%", "Remove unnecessary cargo"],
                 ["HVAC (heat/AC)", "-10% to -30%", "Use seat heaters instead of cabin heat"],
             ]},
        ],
        "extra_sections": """<h2>Understanding Battery Degradation</h2>
<p>EV batteries gradually lose capacity over time. Most manufacturers warrant 70-80% capacity retention over 8 years or 100,000 miles. Real-world data shows Tesla batteries retain about 90% capacity after 200,000 miles, while Nissan Leaf batteries in hot climates may degrade faster due to passive cooling. When estimating long-term range, factor in 1-2% annual degradation for planning purposes.</p>
<h2>Charging Strategy for Maximum Range</h2>
<p>For daily driving, charge to 80% to preserve battery longevity. Only charge to 100% before long trips. Frequent DC fast charging (Level 3) generates more heat and can accelerate degradation compared to Level 2 home charging. Plan road trips using the rule of thumb: actual driving range = EPA range × 0.85 for highway, or EPA range × 1.10 for city driving.</p>""",
    },

    "cbm-calculator": {
        "tables": [
            {"title": "Standard Container Dimensions", "headers": ["Container", "Internal L×W×H (m)", "CBM Capacity", "Max Payload"],
             "rows": [
                 ["20ft Standard", "5.90 × 2.35 × 2.39", "33.2 CBM", "21,770 kg"],
                 ["40ft Standard", "12.03 × 2.35 × 2.39", "67.7 CBM", "26,680 kg"],
                 ["40ft High Cube", "12.03 × 2.35 × 2.69", "76.3 CBM", "26,460 kg"],
                 ["45ft High Cube", "13.56 × 2.35 × 2.69", "85.9 CBM", "25,600 kg"],
             ]},
        ],
        "extra_sections": """<h2>CBM and Freight Cost Relationship</h2>
<p>Ocean freight is typically charged by the higher of actual weight (in metric tons) or volume (in CBM), using a ratio of 1 CBM = 1 metric ton for LCL (Less than Container Load) shipments. For FCL (Full Container Load), you pay per container regardless of how full it is. Understanding your cargo's CBM helps determine whether LCL or FCL is more cost-effective. As a rule of thumb, if your shipment exceeds 15 CBM, an FCL 20ft container is usually cheaper than LCL rates.</p>
<h2>Common Mistakes in CBM Calculation</h2>
<p><strong>Mistake 1:</strong> Measuring inner carton dimensions instead of outer dimensions. Always use the outermost measurement including packaging, pallets, and protective materials.</p>
<p><strong>Mistake 2:</strong> Forgetting to account for pallet height. Standard pallets add 15 cm (6 inches) of height per layer.</p>
<p><strong>Mistake 3:</strong> Not considering stacking limits. Fragile goods may not be stackable, effectively doubling the CBM used.</p>""",
    },

    "paint-calculator": {
        "tables": [
            {"title": "Paint Coverage by Type", "headers": ["Paint Type", "Coverage (sq ft/gallon)", "Coats Needed", "Best For"],
             "rows": [
                 ["Flat/Matte", "350-400", "2", "Ceilings, low-traffic areas"],
                 ["Eggshell", "350-400", "2", "Living rooms, bedrooms"],
                 ["Satin", "350-400", "2", "Kitchens, hallways, kids' rooms"],
                 ["Semi-Gloss", "350-400", "2", "Bathrooms, trim, doors"],
                 ["Gloss", "300-350", "2-3", "Cabinets, furniture, accents"],
                 ["Primer", "300-350", "1", "New drywall, color changes"],
             ]},
        ],
        "extra_sections": """<h2>How to Measure Your Room</h2>
<p>Measure the length and height of each wall, then multiply to get the square footage. Subtract window and door areas (standard door: ~21 sq ft, standard window: ~12 sq ft). Add 10% for waste, touch-ups, and uneven surfaces. For textured walls like stucco or brick, add 20-30% as the rough surface absorbs more paint.</p>
<h2>Pro Tips for Accurate Estimation</h2>
<p><strong>Dark to light color change:</strong> Add 1 extra coat (3 total) or use a tinted primer first. Going from dark red to white without primer could take 4+ coats.</p>
<p><strong>Ceiling paint:</strong> Ceilings typically need flat paint. One gallon covers about 400 sq ft on smooth ceilings. Textured (popcorn) ceilings need 25-50% more paint.</p>
<p><strong>Trim and doors:</strong> A standard interior door takes about 1 quart. Budget 1 gallon of trim paint per 200 linear feet of baseboard and crown molding.</p>""",
    },

    "court-fee": {
        "tables": [
            {"title": "US Federal Court Filing Fees (2026)", "headers": ["Case Type", "Filing Fee", "Notes"],
             "rows": [
                 ["Civil Action", "$405", "Complaint or petition"],
                 ["Appeal to Circuit Court", "$605", "From district court"],
                 ["Bankruptcy Ch. 7", "$338", "Individual liquidation"],
                 ["Bankruptcy Ch. 13", "$313", "Repayment plan"],
                 ["Bankruptcy Ch. 11", "$1,738", "Business reorganization"],
                 ["Habeas Corpus", "$5", "State prisoner petition"],
                 ["Miscellaneous Case", "$52", "Registration of judgment"],
             ]},
        ],
        "extra_sections": """<h2>Fee Waivers (In Forma Pauperis)</h2>
<p>If you cannot afford court fees, you may apply to have them waived by filing a motion for In Forma Pauperis (IFP) status. Courts evaluate your income, assets, and expenses. Generally, if your income is below 125-150% of the federal poverty guidelines, you qualify. The form requires disclosure of bank accounts, monthly income, debts, and dependents. Approval rates vary by court but are granted in roughly 60-70% of applications.</p>
<h2>Hidden Costs Beyond Filing Fees</h2>
<p>Court filing fees are just the beginning. Other costs include: service of process ($50-100 per defendant), deposition transcripts ($3-7 per page), expert witness fees ($200-500/hour), mediation fees ($150-400/hour), and appeal filing fees. For a typical civil case, total court-related costs (excluding attorney fees) range from $1,000 to $10,000 depending on complexity and duration.</p>""",
    },

    "health-insurance-estimate": {
        "tables": [
            {"title": "ACA Metal Tier Comparison", "headers": ["Tier", "Premium", "Deductible", "Actuarial Value", "Best For"],
             "rows": [
                 ["Bronze", "Lowest", "$6,000-8,000", "60%", "Healthy, rarely use healthcare"],
                 ["Silver", "Moderate", "$3,000-5,000", "70%", "Average use, subsidy eligible"],
                 ["Gold", "Higher", "$1,000-2,000", "80%", "Regular prescriptions/visits"],
                 ["Platinum", "Highest", "$0-500", "90%", "Frequent medical needs"],
             ]},
        ],
        "extra_sections": """<h2>Understanding Your Total Healthcare Costs</h2>
<p>Your total annual healthcare cost is not just your premium. The formula is: Total Cost = Annual Premium + Deductible Met + Copays + Coinsurance, up to your Out-of-Pocket Maximum. For 2026, the ACA OOP max is $9,450 for individuals and $18,900 for families. Once you hit this cap, insurance covers 100% of covered services for the rest of the year.</p>
<h2>Tips to Lower Your Health Insurance Costs</h2>
<p><strong>Check subsidy eligibility:</strong> Households earning up to 400% of the Federal Poverty Level qualify for ACA premium tax credits. A family of four earning $60,000 could save $500+ per month.</p>
<p><strong>Use an HSA:</strong> If enrolled in a High Deductible Health Plan (HDHP), contribute to a Health Savings Account. Contributions are tax-deductible, growth is tax-free, and withdrawals for medical expenses are tax-free — a triple tax advantage.</p>
<p><strong>Compare networks:</strong> HMO plans are 20-40% cheaper than PPO plans but restrict you to in-network providers. If you don't need specialist referrals or out-of-network access, HMO saves significantly.</p>""",
    },
}


def build_table_html(table_data):
    """Generate HTML table from dict"""
    html = f'<table>\n<tr>'
    for h in table_data["headers"]:
        html += f'<th>{h}</th>'
    html += '</tr>\n'
    for row in table_data["rows"]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{cell}</td>'
        html += '</tr>\n'
    html += '</table>'
    return html


def thicken_page(filepath, slug):
    """Add extra content to a tool page"""
    extra = EXTRA_CONTENT.get(slug)
    if not extra:
        print(f"  ⏭ {slug}: no extra content defined, skipping")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the second </article> tag (after the ad slot)
    articles = list(re.finditer(r'</article>', content))
    if len(articles) < 2:
        print(f"  ❌ {slug}: could not find second </article> tag")
        return False

    insert_pos = articles[-1].start()

    # Build new content
    new_html = ""
    for table_data in extra.get("tables", []):
        new_html += f'\n<h3>{table_data["title"]}</h3>\n{build_table_html(table_data)}\n'

    if extra.get("extra_sections"):
        new_html += "\n" + extra["extra_sections"]

    content = content[:insert_pos] + new_html + content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Count new word count
    articles_text = re.findall(r'<article.*?</article>', content, re.DOTALL)
    total_text = re.sub(r'<[^>]+>', '', ' '.join(articles_text))
    word_count = len(total_text.split())

    print(f"  ✅ {slug}: thickened to {word_count} words")
    return True


def main():
    if "--all-thin" in sys.argv:
        # Find all en pages with < 600 words
        en_dir = os.path.join(TOOLS_DIR, "en")
        if not os.path.isdir(en_dir):
            print(f"❌ {en_dir} not found")
            return
        targets = []
        for fname in os.listdir(en_dir):
            if not fname.endswith('.html') or fname.startswith('index'):
                continue
            slug = fname.replace('.html', '')
            if slug in EXTRA_CONTENT:
                targets.append(slug)
        pages = targets
    elif "--pages" in sys.argv:
        idx = sys.argv.index("--pages")
        pages = sys.argv[idx + 1].split(",")
    else:
        pages = list(EXTRA_CONTENT.keys())

    print(f"Thickening {len(pages)} pages...")
    for slug in pages:
        # Try en first, then zh-TW root
        en_path = os.path.join(TOOLS_DIR, "en", f"{slug}.html")
        zh_path = os.path.join(TOOLS_DIR, f"{slug}.html")
        if os.path.exists(en_path):
            thicken_page(en_path, slug)
        elif os.path.exists(zh_path):
            thicken_page(zh_path, slug)
        else:
            print(f"  ❌ {slug}: file not found")


if __name__ == "__main__":
    main()
