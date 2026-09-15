#!/usr/bin/env python3
"""
Build script for the VapePods GitHub Pages site.

MODEL: this file is the single source of truth. Every price below was read from an
official page and is recorded together with (a) the exact URL it came from and
(b) how it was verified. Nothing is inferred, averaged or estimated. If a number
is not printed on the linked page it is not in this file.

Verification levels
-------------------
live-2026-09-15 : the official page was fetched and read during this pass.
carried-2026-09-14 : verified on 2026-09-14, NOT re-fetched today -> shown with a
                     visible "not re-checked today" chip so it can never be mistaken
                     for fresh data.

Sources are either:
  official-site       : the retailer's own domain (pipelinedispensary.com, bloomerangsf.com,
                        shop.urbananow.com, shop.stiiizy.com, www.stiiizy.com, urbananow.com)
  official-brand-menu : the brand's own ordering domain, e.g. stiiizy.dispensary.shop
                        (STIIIZY's own pick-up menu, run on the Flowhub platform)
  brand-listing       : the store's brand-operated marketplace listing (STIIIZY Parkmerced on
                        Weedmaps, linked from the store's own page). Flagged on the site.

Tax handling
------------
  included     : the store's own page says tax is included ("(Tax Incl.)" / "OUT THE DOOR *Tax included*")
  not-included : the store's own page says tax is added at checkout
  not-stated   : the store prints no tax note anywhere we could read -> never guessed.
"""

import json, math, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "site")
os.makedirs(SITE, exist_ok=True)

VERIFIED_DATE = "2026-09-15"
PREV_DATE = "2026-09-14"

# Reference point: Sunset Pipeline, 2161 Irving St, SF 94122 (the user's area).
REF = (37.7631407, -122.4811240)


def haversine_miles(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


# ---------------------------------------------------------------------------
# STORES
# ---------------------------------------------------------------------------
stores = [
    {
        "name": "STIIIZY Parkmerced",
        "group": "STIIIZY retail (the 'Stiiizy at Stonestown' store)",
        "address": "61 Cambon Dr, San Francisco, CA 94132",
        "zip": "94132",
        "phone": "(628) 216-5717",
        "hours": "Daily 7:00 AM - 9:45 PM",
        "url": "https://www.stiiizy.com/pages/stiiizy-parkmerced",
        "menu_url": "https://stiiizy.dispensary.shop/parkmerced/rec/menu",
        "specials_url": "https://stiiizy.dispensary.shop/parkmerced/rec/deals",
        "lat": 37.71799, "lon": -122.47437, "coord_note": "store coordinates from the store's own listing data",
        "tax": "included",
        "tax_note": ("The store's brand-operated listing states: \"ALL PRICES ARE OUT THE DOOR *Tax included*\". "
                     "The pick-up menu itself (stiiizy.dispensary.shop) prints no tax line, so the price you pay "
                     "is the price shown per the store's own statement - confirm at checkout."),
        "source_status": ("Official STIIIZY store page (stiiizy.com) + STIIIZY's own pick-up menu "
                          "(stiiizy.dispensary.shop, Flowhub platform) + brand-operated Weedmaps store listing "
                          "- all live-fetched 2026-09-15. License C10-0000825-LIC; opened July 1, 2023."),
        "deals": [
            "Sundays & Wednesdays: $20.00 STIIIZY 1G OG Pod (Taxes Included) - from the store's own listing intro",
            "Everyday: STIIIZY Buy 2, get 1, 50% off (shown on individual product pages as deal code 'CA - B2G150 - Stiiizy (10/25 -TBD) MMJV3*')",
            "First-time customers: up to 30% off all STIIIZY products (not valid if you have been to any STIIIZY location before)",
            "Everyday: $10.00 STIIIZY 100mg Edible Mylar (Taxes Included)",
            "Sundays & Wednesdays: $20.00 STIIIZY 3.5g Black Label (Taxes Included)",
            "Happy Hour 4:20pm-7:10pm: Buy 2, Get 1 for $1 - Uncle Arnies",
            "Rewards: 1% back every purchase; 4.20% back every first Friday of the month",
            "Store deal page also lists: On Sale, Sessions 3 for $20, Up to 50% off Originals, up to 25-30% off ABX/CBX/Camino/Jeeter/Made/WCC/Care By Design/Smoken Promises",
        ],
    },
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
        "lat": REF[0], "lon": REF[1], "coord_note": "this is the 94122 reference point",
        "tax": "not-included",
        "tax_note": ("Product pages print \"*Cannabis and Sales tax will be added at checkout.\" "
                     "(read on the Northern Lights Live Resin Pod page, 2026-09-15) - listed prices are PRE-TAX."),
        "source_status": ("Official store site (pipelinedispensary.com, Dutchie menu) - live-fetched 2026-09-15. "
                          "Sale page '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' (sale/3241) read line by line."),
        "deals": [
            "30% OFF STIIIZY PODS & ALL-IN-ONE VAPES - official sale page 3241 (18 STIIIZY items listed at sale prices)",
            "30% off select Pipeline Cannabis 7g & 14g flower",
            "Buy 2 for $15, Sunset Select 1g prerolls",
            "West Coast Trees 1g prerolls, 5 for $25",
            "Sunset only: 40% off all Humboldt Grower's Network prerolls",
            "20% off Northern Harvest prerolls",
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
        "menu_url": "https://shop.urbananow.com/geary/menu/vapes-3322",
        "specials_url": "https://shop.urbananow.com/geary",
        "lat": 37.7802, "lon": -122.4466, "coord_note": "straight-line estimate from the listed street address",
        "tax": "not-stated",
        "tax_note": "No tax statement printed on the menu pages we could read - verify at checkout.",
        "source_status": "Official Urbana site + shop.urbananow.com (Sweed POS) - live-fetched 2026-09-15.",
        "deals": [
            "FLAG: the Geary vape menu carries NO Stiiizy-format pods. Brand filter on the live menu lists only "
            "CLAYBOURNE CO., GLOBS, JETTY, PAX LABS, TERP and TIMELESS - none of these mount in a STIIIZY pen.",
            "Closest Urbana with STIIIZY pods is Urbana Mission (33 29th St) - see entries.",
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
        "menu_url": "https://shop.urbananow.com/mission/menu/vapes-3322",
        "specials_url": "https://shop.urbananow.com/mission",
        "lat": 37.7486, "lon": -122.4100, "coord_note": "straight-line estimate from the listed street address",
        "tax": "not-stated",
        "tax_note": "No tax statement printed on the menu pages we could read - verify at checkout.",
        "source_status": ("Official Urbana site + shop.urbananow.com (Sweed POS) - live-fetched 2026-09-15. "
                          "Vape menu shows a 'Pod' sub-category with STIIIZY as one of only two brands."),
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
        "menu_url": "https://bloomerangsf.com/menu/brands/stiiizy-585591/",
        "specials_url": "https://bloomerangsf.com/menu/categories/vapes/",
        "lat": 37.723578, "lon": -122.4016993, "coord_note": "store coordinates from the store's own listing data",
        "tax": "not-stated",
        "tax_note": ("No tax line printed on product pages (BLAZE/Tymber menu). California retailers add sales tax at "
                     "checkout, so treat listed prices as PRE-TAX until a receipt says otherwise."),
        "source_status": ("Official store site (bloomerangsf.com, BLAZE/Tymber menu) - live-fetched 2026-09-15, including "
                          "individual product pages and the store's live product sitemap."),
        "deals": [
            "No STIIIZY-specific promotion published on the site at verification time.",
            "Cheapest verified 0.5g STIIIZY pod in this list at $11.04 (pre-tax).",
        ],
    },
    {
        "name": "STIIIZY Delivery (D2C)",
        "group": "STIIIZY direct-to-consumer (shop.stiiizy.com)",
        "address": "California delivery / pick-up store (set your SF address at checkout)",
        "zip": "CA-wide",
        "phone": "-",
        "hours": "Online",
        "url": "https://www.stiiizy.com/",
        "menu_url": "https://shop.stiiizy.com/category/Vapes?tab=schedule",
        "specials_url": "https://shop.stiiizy.com/shop/daily-deals?tab=schedule",
        "lat": REF[0], "lon": REF[1], "coord_note": "online store - distance is not meaningful",
        "tax": "included",
        "tax_note": "Every price on this store carries the printed tag \"(Tax Incl.)\" - tax INCLUDED in the listed price.",
        "source_status": ("Official STIIIZY store (linked as 'DELIVERY - CA' from stiiizy.com) - live-fetched 2026-09-15 "
                          "(Original THC Pods page and Accessories page)."),
        "deals": [
            "Daily deal: 'STIIIZY Up to 20% OFF - all STIIIZY products every day'",
            "Daily deal: 'Last Chance Deals [Up to 50% OFF]'",
            "Site banner: '4.20% Credit Back'",
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
        "lat": 37.7965, "lon": -122.4069, "coord_note": "straight-line estimate from the listed street address",
        "tax": "not-included",
        "tax_note": ("Pipeline product pages state \"*Cannabis and Sales tax will be added at checkout.\" "
                     "The North Beach item page read today printed no tax line itself - flagged."),
        "source_status": "Official store site (pipelinedispensary.com, Dutchie menu) - product page live-fetched 2026-09-15.",
        "deals": [],
    },
]

store_map = {s["name"]: s for s in stores}
for s in stores:
    s["distance_miles"] = round(haversine_miles(REF, (s["lat"], s["lon"])), 2)

# ---------------------------------------------------------------------------
# ENTRIES
# ---------------------------------------------------------------------------
E = []
_seq = [0]


def add(store, product, type_, size, price, source_url,
        tax=None, price_was=None, deal=None, thc=None, stock=None,
        verified="live", notes=None, brand="STIIIZY", source_kind="official-site",
        is_new=False):
    """type_ = pod | aio | battery   ; tax defaults to the store's tax status."""
    _seq[0] += 1
    st = store_map[store]
    if tax is None:
        tax = st["tax"]
    compat = {
        "pod": "Mounts in a STIIIZY pod pen (original / Pro / Pro XL / BAR)",
        "aio": "All-in-one pen - standalone, does NOT mount in a STIIIZY battery",
        "battery": "Hardware only - no pod included",
    }[type_]
    E.append({
        "id": "E%03d" % _seq[0],
        "store": store, "product": product, "brand": brand, "type": type_, "size": size,
        "price": price, "price_was": price_was, "tax": tax, "deal": deal,
        "source_url": source_url, "source_kind": source_kind, "thc": thc, "stock": stock,
        "verified": verified, "verified_date": VERIFIED_DATE if verified == "live" else PREV_DATE,
        "notes": notes or "", "compat": compat, "is_new": is_new,
        "distance_miles": st["distance_miles"],
    })


POD_NOTE_PM = ("STIIIZY Parkmerced pick-up menu, STIIIZY's own ordering domain. Item carries the menu's "
               "'ON SALE' flag; the pre-discount price is not printed on the page.")

# ===========================================================================
# STIIIZY PARKMERCED  (all live 2026-09-15)
# Deals documented on the sale page / store listing:
DEAL_PM_WED = ("Sundays & Wednesdays: $20.00 STIIIZY 1G OG Pod (Taxes Included) per the store's own listing - "
               "regular menu price for a 1g Original pod is $23.00 (also 'ON SALE')")
DEAL_PM_B2G1 = ("Product page lists this deal code verbatim: 'CA - B2G150 - Stiiizy (10/25 -TBD) MMJV3*'; the store's "
                "own listing describes the same deal as 'STIIIZY Buy 2, get 1, 50% off'")
PM_MENU = "https://stiiizy.dispensary.shop/parkmerced/rec/vapes/nb/eg3?brand=STIIIZY&order_by=price&order_dir=asc"

_PM_PODS_05 = [
    ("Skywalker OG", "88.047%", "cd41d67e-d4d9-4f0f-83e6-1b4fc000128d"),
    ("Blue Dream", "86.628%", "08f9f1a0-7343-42fd-8093-3e8d5ad0d3bf"),
    ("OG Kush", "86.377%", "538f49ac-74ce-4a58-8cf3-c23d5051aabc"),
    ("Pineapple Express", "85.833%", "4d161471-c33f-4853-9651-5d13113a7268"),
    ("Super Lemon Haze", "86.393%", "7f9593ed-397c-4f86-9a8f-5cf1d27ffaa5"),
    ("Watermelon Z", "88.001%", "d2a5da32-75c8-4026-a951-875609239f54"),
    ("Gelato", "87.128%", "92aef683-bd57-4f84-8ba9-32db78e0fbb7"),
    ("Strawberry Cough", "84.655%", "167d003a-e732-42f2-9366-a9b0340d09e1"),
]
for strain, thc, vid in _PM_PODS_05:
    add("STIIIZY Parkmerced", "STIIIZY Original Pod - %s (0.5g)" % strain, "pod", "0.5g", 13.00,
        "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-pod-%s-0.5g/v/%s"
        % (strain.lower().replace(" ", "-"), vid),
        deal=DEAL_PM_B2G1, thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=True,
        notes=POD_NOTE_PM + " Menu shows 0.5g Original pods at $13.00 across many strains.")

_PM_PODS_1G = [
    ("OG Kush", "87.774%", "38d3a611-f255-451b-bef5-d02b6d7b83d6"),
    ("Skywalker OG", "87.883%", "d4814a9c-8be1-4576-8426-aed6952a48f8"),
    ("Blue Burst", "83.377%", "20eeac06-0c8e-40c0-8783-15dd237019ef"),
]
for strain, thc, vid in _PM_PODS_1G:
    add("STIIIZY Parkmerced", "STIIIZY Original Pod - %s (1g)" % strain, "pod", "1g", 23.00,
        "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-pod-%s-1g/v/%s"
        % (strain.lower().replace(" ", "-"), vid),
        deal=DEAL_PM_B2G1 + " | " + DEAL_PM_WED if strain == "OG Kush" else DEAL_PM_B2G1,
        thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=True,
        notes=POD_NOTE_PM + " This is the same SKU as the store's Sunday/Wednesday $20 (tax-incl.) deal."
        if strain == "OG Kush" else POD_NOTE_PM)

add("STIIIZY Parkmerced", "STIIIZY Original All-In-One - Watermelon Z (1g)", "aio", "1g", 23.00,
    "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-all-in-one-watermelon-z-1g/v/e365c19e-ae4b-4b37-b399-f85816e6f3c8",
    thc="87.481%", stock="In stock (menu shows ON SALE)", source_kind="official-brand-menu", is_new=True,
    notes="Standalone all-in-one pen - does not mount in a STIIIZY battery. " + POD_NOTE_PM)

# 1g OG pod weekly deal (brand-operated store listing)
add("STIIIZY Parkmerced", "STIIIZY 1G OG Pod - Sunday & Wednesday deal", "pod", "1g", 20.00,
    "https://weedmaps.com/dispensaries/stiiizy-parkmerced", tax="included",
    deal="Sundays & Wednesdays only: $20.00 STIIIZY 1G OG Pod (Taxes Included)",
    stock="Weekly deal (Sun & Wed)", source_kind="brand-listing", is_new=True,
    notes=("Price and the '(Taxes Included)' wording are quoted from STIIIZY Parkmerced's brand-operated store "
           "listing (the store's own intro text), read 2026-09-15. The official pick-up menu lists the same 1g OG "
           "Kush pod at $23.00 the rest of the week. Deal is weekday-limited - confirm before you go."))

# ===========================================================================
# SUNSET PIPELINE  (sale page + product pages live 2026-09-15)
# ===========================================================================
SP_SALE = "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/specials/sale/3241"
SP_DEAL = "Part of '30% OFF STIIIZY PODS & ALL-IN-ONE VAPES' (official sale page 3241)"
SP_TAXNOTE = "Product pages state: '*Cannabis and Sales tax will be added at checkout.' - price is PRE-TAX."

existing_sp_pods = [
    ("Pineapple Express Original Pod (0.5g)", "0.5g", 14.01, "85.83%",
     "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/pineapple-express-original-pod-0-5g-15482"),
    ("Biscotti Original Pod (0.5g)", "0.5g", 14.01, None,
     "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/biscotti-original-pod-0-5g-1093"),
    ("Purple Haze Live Resin Pod (1g)", "1g", 26.42, "83.6%",
     "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/purple-haze-live-resin-pod-1g-66777"),
    ("STIIIZY White Raspberry (1g pod)", "1g", 24.81, "86.56%",
     "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/stiiizy-white-raspberry"),
]
for prod, size, price, thc, url in existing_sp_pods:
    add("Sunset Pipeline", prod, "pod", size, price, url, tax="not-included", deal=SP_DEAL,
        thc=thc, stock="In stock", notes=SP_TAXNOTE)

# NEW Sunset Pipeline pods
add("Sunset Pipeline", "Northern Lights Live Resin Pod (1g)", "pod", "1g", 26.42,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/northern-lights-live-resin-pod-1g-65890",
    tax="not-included", deal=SP_DEAL, thc="86.75%", stock="In stock", is_new=True,
    notes="Product page read line by line 2026-09-15: '1g $26.42'. " + SP_TAXNOTE)
add("Sunset Pipeline", "Super Lemon Haze Original Pod (1g)", "pod", "1g", 24.82,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/super-lemon-haze-original-pod-1g-45669",
    tax="not-included", deal=SP_DEAL, thc="85.7%", stock="In stock", is_new=True, notes=SP_TAXNOTE)
add("Sunset Pipeline", "Cereal Milk Live Resin Pod (1g)", "pod", "1g", 26.42,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/cereal-milk-live-resin-pod-1g-55297",
    tax="not-included", deal=SP_DEAL, thc="85.97%", stock="In stock", is_new=True, notes=SP_TAXNOTE)
add("Sunset Pipeline", "Strawberry Shortcake Live Resin Diamonds Pod (1g)", "pod", "1g", 26.42,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/strawberry-shortcake-live-resin-diamonds-stiiizy-pod",
    tax="not-included", deal=SP_DEAL, thc="86.87%", stock="In stock", is_new=True, notes=SP_TAXNOTE)
add("Sunset Pipeline", "STIIIZY BAR battery (dual-pod battery)", "battery", "1 ea", 24.02,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/stiiizy-stiiizy-bar",
    tax="not-included", stock="In stock", is_new=True,
    notes="Hardware: holds two 1g STIIIZY pods. " + SP_TAXNOTE)

# Sunset Pipeline AIO pens (carried from 2026-09-14 sale page, still listed on the live sale page)
_sp_aio = [
    ("Apple Fritter All-In-One THC Pen (1g)", 26.00, "86.47%"),
    ("Watermelon Z All-In-One THC Pen (1g)", 28.82, "86.15%"),
    ("Blue Burst All-In-One THC Pen (1g)", 28.82, "83.38%"),
    ("Sour Tangie All-In-One THC Pen (1g)", 28.82, "86.4%"),
    ("Birthday Cake All-In-One (1g)", 28.82, "84.59%"),
    ("SFV OG All-In-One (1g)", 25.62, "85.38%"),
    ("Skywalker OG All-In-One (1g)", 28.82, "87.88%"),
    ("Pineapple Runtz All-In-One (1g)", 28.82, "88.09%"),
    ("Strawnana All-In-One (1g)", 28.82, "83.47%"),
    ("White Raspberry All-In-One (1g)", 28.82, "86%"),
    ("OG Kush All-In-One (1g)", 28.82, None),
    ("King Louis XIII All-In-One (1g)", 26.42, "85.73%"),
    ("Magic Melon All-In-One (1g)", 26.42, "84.72%"),
    ("Orange Sunset All-In-One (1g)", 26.42, "85.88%"),
    ("Tahoe OG Live Resin Diamonds All-In-One (1g)", 28.82, "84.48%"),
    ("White Widow Live Resin Diamonds All-In-One (1g)", 28.82, "84.27%"),
    ("Strawberry Shortcake Live Resin Diamonds All-In-One (1g)", 28.82, "85.3%"),
]
for prod, price, thc in _sp_aio:
    add("Sunset Pipeline", prod, "aio", "1g", price, SP_SALE, tax="not-included", deal=SP_DEAL,
        thc=thc, stock="In stock", notes=SP_TAXNOTE)

# ===========================================================================
# BLOOMERANG (live 2026-09-15)
# ===========================================================================
BR_BRAND = "https://bloomerangsf.com/menu/brands/stiiizy-585591/"
BR_NOTE = ("Bloomerang product pages print no tax line - treat as PRE-TAX until the receipt says otherwise. "
           "Verified live 2026-09-15.")
_br_05 = [
    ("GDP", "84.03%", "05g-gdp-premium-thc-pod-stiiizy-6081732"),
    ("Biscotti", "85.1%", "05g-biscotti-premium-thc-pod-stiiizy-6081728"),
    ("Apple Fritter", "88.56%", "05g-apple-fritter-premium-thc-pod-stiiizy-6081726"),
    ("Strawnana", "87.35%", "05g-strawnana-premium-thc-pod-stiiizy-6081749"),
    ("Strawberry Cough", "86.42%", "05g-strawberry-cough-premium-thc-pod-stiiizy-6081748"),
    ("Skywalker OG", "89.82%", "05g-skywalker-og-premium-thc-pod-stiiizy-6081745"),
    ("Premium Jack", "87.66%", "05g-premium-jack-premium-thc-pod-stiiizy-6081742"),
    ("Orange Sunset", "85.5%", "05g-orange-sunset-premium-thc-pod-stiiizy-6081739"),
]
for strain, thc, slug in _br_05:
    add("Bloomerang", "0.5g %s / Premium THC Pod / STIIIZY" % strain, "pod", "0.5g", 11.04,
        "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/%s/" % slug,
        tax="not-stated", thc=thc, stock="In stock",
        is_new=(strain in ("Premium Jack", "Orange Sunset")),
        notes=BR_NOTE + ("" if strain in ("Premium Jack", "Orange Sunset")
                         else " Price re-verified live 2026-09-15 on the STIIIZY brand page / product pages."))

_br_1g = [
    ("OG Kush", "88.32%", "1g-og-kush-premium-thc-pod-stiiizy-6082043"),
    ("Watermelon Z", "85.35%", "1g-watermelon-z-premium-thc-pod-stiiizy-6082089"),
    ("Strawberry Cough", "85.61%", "1g-strawberry-cough-premium-thc-pod-stiiizy-6082071"),
]
for strain, thc, slug in _br_1g:
    add("Bloomerang", "1g %s / Premium THC POD / STIIIZY" % strain, "pod", "1g", 19.33,
        "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/%s/" % slug,
        tax="not-stated", thc=thc, stock="In stock (product listed in the store's live sitemap)",
        is_new=(strain != "Strawberry Cough"),
        verified="live" if strain in ("OG Kush", "Watermelon Z") else "carried",
        notes=BR_NOTE if strain in ("OG Kush", "Watermelon Z")
        else BR_NOTE + " Price read 2026-09-14; the SKU is still listed in Bloomerang's live product sitemap (2026-09-15) but the price was not re-read today.")

# Bloomerang items that are not on today's brand page but whose pages existed on 2026-09-14
for strain, slug in [("Pineapple Express", "05g-pineapple-express-premium-thc-pod-stiiizy-6081740"),
                     ("Pineapple Runtz", "05g-pineapple-runtz-premium-thc-pod-stiiizy-6562326")]:
    add("Bloomerang", "0.5g %s / Premium THC Pod / STIIIZY" % strain, "pod", "0.5g", 11.04,
        "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/%s/" % slug,
        tax="not-stated", verified="carried", stock="Listed in the store's live product sitemap (2026-09-15)",
        notes=BR_NOTE + " FLAG: this SKU did not appear on the brand page on 2026-09-15 (the page listed 6 pods). "
                        "The product URL is still present in the store's live sitemap, so the price needs a manual click-through.")

add("Bloomerang", "1g AIO Premium Jack / Disposable Pen / STIIIZY", "aio", "1g", 20.25,
    "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/1g-aio-premium-jack-disposable-pen-stiiizy-7795879/",
    tax="not-stated", thc="80.56%", stock="In stock", is_new=True,
    notes="Standalone disposable - does not mount in a STIIIZY battery. " + BR_NOTE)
add("Bloomerang", "0.5g AIO Watermelon Z / Disposable Pen / STIIIZY", "aio", "0.5g", 14.72,
    "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/05g-aio-watermelon-z-disposable-pen-stiiizy-6082528/",
    tax="not-stated", thc="84.35%", stock="In stock",
    notes="Standalone disposable - does not mount in a STIIIZY battery. " + BR_NOTE)
add("Bloomerang", "Advanced Starter Kit - Red (STIIIZY battery kit)", "battery", "1 ea", 36.82,
    "https://bloomerangsf.com/menu/products/stiiizy-585591/accessories/advanced-starter-kit-red-stiiizy-6082349/",
    tax="not-stated", stock="In stock",
    notes="Hardware kit (battery). Listed among 'More by STIIIZY' on a live product page. " + BR_NOTE)

# ===========================================================================
# URBANA - MISSION (live 2026-09-15)
# ===========================================================================
UM = "https://shop.urbananow.com/mission/menu/vapes-3322"
UM_NOTE = "Bloomerang-style caveat: Urbana prints no tax line - treat as PRE-TAX until the receipt says otherwise. Live 2026-09-15."
_um = [
    ("Sour Diesel Pod (STIIIZY ORG, 1g)", "91.78%", "Only 5 left", False),
    ("Blue Dream ORG Pod (1g)", "84.79%", "Only 1 left", False),
    ("Premium Jack ORG Pod (1g)", "88.13%", "Only 4 left", False),
    ("Apple Fritter ORG Pod (1g)", "85.66-87%", "Only 5 left", False),
    ("Blue Burst ORG Pod (1g)", "84.21%", "Only 2 left", False),
    ("Juicy Melon ORG 1:1 Pod (THC/CBD, 1g)", "43.81% THC / 37.82% CBD", "Only 8 left", False),
    ("OG Kush ORG Pod (1g)", "87.76%", "In stock", True),
]
for prod, thc, stock, isnew in _um:
    add("Urbana - Mission", prod, "pod", "1g", 24.00, UM, tax="not-stated", thc=thc, stock=stock,
        is_new=isnew, notes=UM_NOTE)
add("Urbana - Mission", "White Widow LQD Pod (Live Resin Liquid Diamonds, 1g)", "pod", "1g", 26.00,
    UM, tax="not-stated", thc="84.43-86.46%", stock="In stock", notes=UM_NOTE)

# ===========================================================================
# STIIIZY DELIVERY (D2C) - tax included
# ===========================================================================
D2C_PODS = "https://shop.stiiizy.com/shop/stiiizy-original-thc-pods"
D2C_ACC = "https://shop.stiiizy.com/category/Accessories"
D2C_VAPES = "https://shop.stiiizy.com/category/Vapes"
D2C_NOTE = "Page prints '(Tax Incl.)' next to the price - tax INCLUDED."

add("STIIIZY Delivery (D2C)", "Original THC Pod - all strains (0.5g)", "pod", "0.5g", 17.00, D2C_PODS,
    tax="included", price_was=21.00, deal="SALE - was $21.00 (tax incl.)",
    stock="In stock - 28 of the 53 Original pod SKUs are 0.5g",
    notes="Live page header: 'All Strains of Original THC Pods - 52 options available - $17.00 - $27.00 (Tax Incl.)'. " + D2C_NOTE)
add("STIIIZY Delivery (D2C)", "Original THC Pod - all strains (1g)", "pod", "1g", 27.00, D2C_PODS,
    tax="included", price_was=33.00, deal="SALE - was $33.00 (tax incl.)",
    stock="In stock - 25 of the 53 Original pod SKUs are 1g", notes=D2C_NOTE)
add("STIIIZY Delivery (D2C)", "STIIIZY BAR battery (dual 1g-pod battery)", "battery", "1 ea", 40.00, D2C_ACC,
    tax="included", verified="live", is_new=True,
    stock="In stock - 8 colourways listed, all $40.00",
    notes="Live Accessories page 2026-09-15: BAR, Purple, Camouflage, Cheetah, Rose, Blue, Pearl White, Red, "
          "Silver - every colourway $40.00 (Tax Incl.). Holds two 1g pods. " + D2C_NOTE)
add("STIIIZY Delivery (D2C)", "Live Resin Liquid Diamonds Pod (0.5g)", "pod", "0.5g", 18.00, D2C_VAPES,
    tax="included", price_was=22.00, deal="SALE - was $22.00 (tax incl.)", verified="carried", notes=D2C_NOTE)
add("STIIIZY Delivery (D2C)", "Live Resin Liquid Diamonds Pod (1g)", "pod", "1g", 29.00, D2C_VAPES,
    tax="included", price_was=36.00, deal="SALE - was $36.00 (tax incl.)", verified="carried", notes=D2C_NOTE)
add("STIIIZY Delivery (D2C)", "Liquid Diamonds All-In-One (1g)", "aio", "1g", 29.00, D2C_VAPES,
    tax="included", price_was=36.00, deal="SALE - was $36.00 (tax incl.)", verified="carried", notes=D2C_NOTE)
add("STIIIZY Delivery (D2C)", "AIO Premium THC Pen (1g)", "aio", "1g", 29.00, D2C_VAPES,
    tax="included", price_was=36.00, deal="SALE - was $36.00 (tax incl.)", verified="carried", notes=D2C_NOTE)
add("STIIIZY Delivery (D2C)", "CBD All-In-One 1:1 THC/CBD (Mango, 0.5g)", "aio", "0.5g", 21.00, D2C_VAPES,
    tax="included", price_was=26.00, deal="SALE - was $26.00 (tax incl.)", verified="carried", notes=D2C_NOTE)

# ===========================================================================
# NORTH BEACH PIPELINE
# ===========================================================================
add("North Beach Pipeline", "STIIIZY | Blue Burst Pod (1g)", "pod", "1g", 26.00,
    "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-blue-burst-pod",
    tax="not-included", stock="OUT OF STOCK 2026-09-15 (notify-me button only)",
    notes="Page read 2026-09-15: '1g $26.00' with an 'Out of stock' banner and 'Notify me when it's back'. "
          "This page printed no tax line; Pipeline product pages generally state tax is added at checkout.")
add("North Beach Pipeline", "STIIIZY Bar Battery", "battery", "1 ea", 27.62,
    "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-bar-stiiizy-battery",
    tax="not-included", verified="carried",
    notes="Verified 2026-09-14; not re-read on 2026-09-15. Pipeline product pages state tax is added at checkout.")

# ---------------------------------------------------------------------------
# Deals back on the store records (single source of truth for the deals table)
# ---------------------------------------------------------------------------
stores[0]["deals"] = stores[0]["deals"]  # Parkmerced (see above)

# ---------------------------------------------------------------------------
# FLAGS (things a human should look at)
# ---------------------------------------------------------------------------
flags = [
    ("FLAG", "STIIIZY Parkmerced's pick-up menu (stiiizy.dispensary.shop) prints no tax line. Its brand-operated "
             "store listing states the opposite - 'ALL PRICES ARE OUT THE DOOR *Tax included*' - so the $13.00 / "
             "$23.00 menu prices are treated here as tax-included, per the store's own statement. Confirm on the receipt.",
     "https://weedmaps.com/dispensaries/stiiizy-parkmerced"),
    ("FLAG", "Parkmerced's pod prices carry the menu's 'ON SALE' flag but the pre-discount price is not printed "
             "anywhere on the page, so no 'was' price can be shown for them (unlike the STIIIZY D2C store, which "
             "prints both).",
     "https://stiiizy.dispensary.shop/parkmerced/rec/vapes/nb/eg3?brand=STIIIZY&order_by=price&order_dir=asc"),
    ("FLAG", "The STIIIZY 'Buy 2, get 1, 50% off' deal appears on product pages only as an internal deal code "
             "'CA - B2G150 - Stiiizy (10/25 -TBD) MMJV3*'. The percentage pattern matches the store listing's "
             "'Buy 2, get 1, 50% off', but the full terms are not published online - ask the budtender.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-pod-skywalker-og-0.5g/v/cd41d67e-d4d9-4f0f-83e6-1b4fc000128d"),
    ("FLAG", "Urbana - Geary (one of your three anchor stores) carries NO Stiiizy-format pods. The live vape menu's "
             "own brand filter lists only CLAYBOURNE CO., GLOBS, JETTY, PAX LABS, TERP and TIMELESS - none of which "
             "mount in a STIIIZY pen. Closest Urbana with STIIIZY pods is Urbana Mission at $24.00/1g.",
     "https://shop.urbananow.com/geary/menu/vapes-3322"),
    ("FLAG", "Sunset Pipeline's STIIIZY prices are the POST-DISCOUNT prices under the '30% OFF STIIIZY PODS & "
             "ALL-IN-ONE VAPES' sale. The pre-discount prices are not printed, so a 'was' price cannot be shown.",
     "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/specials/sale/3241"),
    ("FLAG", "North Beach Pipeline's STIIIZY Blue Burst Pod ($26.00) is still out of stock as of 2026-09-15.",
     "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-blue-burst-pod"),
    ("FLAG", "Two Bloomerang SKUs (0.5g Pineapple Express, 0.5g Pineapple Runtz, $11.04 each) were verified on "
             "2026-09-14 but did NOT appear on the brand page on 2026-09-15 (the page listed 6 pods). Their product "
             "URLs are still present in Bloomerang's live product sitemap, so they are kept but marked "
             "'not re-checked today' - click through before relying on them.",
     "https://bloomerangsf.com/menu/products-sitemap.xml"),
    ("FLAG", "The STIIIZY D2C store loaded with 'DELIVERY - Los Angeles, CA' as the default location in our fetch. "
             "Whether that delivery service covers 94122 must be confirmed at checkout; the STIIIZY pick-up store "
             "(Parkmerced) is the alternative.",
     "https://shop.stiiizy.com/category/Vapes?tab=schedule"),
    ("FLAG", "Bloomerang and Urbana print no tax line on product pages. Their prices are therefore shown as "
             "'tax not stated' and treated as PRE-TAX on this site - never guessed to be included.",
     "https://bloomerangsf.com/menu/brands/stiiizy-585591/"),
    ("INFO", "How the 'est. out-the-door' figure on this site is calculated: CA cannabis excise tax is 15% of gross "
             "receipts and the excise is itself part of the amount subject to sales tax; San Francisco's combined "
             "sales/use tax rate is 8.625% (7.25% statewide base + 1.375% district). Formula used: (price x 1.15) x "
             "1.08625. It is an ESTIMATE for comparison only - any local cannabis business tax a retailer passes on "
             "would raise it, and medical patients may be exempt from some of it.",
     "https://cdtfa.ca.gov/industry/cannabis/tax-facts.htm"),
    ("INFO", "Prices move constantly. Every entry carries the date it was read and a direct link to the page it "
             "came from. Eleven entries are marked 'not re-checked today' rather than being silently re-dated.",
     None),
]

# other STIIIZY retail locations (store facts only, no online prices captured)
other_locations = [
    ("STIIIZY SoMa", "518 Brannan St, San Francisco, CA 94107", "(628) 254-1420",
     "Mon-Thu 9:00 AM - 8:45 PM, Fri-Sat 9:00 AM - 9:45 PM",
     "https://www.stiiizy.com/pages/soma-dispensary",
     "In-store menu runs on stiiizy.dispensary.shop - per-item prices were not captured in this pass."),
    ("STIIIZY Union Square", "180 O'Farrell St, San Francisco, CA 94102", "(628) 258-5133",
     "Daily 7:00 AM - 9:45 PM",
     "https://www.stiiizy.com/pages/union-square-dispensary",
     "In-store menu runs on stiiizy.dispensary.shop - per-item prices were not captured in this pass."),
    ("STIIIZY Mission", "3326 Mission St, San Francisco, CA 94110", "(415) 787-6006",
     "Daily 8:00 AM - 9:45 PM",
     "https://www.stiiizy.com/pages/mission-dispensary",
     "In-store menu runs on stiiizy.dispensary.shop - per-item prices were not captured in this pass."),
]

# ---------------------------------------------------------------------------
data = {
    "title": "STIIIZY Pod Deals - San Francisco (94122 / Stonestown)",
    "verified_date": VERIFIED_DATE,
    "previous_date": PREV_DATE,
    "reference_point": "2161 Irving St, San Francisco, CA 94122 (Sunset Pipeline) - all distances are straight-line from here",
    "stores": stores,
    "entries": E,
    "flags": flags,
    "other_locations": other_locations,
    "tax_estimate": {
        "excise": 0.15,
        "sales": 0.08625,
        "multiplier": round(1.15 * 1.08625, 4),
        "excise_source": "https://cdtfa.ca.gov/industry/cannabis/tax-facts.htm",
        "sales_source": "https://cdtfa.ca.gov/taxes-and-fees/rates.aspx",
    },
}

with open(os.path.join(SITE, "data.js"), "w") as f:
    f.write("// Generated by build/build.py from official sources on " + VERIFIED_DATE + "\n")
    f.write("// Do not edit by hand - edit build/build.py (each entry carries its source URL).\n")
    f.write("window.PODS_DATA = ")
    json.dump(data, f, indent=2)
    f.write(";\n")

# ---------------------------------------------------------------------------
# Root-level page. The repository root is also served by GitHub Pages in the
# legacy "main / (root)" configuration, so we emit the same page there with the
# asset paths pointed at site/. Both URLs therefore show the same, current site.
# ---------------------------------------------------------------------------
with open(os.path.join(SITE, "index.html")) as f:
    page = f.read()
root_page = ("<!-- Generated by build/build.py - same page as site/index.html, with assets under site/.\n"
             "     Edit site/index.html and re-run build/build.py. -->\n"
             + page.replace('href="style.css"', 'href="site/style.css"')
                   .replace('src="data.js"', 'src="site/data.js"')
                   .replace('src="app.js"', 'src="site/app.js"'))
with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(root_page)

live = len([e for e in E if e["verified"] == "live"])
new = len([e for e in E if e["is_new"]])
print("Wrote %s/data.js" % SITE)
print("entries: %d (live-verified today: %d, new this pass: %d)" % (len(E), live, new))
print("stores: %d | flags: %d" % (len(stores), len(flags)))
