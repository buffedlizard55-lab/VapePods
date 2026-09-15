#!/usr/bin/env python3
"""
Build script for the VapePods GitHub Pages site.
All entries below were verified on 2026-09-14 from official store sites
(server-rendered pages) or the official sites' search indexes (flagged as such).
No data is invented; anything not directly verifiable is explicitly flagged.
"""
import json, math, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "site")
os.makedirs(SITE, exist_ok=True)

VERIFIED_DATE = "2026-09-14"

# Reference point: Sunset Pipeline, 2161 Irving St, SF 94122 (user's area).
# Coordinates from official listing data captured during research.
REF = (37.7631407, -122.4811240)

def haversine_miles(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))

# ---------------------------------------------------------------------------
# STORES (all addresses/hours from official store sites unless noted)
# ---------------------------------------------------------------------------
stores = [
    {
        "name": "Sunset Pipeline",
        "group": "Pipeline Dispensaries (Portola Pipeline Cannabis)",
        "address": "2161 Irving St, San Francisco, CA 94122",
        "zip": "94122",
        "phone": "(415) 571-8575",
        "hours": "Daily 8:00 AM - 10:00 PM",
        "url": "https://www.pipelinedispensary.com/location/sunset-pipeline/",
        "menu_url": "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary",
        "specials_url": "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/specials",
        "lat": REF[0], "lon": REF[1],
        "tax_note": "Prices shown are BEFORE tax. Product pages state: '*Sales tax will be added at checkout.'",
        "source_status": "Official store site (pipelinedispensary.com) - live-fetched 2026-09-14",
        "deals": [
            "30% OFF STIIIZY PODS & ALL-IN-ONE VAPES (sale page lists 15 STIIIZY products at sale prices)",
            "30% off select Pipeline Cannabis 7g & 14g flower",
            "10% off CAKE all-in-one vapes",
            "20% off Northern Harvest prerolls",
            "40% off all Humboldt Grower's Network prerolls (Sunset only)",
            "Munchie Mondays: 20% off all Kahna gummies",
        ],
    },
    {
        "name": "STIIIZY Parkmerced",
        "group": "STIIIZY retail (the 'Stiiizy at Stonestown' store)",
        "address": "61 Cambon Dr, San Francisco, CA 94132",
        "zip": "94132",
        "phone": "(628) 216-5717",
        "hours": "Daily 7:00 AM - 9:45 PM",
        "url": "https://www.stiiizy.com/pages/stiiizy-parkmerced",
        "menu_url": "https://stiiizy.dispensary.shop/parkmerced/rec/menu",
        "specials_url": "https://www.stiiizy.com/pages/stiiizy-parkmerced",
        "lat": 37.7288, "lon": -122.4755,
        "tax_note": "In-store POS applies CA taxes; Stiiizy D2C prices are tax-included (see STIIIZY Delivery store).",
        "source_status": "Official stiiizy.com store page - live-fetched 2026-09-14. License C10-0000825-LIC listed on page. Opened July 1, 2023.",
        "deals": [
            "Weekly deals + daily deals (Mon-Sun) posted on store page as image assets (manual review)",
            "'Discounted menu and special ounce deals' link on store page (linktree) was DOWN at verification time - flag",
            "Official live in-store menu (stiiizy.dispensary.shop) is a JS app - per-product prices not machine-verifiable; use link for manual review",
        ],
    },
    {
        "name": "Urbana - Geary",
        "group": "Urbana Dispensaries",
        "address": "4811 Geary Blvd, San Francisco, CA 94118",
        "zip": "94118",
        "phone": "(415) 702-6767",
        "hours": "Daily 10:00 AM - 9:00 PM",
        "url": "https://urbananow.com/locations/geary/",
        "menu_url": "https://shop.urbananow.com/geary",
        "specials_url": "https://shop.urbananow.com/geary",
        "lat": 37.7802, "lon": -122.4466,
        "tax_note": "Prices shown are BEFORE tax (Sweed POS; tax computed at checkout). No tax statement printed on menu pages - verify at checkout.",
        "source_status": "Official Urbana site + shop.urbananow.com - live-fetched 2026-09-14",
        "deals": [
            "FLAG: As of 2026-09-14 the Geary store's online vape menu (24 items, 2 pages) contains NO Stiiizy-format pods. Brands stocked: TERP, PAX Labs, Jetty, Claybourne, Globs, Timeless (mostly AIO pens and 510-thread carts, which do NOT fit a Stiiizy pen).",
            "Urbana Mission store carries STIIIZY pods (see entries) - closest Urbana option for Stiiizy pods.",
        ],
    },
    {
        "name": "Urbana - Mission",
        "group": "Urbana Dispensaries",
        "address": "33 29th St, San Francisco, CA 94110",
        "zip": "94110",
        "phone": "(415) 814-3519",
        "hours": "Daily 10:00 AM - 9:00 PM",
        "url": "https://urbananow.com/locations/mission/",
        "menu_url": "https://shop.urbananow.com/mission",
        "specials_url": "https://shop.urbananow.com/mission",
        "lat": 37.7486, "lon": -122.4100,
        "tax_note": "Prices shown are BEFORE tax (Sweed POS; tax computed at checkout). No tax statement printed on menu pages - verify at checkout.",
        "source_status": "Official Urbana site + shop.urbananow.com - live-fetched 2026-09-14. Address confirmed on official locations page.",
        "deals": [],
    },
    {
        "name": "Bloomerang",
        "group": "Bloomerang Dispensary",
        "address": "3015 San Bruno Ave, San Francisco, CA 94134",
        "zip": "94134",
        "phone": "(415) 508-9400",
        "hours": "Daily 9:00 AM - 9:00 PM",
        "url": "https://bloomerangsf.com/",
        "menu_url": "https://bloomerangsf.com/menu/",
        "specials_url": "https://bloomerangsf.com/menu/",
        "lat": 37.723578, "lon": -122.4016993,
        "tax_note": "No tax statement on product pages (BLAZE POS; tax applied at checkout - standard for licensed CA retailers). Verify at checkout.",
        "source_status": "Official store site (bloomerangsf.com, BLAZE POS) - live-fetched 2026-09-14. License C10-0000640-LIC in site footer.",
        "deals": [
            "No active STIIIZY-specific promotion published on site at verification time.",
        ],
    },
    {
        "name": "STIIIZY Delivery (D2C)",
        "group": "STIIIZY direct-to-consumer (delivery.stiiizy.com / shop.stiiizy.com)",
        "address": "Ships/delivers within California (set your SF address at checkout)",
        "zip": "CA-wide",
        "phone": "-",
        "hours": "Online",
        "url": "https://www.stiiizy.com/",
        "menu_url": "https://shop.stiiizy.com/?tab=schedule",
        "specials_url": "https://shop.stiiizy.com/shop/daily-deals",
        "lat": REF[0], "lon": REF[1],
        "tax_note": "ALL prices on this store are explicitly marked '(Tax Incl.)' - tax INCLUDED in listed price.",
        "source_status": "Official STIIIZY store (linked as 'DELIVERY - CA' from stiiizy.com) - live-fetched 2026-09-14",
        "deals": [
            "Daily deal: 'STIIIZY Up to 20% OFF - all STIIIZY products every day'",
            "Daily deal: 'Last Chance Deals (Up to 50% OFF)'",
            "4.20% credit back (homepage banner, image - manual review)",
        ],
    },
    {
        "name": "North Beach Pipeline",
        "group": "Pipeline Dispensaries (Portola Pipeline Cannabis)",
        "address": "1335 Grant Ave, San Francisco, CA 94133",
        "zip": "94133",
        "phone": "(415) 658-7009",
        "hours": "Daily (see store site)",
        "url": "https://www.pipelinedispensary.com/locations/",
        "menu_url": "https://www.pipelinedispensary.com/stores/north-beach-pipeline",
        "specials_url": "https://www.pipelinedispensary.com/stores/north-beach-pipeline/specials",
        "lat": 37.7965, "lon": -122.4069,
        "tax_note": "Prices shown are BEFORE tax. Product pages state: '*Sales tax will be added at checkout.'",
        "source_status": "Official store site (pipelinedispensary.com) - product pages live-fetched 2026-09-14",
        "deals": [],
    },
]

for s in stores:
    s["distance_miles"] = round(haversine_miles(REF, (s["lat"], s["lon"])), 2)

# ---------------------------------------------------------------------------
# ENTRIES (verified price data)
# verified = "live"  -> fetched the official page directly on VERIFIED_DATE
#            "index" -> from search-engine index of the official page (flagged)
# ---------------------------------------------------------------------------
E = []
def add(store_key, product, brand, type_, size, price, price_was, tax, deal,
        source_url, thc=None, stock=None, verified="live", notes=None,
        compat="Fits STIIIZY pen (pod)"):
    E.append({
        "store": store_key, "product": product, "brand": brand, "type": type_,
        "size": size, "price": price, "price_was": price_was, "tax": tax,
        "deal": deal, "source_url": source_url, "thc": thc, "stock": stock,
        "verified": verified, "notes": notes or "", "compat": compat,
        "verified_date": VERIFIED_DATE,
    })

SP = "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/specials/sale/3241"
SP_BASE = "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/"

# --- Sunset Pipeline: 30% OFF STIIIZY PODS & ALL-IN-ONE VAPES sale (sale prices shown)
add("Sunset Pipeline", "Pineapple Express Original Pod", "STIIIZY", "pod", "0.5g",
    14.01, None, "not-included", "Part of '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' sale",
    SP, thc="85.83%", stock="In stock")
add("Sunset Pipeline", "Biscotti Original Pod", "STIIIZY", "pod", "0.5g",
    14.01, None, "not-included", "Part of '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' sale",
    SP, stock="In stock")
add("Sunset Pipeline", "Purple Haze Live Resin Pod", "STIIIZY", "pod", "1g",
    26.42, None, "not-included", "Part of '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' sale",
    SP, thc="83.6%", stock="In stock")
add("Sunset Pipeline", "STIIIZY White Raspberry (Original Pod)", "STIIIZY", "pod", "1g",
    24.81, None, "not-included", "Part of '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' sale",
    SP, thc="86.56%", stock="In stock")
aio_note = "All-in-one pen: standalone (does NOT mount in a Stiiizy battery)"
for prod, price, thc in [
    ("Apple Fritter All-In-One THC Pen", 26.00, "86.47%"),
    ("Watermelon Z All-In-One THC Pen", 28.82, "86.15%"),
    ("Blue Burst All-In-One THC Pen", 28.82, "83.38%"),
    ("Sour Tangie All-In-One THC Pen", 28.82, "86.4%"),
    ("Birthday Cake All-In-One", 28.82, "84.59%"),
    ("SFV OG All-In-One", 25.62, "85.38%"),
    ("Skywalker OG All-In-One", 28.82, "87.88%"),
    ("Pineapple Runtz All-In-One", 28.82, "88.09%"),
    ("Strawnana All-In-One", 28.82, "83.47%"),
    ("White Raspberry All-In-One", 28.82, "86%"),
    ("OG Kush All-In-One", 28.82, None),
]:
    add("Sunset Pipeline", prod, "STIIIZY", "aio", "1g",
        price, None, "not-included", "Part of '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' sale",
        SP, thc=thc, stock="In stock", notes=aio_note,
        compat="Standalone AIO pen (no battery needed)")

# --- Bloomerang (STIIIZY brand page, 0.5g Premium pods, all $11.04)
BR = "https://bloomerangsf.com/menu/brands/stiiizy-585591/"
for prod, thc in [
    ("0.5g GDP Premium THC Pod", "84.03%"),
    ("0.5g Biscotti Premium THC Pod", "85.1%"),
    ("0.5g Apple Fritter Premium THC Pod", "88.56%"),
    ("0.5g Strawnana Premium THC Pod", "87.35%"),
    ("0.5g Strawberry Cough Premium THC Pod", "86.42%"),
    ("0.5g Skywalker OG Premium THC Pod", "89.82%"),
]:
    add("Bloomerang", prod, "STIIIZY", "pod", "0.5g",
        11.04, None, "not-stated", None,
        BR, thc=thc, stock="In stock")
# extras confirmed on the same brand page / product-page 'you might also like'
add("Bloomerang", "0.5g Pineapple Express Premium THC Pod", "STIIIZY", "pod", "0.5g",
    11.04, None, "not-stated", None,
    "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/05g-pineapple-express-premium-thc-pod-stiiizy-6081740/",
    thc="89.58%")
add("Bloomerang", "0.5g Pineapple Runtz Premium THC Pod", "STIIIZY", "pod", "0.5g",
    11.04, None, "not-stated", None,
    "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/05g-pineapple-runtz-premium-thc-pod-stiiizy-6562326/",
    thc="84.01%")

# --- Urbana Mission (STIIIZY pods)
UM = "https://shop.urbananow.com/mission/menu/vapes-3322"
for prod, thc, stock in [
    ("Sour Diesel Pod (STIIIZY ORG)", "91.78%", "Only 5 left"),
    ("Blue Dream ORG Pod", "84.79%", "Only 1 left"),
    ("Premium Jack ORG Pod", "88.13%", "Only 4 left"),
    ("Apple Fritter ORG Pod", "85.66-87%", "Only 5 left"),
    ("Blue Burst Org Pod", "84.21%", "Only 2 left"),
    ("Juicy Melon ORG 1:1 Pod (THC/CBD)", "43.81% THC / 37.82% CBD", "Only 8 left"),
]:
    add("Urbana - Mission", prod, "STIIIZY", "pod", "1g",
        24.00, None, "not-stated", None, UM, thc=thc, stock=stock)
add("Urbana - Mission", "White Widow LQD Pod (Live Resin Liquid Diamonds)", "STIIIZY", "pod", "1g",
    26.00, None, "not-stated", None, UM, thc="84.43-86.46%")

# --- STIIIZY D2C (tax included)
D2C_PODS = "https://shop.stiiizy.com/shop/stiiizy-original-thc-pods"
D2C_VAPES = "https://shop.stiiizy.com/category/Vapes"
D2C_DEALS = "https://shop.stiiizy.com/shop/daily-deals"
add("STIIIZY Delivery (D2C)", "Original THC Pod - any of 28 strains (0.5g)", "STIIIZY", "pod", "0.5g",
    17.00, 21.00, "included", "SALE - was $21.00 (tax incl.)",
    D2C_PODS, notes="Live page shows every 0.5g Original pod at $17.00 (was $21.00), each marked '(Tax Incl.)'")
add("STIIIZY Delivery (D2C)", "Original THC Pod - any of 26 strains (1g)", "STIIIZY", "pod", "1g",
    27.00, 33.00, "included", "SALE - was $33.00 (tax incl.)",
    D2C_PODS, notes="Live page shows 1g Original pods (e.g. Pineapple Runtz, Pink Acai, Apple Fritter, Birthday Cake, Blue Burst, Blue Dream, Biscotti) at $27.00 (was $33.00), each marked '(Tax Incl.)'")
add("STIIIZY Delivery (D2C)", "Live Resin Liquid Diamonds Pod (Hawaiian Snow, Purple Zlushie, more)", "STIIIZY", "pod", "0.5g",
    18.00, 22.00, "included", "SALE - was $22.00 (tax incl.)",
    D2C_VAPES)
add("STIIIZY Delivery (D2C)", "Live Resin Liquid Diamonds Pod (Northern Lights, more)", "STIIIZY", "pod", "1g",
    29.00, 36.00, "included", "SALE - was $36.00 (tax incl.)",
    D2C_VAPES)
add("STIIIZY Delivery (D2C)", "Liquid Diamonds All-In-One (Lemon Cherry Gelato, Strawberry Shortcake, Pink Runtz, more)", "STIIIZY", "aio", "1g",
    29.00, 36.00, "included", "SALE - was $36.00 (tax incl.)",
    D2C_VAPES, notes=aio_note, compat="Standalone AIO pen (no battery needed)")
add("STIIIZY Delivery (D2C)", "AIO Premium THC Pen (Lemon Cherry Gelato, Northern Lights, Pink Runtz, Purple Haze, Purple Zlushie, Strawberry Shortcake, Tahoe OG, White Widow)", "STIIIZY", "aio", "1g",
    29.00, 36.00, "included", "SALE - was $36.00 (tax incl.)",
    D2C_VAPES, verified="index",
    notes=aio_note + " - prices captured from search index of official shop.stiiizy.com Vapes page (page is JS-rendered; link for manual review)",
    compat="Standalone AIO pen (no battery needed)")
add("STIIIZY Delivery (D2C)", "CBD All-In-One 1:1 THC/CBD (Mango, 0.5g)", "STIIIZY", "aio", "0.5g",
    21.00, 26.00, "included", "SALE - was $26.00 (tax incl.)",
    D2C_VAPES, notes=aio_note, compat="Standalone AIO pen (no battery needed)")
add("STIIIZY Delivery (D2C)", "STIIIZY BAR battery (dual 1g-pod holder, display, USB-C)", "STIIIZY", "battery", "1 ea",
    None, None, "included", None,
    "https://shop.stiiizy.com/category/Accessories",
    verified="index",
    notes="D2C price not captured in live fetch; sold in D2C 'Deals of the Day' (STIIIZY BAR). Manual review via link.",
    compat="Holds two STIIIZY 1g pods")

# --- North Beach Pipeline
add("North Beach Pipeline", "STIIIZY Blue Burst Pod", "STIIIZY", "pod", "1g",
    26.00, None, "not-included", None,
    "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-blue-burst-pod",
    thc="CBD 0.52% listed", stock="OUT OF STOCK at verification time (notify-me available)")
add("North Beach Pipeline", "STIIIZY Bar Battery", "STIIIZY", "battery", "1 ea",
    27.62, None, "not-included", None,
    "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-bar-stiiizy-battery",
    notes="Page states '*Sales tax will be added at checkout.'",
    compat="Holds two STIIIZY 1g pods")

# store distance join
store_map = {s["name"]: s for s in stores}
for e in E:
    e["distance_miles"] = store_map[e["store"]]["distance_miles"]

# ---------------------------------------------------------------------------
# IRREGULARITIES / FLAGS (for the review panel)
# ---------------------------------------------------------------------------
flags = [
    ("FLAG", "Urbana - Geary (your anchor store) has NO Stiiizy-format pods online as of 2026-09-14. Full vape menu checked (24 items): TERP, PAX Labs, Jetty, Claybourne, Globs, Timeless - all AIO pens or 510-thread carts, none fit a Stiiizy pen. Closest Urbana with STIIIZY pods is Urbana Mission (33 29th St) at $24.00/1g.",
     "https://shop.urbananow.com/geary/menu/vapes-3322"),
    ("FLAG", "stiiizy.com /products/* pages redirect to the homepage from non-CA networks (geo-restriction). D2C prices above were taken from the live shop.stiiizy.com pages where possible; items marked 'search-index' come from the search index of the official site and need a manual click-through.",
     "https://shop.stiiizy.com/shop/stiiizy-original-thc-pods"),
    ("FLAG", "STIIIZY Parkmerced in-store menu (stiiizy.dispensary.shop) is a JavaScript app - per-product prices cannot be machine-verified. The store page's 'discounted menu' linktree (retail.stiiizy.com/linktree/parkmerced) showed 'Deployment Paused' at verification time. Weekly/daily deal graphics are image files - manual review required.",
     "https://www.stiiizy.com/pages/stiiizy-parkmerced"),
    ("FLAG", "North Beach Pipeline STIIIZY Blue Burst Pod (1g, $26.00) is OUT OF STOCK as of 2026-09-14.",
     "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-blue-burst-pod"),
    ("FLAG", "Sunset Pipeline's STIIIZY sale prices are the POST-DISCOUNT prices under the '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' sale. Pre-discount prices are not printed on the page; back-calculated values ($14.01 -> ~$20.01 for 0.5g, $28.82 -> ~$41.17 for 1g AIO) are derivations, not listed facts.",
     "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/specials/sale/3241"),
    ("FLAG", "Bloomerang and Urbana product pages do not print a tax-included/excluded statement. California licensed retailers add sales tax + 15% state cannabis excise + local cannabis business tax at checkout, so treat their listed prices as PRE-TAX until the receipt says otherwise.",
     "https://bloomerangsf.com/menu/brands/stiiizy-585591/"),
    ("FLAG", "Excluded as untrusted/unverifiable for SF: stiiizypods.site (unofficial third-party shop, not STIIIZY), herb.delivery (Los Angeles-based, not SF), 420labs.com (domain parked/for sale, not the SF store's site), thestash.com (unrelated site). No data from these was used.",
     None),
    ("FLAG", "Urbana's homepage JSON-LD lists an Oakland address (415 W. Grand Ave) while its own location pages list Geary + Mission SF addresses. The official location pages were treated as authoritative. Minor site-data inconsistency.",
     "https://urbananow.com/"),
    ("INFO", "SF combined SALES tax is 8.625% (7.25% CA state + 1.375% city/district) per multiple 2026 tax-rate sources; CDTFA's quarterly rate files are the official reference. On cannabis, add the 15% CA state cannabis excise tax (official, CDTFA; rate restored to 15% effective Oct 1 2025, next adjustment delayed to FY2028-29) plus SF's local cannabis business tax (reported 2.5-5% of gross receipts depending on retailer size - confirm on your receipt).",
     "https://cdtfa.ca.gov/industry/cannabis/tax-facts.htm"),
    ("INFO", "STIIIZY D2C prices changed between the search index ($16/$20, $26/$32) and the live page ($17/$21, $27/$33) during verification - prices move. This list reflects the live page at 2026-09-14; re-verify before purchase.",
     "https://shop.stiiizy.com/shop/stiiizy-original-thc-pods"),
]

# other STIIIZY retail locations (verified store facts, no online prices captured)
other_locations = [
    ("STIIIZY SoMa", "518 Brannan St, San Francisco, CA 94107", "(628) 254-1420",
     "Mon-Thu 9:00 AM - 8:45 PM, Fri-Sat 9:00 AM - 9:45 PM",
     "https://www.stiiizy.com/pages/soma-dispensary",
     "In-store menu via stiiizy.dispensary.shop (JS app - manual review)."),
    ("STIIIZY Union Square", "180 O'Farrell St, San Francisco, CA 94102", "(628) 258-5133",
     "Daily 7:00 AM - 9:45 PM",
     "https://www.stiiizy.com/pages/union-square-dispensary",
     "In-store menu via stiiizy.dispensary.shop (JS app - manual review)."),
    ("STIIIZY Mission", "3326 Mission St, San Francisco, CA 94110", "(415) 787-6006",
     "Daily 8:00 AM - 9:45 PM",
     "https://www.stiiizy.com/pages/mission-dispensary",
     "In-store menu via stiiizy.dispensary.shop (JS app - manual review)."),
]

data = {
    "title": "Stiiizy Pod Deals - San Francisco (94122 / Stonestown)",
    "verified_date": VERIFIED_DATE,
    "reference_point": "2161 Irving St, San Francisco, CA 94122 (Sunset Pipeline)",
    "stores": stores,
    "entries": E,
    "flags": flags,
    "other_locations": other_locations,
}

with open(os.path.join(SITE, "data.js"), "w") as f:
    f.write("// Generated by build/build.py on " + VERIFIED_DATE + "\n")
    f.write("window.PODS_DATA = ")
    json.dump(data, f, indent=2)
    f.write(";\n")

print(f"Wrote {SITE}/data.js with {len(E)} entries, {len(stores)} stores, {len(flags)} flags")
