#!/usr/bin/env python3
"""
Build script for the VapePods GitHub Pages site.

MODEL: this file is the single source of truth. Every price below was read from an
official page and is recorded together with (a) the exact URL it came from and
(b) how it was verified. Nothing is inferred, averaged or estimated. If a number
is not printed on the linked page it is not in this file.

Verification levels
-------------------
live-2026-09-15 : the official page was fetched and read during this pass. For
                  STIIIZY Parkmerced SKUs this usually means the store's own menu
                  listing page (which prints name, THC, both prices and the
                  product link); SKUs whose own product page was opened say so in
                  their notes.
live-module     : price read on a related page of the same official site (e.g. a
                  "you might also like" module), not the SKU's own page. Shown
                  with its own chip, never as a plain "read".
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
                     "The store's own pick-up menu now backs that up with item-level deal codes that end in 'OTD' "
                     "(out the door): 'CA - III Daily - .5g OG Pod $10 OTD', 'CA - III Daily - 1g OG Pod $20 OTD' "
                     "and 'CA - III Daily - .5 OG LIIIL $12 OTD'. Those three lines cover the Original pods and the "
                     "0.5g Original all-in-ones only; Liquid Diamonds pods, CBD items and 1g all-in-ones carry no "
                     "OTD code and rely on the store-wide statement. No tax line is printed at add-to-bag - "
                     "confirm on the receipt."),
        "source_status": ("Official STIIIZY store page (stiiizy.com) + STIIIZY's own pick-up menu "
                          "(stiiizy.dispensary.shop, Flowhub platform) + brand-operated Weedmaps store listing - "
                          "all live-fetched 2026-09-15. The vape menu (STIIIZY filter, price ascending) was re-read "
                          "page by page, pages 1-5 of 8, and individual product pages were opened for the SKUs "
                          "noted below. Menu licence line: JBTB HOLDINGS INC C11-0000586-LIC / IRONWORKS COLLECTIVE "
                          "INC C11-0000620-LIC; store licence C10-0000825-LIC. Menu filter counts shifted slightly "
                          "during the day (STIIIZY 149 -> 148, 1g 80 -> 79) - normal menu churn. Pages 6-8 (items "
                          "above $20.00) were not scanned - see flags."),
        "deals": [
            "DAILY (deal code on every Original pod page): 'CA - III Daily - .5g OG Pod $10 OTD (B)' - 0.5g Original pods $10.00 out the door (list $13.00, -23%)",
            "DAILY (deal code on every Original pod page): 'CA - III Daily - 1g OG Pod $20 OTD (B)' - 1g Original pods $20.00 out the door (list $23.00, -13%)",
            "DAILY (deal code on 0.5g Original all-in-one product pages): 'CA - III Daily - .5 OG LIIIL $12 OTD (B)' - 0.5g Original all-in-ones $12.00 out the door (list $16.00, -25%)",
            "Everyday: STIIIZY Buy 2, get 1, 50% off (second deal code on the same pages: 'CA - B2G150 - Stiiizy (10/25 -TBD) MMJV3*')",
            "First-time customers: up to 30% off all STIIIZY products (not valid if you have been to any STIIIZY location before)",
            "Everyday: $10.00 STIIIZY 100mg Edible Mylar (Taxes Included)",
            "Sundays & Wednesdays: $20.00 STIIIZY 3.5g Black Label (Taxes Included)",
            "Happy Hour 4:20pm-7:10pm: Buy 2, Get 1 for $1 - Uncle Arnies",
            "Rewards: 1% back every purchase; 4.20% back every first Friday of the month",
            "Deals page also lists: On Sale, Sessions 3 for $20, Stiiizy Extracts up to 25% off, up to 20% off Crushed Diamonds, up to 25-35% off ABX/Care By Design/Made/WCC/Kingroll/Smokiez/Gramlin",
            "FLAG: the brand-operated listing says the $20 1G OG pod is Sundays & Wednesdays; the store's own menu prints it as a DAILY deal code. Treat $20 as the everyday price but confirm in store.",
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
        "source_status": "Official Urbana site + shop.urbananow.com (Sweed POS) - live-fetched and re-checked 2026-09-15 (second pass of the day). The vape category's own brand filter was read again: still CLAYBOURNE CO., GLOBS, JETTY, PAX LABS, TERP, TIMELESS.",
        "deals": [
            "FLAG (re-confirmed 2026-09-15, second pass): the Geary vape menu carries NO Stiiizy-format pods. The live menu's own brand filter lists only CLAYBOURNE CO., GLOBS, JETTY, PAX LABS, TERP and TIMELESS, and the only sub-categories offered are All In One and Cartridge (510-thread / PAX), none of which mount in a STIIIZY pen.",
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
        "verified": verified, "verified_date": VERIFIED_DATE if verified in ("live", "live-module") else PREV_DATE,
        "notes": notes or "", "compat": compat, "is_new": is_new,
        "distance_miles": st["distance_miles"],
    })


# ===========================================================================
# STIIIZY PARKMERCED  (all live 2026-09-15)
# ===========================================================================
POD_NOTE_PM = ("STIIIZY Parkmerced pick-up menu (stiiizy.dispensary.shop, STIIIZY's own ordering domain), "
               "read 2026-09-15. The page prints BOTH numbers for this item: the struck-through list price and "
               "the price actually charged at add-to-bag - so the 'was' price here is printed by the store, "
               "not inferred.")
POD_NOTE_05 = POD_NOTE_PM + " Same $13.00 -> $10.00 pair printed on every 0.5g Original pod on the menu."
POD_NOTE_05_PDP = POD_NOTE_PM + " Product page read line by line 2026-09-15 (price and both deal codes)."
POD_NOTE_1G_PDP = (POD_NOTE_PM + " Product page read line by line 2026-09-15: 'Each $20.00 $23.00 -13%', "
                   "'Add 1 to Bag - $20.00', both deal codes listed.")
POD_NOTE_LQD = ("Liquid Diamonds pods use the same STIIIZY pod fitting as the Original pods. STIIIZY Parkmerced "
                "pick-up menu (STIIIZY's own ordering domain), read 2026-09-15. The page prints a single price "
                "for this SKU - no 'was' price and no OTD deal code - so only the store-wide 'ALL PRICES ARE OUT "
                "THE DOOR *Tax included*' statement covers its tax treatment.")
POD_NOTE_LQD_PDP = (POD_NOTE_LQD + " Product page read line by line 2026-09-15: 'Each $14.00', "
                    "'Add 1 to Bag - $14.00', only the B2G150 deal code listed.")
POD_NOTE_CBD = ("CBD pod - mounts in a STIIIZY pod pen like the THC pods. STIIIZY Parkmerced pick-up menu "
                "(STIIIZY's own ordering domain), read 2026-09-15. The menu shows a single price with the "
                "'ON SALE' flag for this SKU - no 'was' price and no OTD deal code were read for it, so only "
                "the store-wide 'ALL PRICES ARE OUT THE DOOR *Tax included*' statement covers its tax treatment.")
AIO_NOTE_05 = ("Standalone all-in-one pen - does not mount in a STIIIZY battery. STIIIZY Parkmerced pick-up menu "
               "(stiiizy.dispensary.shop, STIIIZY's own ordering domain), read 2026-09-15. The page prints BOTH "
               "numbers for this item: the struck-through list price and the price actually charged at add-to-bag "
               "- so the 'was' price here is printed by the store, not inferred. Same $16.00 -> $12.00 pair "
               "printed on every 0.5g Original all-in-one on the menu.")
AIO_NOTE_05_PDP = (AIO_NOTE_05 + " Product page read line by line 2026-09-15: 'Each $12.00 $16.00 -25%', "
                   "'Add 1 to Bag - $12.00', both deal codes listed.")
AIO_NOTE_1G = ("Standalone all-in-one pen - does not mount in a STIIIZY battery. STIIIZY Parkmerced pick-up menu "
               "(stiiizy.dispensary.shop, STIIIZY's own ordering domain), read 2026-09-15. The page prints BOTH "
               "numbers for this item: the struck-through list price and the price actually charged at add-to-bag "
               "- so the 'was' price here is printed by the store, not inferred.")
AIO_NOTE_CBD = ("Standalone CBD all-in-one pen - does not mount in a STIIIZY battery. STIIIZY Parkmerced pick-up "
                "menu (STIIIZY's own ordering domain), read 2026-09-15. The menu shows a single price with the "
                "'ON SALE' flag for this SKU - no 'was' price and no OTD deal code were read for it, so only "
                "the store-wide 'ALL PRICES ARE OUT THE DOOR *Tax included*' statement covers its tax treatment.")

DEAL_PM_DAILY_05 = ("Daily deal code on the product page verbatim: 'CA - III Daily - .5g OG Pod $10 OTD (B)' - "
                    "$10.00 out the door for a 0.5g Original pod (list $13.00, -23%)")
DEAL_PM_DAILY_1G = ("Daily deal code on the product page verbatim: 'CA - III Daily - 1g OG Pod $20 OTD (B)' - "
                    "$20.00 out the door for a 1g Original pod (list $23.00, -13%)")
DEAL_PM_DAILY_AIO05 = ("Daily deal code on the product page verbatim: 'CA - III Daily - .5 OG LIIIL $12 OTD (B)' - "
                       "$12.00 out the door for a 0.5g Original all-in-one (list $16.00, -25%)")
DEAL_PM_B2G1 = ("Second deal code listed on the same product page: 'CA - B2G150 - Stiiizy (10/25 -TBD) MMJV3*'; "
                "the store's own listing describes that deal as 'STIIIZY Buy 2, get 1, 50% off'")
DEAL_PM_05 = DEAL_PM_DAILY_05 + " | " + DEAL_PM_B2G1
DEAL_PM_1G = DEAL_PM_DAILY_1G + " | " + DEAL_PM_B2G1
DEAL_PM_AIO05 = DEAL_PM_DAILY_AIO05 + " | " + DEAL_PM_B2G1

PM_PDP = "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/%s/v/%s"


def _pm_slug(kind, strain, size):
    return "stiiizy-%s-%s-%s" % (kind, strain.lower().replace(" ", "-"), size)


# --- 0.5g Original pods: $13.00 -> $10.00 (strain, thc, vid, is_new, own-page-opened) ---
_PM_PODS_05 = [
    ("Skywalker OG", "88.047%", "cd41d67e-d4d9-4f0f-83e6-1b4fc000128d", False, False),
    ("Blue Dream", "86.628%", "08f9f1a0-7343-42fd-8093-3e8d5ad0d3bf", False, False),
    ("OG Kush", "86.377%", "538f49ac-74ce-4a58-8cf3-c23d5051aabc", False, False),
    ("Pineapple Express", "85.833%", "4d161471-c33f-4853-9651-5d13113a7268", False, False),
    ("Super Lemon Haze", "86.393%", "7f9593ed-397c-4f86-9a8f-5cf1d27ffaa5", False, False),
    ("Watermelon Z", "88.001%", "d2a5da32-75c8-4026-a951-875609239f54", False, False),
    ("Gelato", "87.128%", "92aef683-bd57-4f84-8ba9-32db78e0fbb7", False, False),
    ("Strawberry Cough", "84.655%", "167d003a-e732-42f2-9366-a9b0340d09e1", False, False),
    ("Apple Fritter", "87.711%", "4a1efda5-e372-4132-b9f7-84c9b4ddf555", True, True),
    ("Hardcore OG", "88.027%", "ad90637b-f37e-46ce-ad97-1b3979baa839", True, False),
    ("GDP", "86.253%", "d9e0d72c-bf21-483b-841b-78e1e7ad5800", True, False),
    ("King Louis XIII", "84.600%", "cb1fc506-cb26-4345-9761-90821c8ade06", True, False),
    ("SFV OG", "86.386%", "a4fc9960-0e6d-41f3-adc5-a17ce4be6869", True, False),
    ("Strawnana", "85.317%", "a7687bfe-8675-4d0e-93dd-39e011f2934e", True, False),
    ("Do si dos", "85.590%", "d20431aa-0f90-4e03-ae1c-81a9ad8fc0cc", True, False),
    ("Biscotti", "86.371%", "cfcc4d22-328b-4552-b60f-0acc8b7923a2", True, False),
    ("Pink Acai", "85.986%", "284df739-428a-4f30-9012-a1226a538bf1", True, False),
    ("Sour Tangie", "84.895%", "6cef1243-5477-4071-88cd-f7d03b9e8946", True, False),
    # Magic Melon: link corrected 2026-09-15 (...65e1b695c1b0, was ...65e1e695c1b0) - see flags.
    ("Magic Melon", "86.038%", "fbf83bc4-249c-48c8-b91d-65e1b695c1b0", True, False),
    ("Premium Jack", "84.930%", "1bad4584-3f24-4902-afcb-7e0179736cf3", True, False),
    ("White Raspberry", "86.597%", "badd40b2-0fb2-4b1c-8428-ded2ab2ce213", True, False),
    ("Purple Punch", "83.890%", "898a8f09-650d-424f-b2d9-3f54f80cbad3", True, False),
    ("Blue Burst", "83.377%", "ce693c68-d303-4284-89ae-8850af9ff562", True, False),
    # Found on menu page 1 in the closing pass:
    ("Orange Sunset", "85.651%", "8c747c9a-789c-401e-8c74-a7c8729999dc", True, False),
    ("Birthday Cake", "86.361%", "6d497398-8179-495f-bc5e-10b21d2562e2", True, False),
    ("Sour Diesel", "86.131%", "adbc4fcf-7022-4205-be31-e9db8abdb251", True, False),
    ("Pineapple Runtz", "88.088%", "ce5f4f6b-5d88-4cc7-97ca-bc9e3c210ca3", True, False),
]
for strain, thc, vid, isnew, ownpage in _PM_PODS_05:
    add("STIIIZY Parkmerced", "STIIIZY Original Pod - %s (0.5g)" % strain, "pod", "0.5g", 10.00,
        PM_PDP % (_pm_slug("original-pod", strain, "0.5g"), vid),
        price_was=13.00, deal=DEAL_PM_05, thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=isnew,
        notes=POD_NOTE_05_PDP if ownpage else POD_NOTE_05)

# --- 1g Original pods: $23.00 -> $20.00 ---
_PM_PODS_1G = [
    ("OG Kush", "87.774%", "38d3a611-f255-451b-bef5-d02b6d7b83d6", False, True),
    ("Skywalker OG", "87.883%", "d4814a9c-8be1-4576-8426-aed6952a48f8", False, False),
    ("Blue Burst", "83.377%", "20eeac06-0c8e-40c0-8783-15dd237019ef", False, False),
    ("Pineapple Runtz", "87.160%", "b28a7bb7-f8f4-41a6-a9f4-0bf912a75add", True, True),
    ("Strawberry Cough", "84.348%", "84027d77-4aca-407b-b300-fc50071a30a3", True, False),
    # Found on menu page 5 in the closing pass:
    ("Birthday Cake", "83.779%", "76576798-3d96-4b1e-9fe4-98ae5116e33e", True, False),
    ("Super Lemon Haze", "85.696%", "1a301443-93ef-4847-92c2-0009a0f34426", True, False),
    ("Strawnana", "85.975%", "80ecf1cb-d88f-462f-b26e-eae67c701a20", True, False),
    ("Premium Jack", "86.091%", "873e968d-3a67-4085-b1ff-58454c9939cf", True, False),
    ("GDP", "86.758%", "188e5df1-cfb9-4f1d-9a70-5b81be3d6be4", True, False),
    ("Biscotti", "87.689%", "48546ab4-53e4-4a48-926c-9a6d8ac8ec6c", True, False),
    ("Sour Tangie", "85.421%", "c0960d92-7db0-420d-a155-db97b72567ef", True, False),
    ("SFV OG", "85.076%", "d7edd9ff-eaa4-4a14-834f-b4b1ac6422b9", True, False),
    ("Apple Fritter", "86.466%", "f3ea1df5-b807-4366-9314-885fb6a8f246", True, False),
]
for strain, thc, vid, isnew, ownpage in _PM_PODS_1G:
    add("STIIIZY Parkmerced", "STIIIZY Original Pod - %s (1g)" % strain, "pod", "1g", 20.00,
        PM_PDP % (_pm_slug("original-pod", strain, "1g"), vid),
        price_was=23.00, deal=DEAL_PM_1G, thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=isnew,
        notes=POD_NOTE_1G_PDP if ownpage else POD_NOTE_PM)

# --- 0.5g Liquid Diamonds pods: $14.00 flat, B2G150 code only (no OTD code) ---
_PM_PODS_LQD = [
    ("Strawberry Milkshake", "78.073%", "03ca8ce9-e213-420a-99d3-88a18b051dc1", True, True),
    ("Green Crack", "79.617%", "746efec8-fb8b-4aae-9a57-871e308f860e", True, False),
    ("Hawaiian Snow", "78.771%", "982c8573-579f-463f-b60e-69aafda6102f", True, False),
    # Found on menu pages 3-4 in the closing pass (Cereal Milk's own page opened):
    ("Cereal Milk", "77.906%", "5cbcc351-9050-42ba-8101-a008bed3dde1", True, True),
    ("White Widow", "80.475%", "53eb6750-a0a3-4e34-9301-99a8cdff552c", True, False),
    ("Lemon Cherry Gelato", "77.514%", "91a8d6f6-a01a-4e13-b0ef-8016c28be7c1", True, False),
    ("Northern Lights", "78.419%", "01cfe14c-c8ae-4f63-b736-bb105d570048", True, False),
    ("Pink Runtz", "79.330%", "0007a6aa-f048-4567-9922-d25ba3fbdb45", True, False),
    ("Purple Haze", "79.389%", "be2c3c3c-01d2-4b05-b2b3-04fb3901f4eb", True, False),
    ("Strawberry Shortcake", "77.809%", "f668bf79-2e5c-4113-8570-c6738e4e597c", True, False),
    ("Tahoe OG", "76.398%", "21e3a806-7d12-450b-a855-dc3aebe2a9cb", True, False),
    ("Purple Zlushie", "78.251%", "47050ec0-c2e0-49d3-8e73-1e6a4df75a51", True, False),
]
for strain, thc, vid, isnew, ownpage in _PM_PODS_LQD:
    add("STIIIZY Parkmerced", "STIIIZY Liquid Diamonds Pod - %s (0.5g)" % strain, "pod", "0.5g", 14.00,
        PM_PDP % (_pm_slug("liquid-diamonds-pod", strain, "0.5g"), vid),
        deal=DEAL_PM_B2G1, thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=isnew,
        notes=POD_NOTE_LQD_PDP if ownpage else POD_NOTE_LQD)

# --- 0.5g CBD pods: $15.00 flat (menu page 4, closing pass) ---
_PM_PODS_CBD = [
    ("Mango", "45.377% THC / 40.557% CBD", "78e76631-db1d-4e26-a719-e0cb38c894d8"),
    ("Juicy Melon", "44.529% THC / 40.058% CBD", "df102289-97eb-4a2c-9b83-00c59adb9407"),
]
for strain, thc, vid in _PM_PODS_CBD:
    add("STIIIZY Parkmerced", "STIIIZY CBD Pod - %s (0.5g)" % strain, "pod", "0.5g", 15.00,
        PM_PDP % (_pm_slug("cbd-pod", strain, "0.5g"), vid),
        thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=True, notes=POD_NOTE_CBD)

# --- 0.5g Original all-in-ones: $16.00 -> $12.00 (menu pages 2-3, closing pass) ---
_PM_AIO_05 = [
    ("SFV OG", "85.076%", "8b6f43bd-0e02-40fa-8801-85c3ef451237", False),
    ("Birthday Cake", "86.566%", "b6bf1c22-670d-40e1-bb89-40cf61d6211b", False),
    ("Blue Burst", "85.420%", "18348c5d-a94e-4b03-98ba-52b21cf5ab6b", False),
    ("Do si dos", "87.823%", "1d2681d9-d8f0-4441-9b0c-28ffbe4d4809", False),
    ("Sour Tangie", "84.895%", "ec0fe882-971c-4486-bd5e-712698e08f46", True),
    ("Pineapple Express", "87.762%", "f64b2d4e-acb3-4850-8405-306ab65859a4", True),
    ("Pink Acai", "83.751%", "c72b876c-b1a4-4e13-a3a3-2129470b16b5", False),
    ("Hardcore OG", "88.693%", "1f1a80ef-6c4f-48dd-ab2b-34104d7e2136", False),
    ("Watermelon Z", "85.724%", "7d45da18-7cf8-4260-b070-3e3b1e027287", False),
    ("Biscotti", "84.624%", "bfc561ec-28e2-4b95-8cba-aed3ee6b6c30", False),
    ("Orange Sunset", "87.681%", "eef79d8a-e5a4-42a9-927d-1dab5236da57", False),
    ("Premium Jack", "87.701%", "467a972a-7819-4a74-95ca-51d48dc76218", False),
    ("Purple Punch", "85.434%", "bd3e612c-6615-43e1-bd40-f1615e3cb053", False),
    ("Pineapple Runtz", "85.760%", "a6143619-5ade-474a-9ba7-d34b1847c3dd", False),
    ("King Louis XIII", "86.312%", "cef227e2-8d05-4fee-8f8b-bcc3b201ee3f", False),
    ("Apple Fritter", "86.598%", "e5c196c2-8c2e-457f-9950-67d5228626a9", False),
    ("White Raspberry", "85.240%", "c9182551-4b21-4545-a98b-f769fae44c11", False),
    ("GDP", "87.488%", "7464ff32-4d84-456e-8633-783f02a8fb27", False),
    ("Strawberry Cough", "84.289%", "91ed79cc-216d-40ca-a438-5997e36111cd", False),
    ("Gelato", "87.128%", "3f8be944-5050-4251-872c-972c71716b2c", False),
    ("OG Kush", "86.630%", "e4e9c01d-5b24-4f54-af73-0e91645ffda2", False),
    ("Skywalker OG", "89.613%", "3e87bc74-39a5-4d58-bc5b-09a51cff4b88", False),
    ("Blue Dream", "85.447%", "4a1ee000-a3a2-4ccf-83bc-c29740b65408", False),
    ("Sour Diesel", "86.258%", "e5f5ef08-6e7f-4681-b595-44722f43ba20", False),
    ("Magic Melon", "86.224%", "b3f4f0a9-bd6d-44dc-a6f8-f084a675d842", False),
    ("Strawnana", "85.368%", "0e8847bf-ca65-4131-b562-6282754e4918", False),
]
for strain, thc, vid, ownpage in _PM_AIO_05:
    add("STIIIZY Parkmerced", "STIIIZY Original All-In-One - %s (0.5g)" % strain, "aio", "0.5g", 12.00,
        PM_PDP % (_pm_slug("original-all-in-one", strain, "0.5g"), vid),
        price_was=16.00, deal=DEAL_PM_AIO05, thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=True,
        notes=AIO_NOTE_05_PDP if ownpage else AIO_NOTE_05)

# --- 0.5g CBD all-in-ones: $16.00 flat (menu page 4, closing pass) ---
_PM_AIO_CBD = [
    ("Mango", "45.053% THC / 40.562% CBD", "a4d7e099-b159-4ebe-913c-2f190573f790"),
    ("Juicy Melon", "43.246% THC / 39.746% CBD", "39d43771-ee39-485c-b596-c8d09d0e9074"),
]
for strain, thc, vid in _PM_AIO_CBD:
    add("STIIIZY Parkmerced", "STIIIZY CBD All-In-One - %s (0.5g)" % strain, "aio", "0.5g", 16.00,
        PM_PDP % (_pm_slug("cbd-all-in-one", strain, "0.5g"), vid),
        thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=True, notes=AIO_NOTE_CBD)

# --- 1g Original all-in-ones: $23.00 -> $20.00 (menu pages 4-5, closing pass) ---
# NOTE: the Watermelon Z row below predates the closing pass and is kept verbatim (see flags).
add("STIIIZY Parkmerced", "STIIIZY Original All-In-One - Watermelon Z (1g)", "aio", "1g", 23.00,
    "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-all-in-one-watermelon-z-1g/v/e365c19e-ae4b-4b37-b399-f85816e6f3c8",
    thc="87.481%", stock="In stock (menu shows ON SALE)", source_kind="official-brand-menu",
    notes=AIO_NOTE_1G)
_PM_AIO_1G = [
    ("Hardcore OG", "88.027%", "248074fc-6d4d-4525-8018-bb29f03c70d0"),
    ("Biscotti", "86.769%", "82ef9fd7-f511-4860-b410-c9b35926659a"),
    ("SFV OG", "85.882%", "a9fbcc56-2a33-4d8c-bbd4-853873d5f975"),
    ("Birthday Cake", "85.391%", "52bba187-54dd-4050-a725-572ef52d9a81"),
    ("Pineapple Runtz", "88.088%", "43fac682-9863-4776-86cd-0aed0cb7138d"),
    ("Strawnana", "82.861%", "bcd3b068-ea7c-4d0b-bf1e-a52e0a939a4a"),
    ("Strawberry Cough", "83.835%", "91cc36a7-2ad2-4fff-8b0f-84b7607f021f"),
    ("Pink Acai", "85.804%", "1ae29b06-51fb-4dfd-b221-debac03f5a86"),
    ("GDP", "82.810%", "9490a34b-8da6-4756-b368-c056683818cb"),
    ("White Raspberry", "85.146%", "43bf65c4-14ae-4eb3-9d82-0274d51388af"),
    ("Do si dos", "87.281%", "ff00b9e0-b87f-46bd-b693-dca2cf237ce8"),
    ("Blue Dream", "84.395%", "02c20678-5500-4298-971c-61ec140f04a8"),
    ("Super Lemon Haze", "86.393%", "afa5efdc-1dab-49c7-9c97-5bf9a119eb4b"),
    ("Purple Punch", "87.014%", "0062d381-ff3c-439b-9e91-5cd7922c75a6"),
    ("Sour Diesel", "88.202%", "eaf99f51-39c3-4358-bd97-7d207c0e5748"),
    ("Apple Fritter", "86.466%", "cfae6044-1070-464f-8d7c-afb12d06f092"),
    ("King Louis XIII", "84.600%", "65828c59-c439-4f8f-8344-59376cc5bdc3"),
    ("Orange Sunset", "85.880%", "2012fb6d-4e01-484b-9bd6-3367a3777170"),
    ("Premium Jack", "83.801%", "21601fc6-e795-4f9e-8baf-e2abcded6f6c"),
    ("Magic Melon", "84.716%", "71909b29-af85-43e7-ac85-a4409a57abd5"),
    ("Gelato", "88.018%", "559e1827-bd2b-4453-bb0b-1acc5de7e6e6"),
]
for strain, thc, vid in _PM_AIO_1G:
    add("STIIIZY Parkmerced", "STIIIZY Original All-In-One - %s (1g)" % strain, "aio", "1g", 20.00,
        PM_PDP % (_pm_slug("original-all-in-one", strain, "1g"), vid),
        price_was=23.00, thc=thc, stock="In stock (menu shows ON SALE)",
        source_kind="official-brand-menu", is_new=True, notes=AIO_NOTE_1G)

# 1g OG pod weekly deal (brand-operated store listing) - kept as the tax-wording source
add("STIIIZY Parkmerced", "STIIIZY 1G OG Pod - $20 out-the-door deal (store listing wording)", "pod", "1g", 20.00,
    "https://weedmaps.com/dispensaries/stiiizy-parkmerced", tax="included",
    deal="Store listing: '$20.00 STIIIZY 1G OG Pod (Taxes Included)', listed under Sundays & Wednesdays - "
         "but the store's own menu shows the $20.00 as a DAILY deal code ('CA - III Daily - 1g OG Pod $20 OTD')",
    stock="In stock", source_kind="brand-listing",
    notes=("Price and the '(Taxes Included)' wording are quoted from STIIIZY Parkmerced's brand-operated store "
           "listing, read 2026-09-15. This entry is kept as the source for the tax-included wording only; the "
           "per-strain 1g pod entries above are priced from the store's own menu, which shows $20.00 every day "
           "of the week. FLAG: the listing says Sun & Wed, the store's own menu says Daily - ask in store."))

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

add("Sunset Pipeline", "Northern Lights Live Resin Pod (1g)", "pod", "1g", 26.42,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/northern-lights-live-resin-pod-1g-65890",
    tax="not-included", deal=SP_DEAL, thc="86.75%", stock="In stock",
    notes="Product page read line by line 2026-09-15: '1g $26.42'. " + SP_TAXNOTE)
add("Sunset Pipeline", "Super Lemon Haze Original Pod (1g)", "pod", "1g", 24.82,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/super-lemon-haze-original-pod-1g-45669",
    tax="not-included", deal=SP_DEAL, thc="85.7%", stock="In stock", notes=SP_TAXNOTE)
add("Sunset Pipeline", "Cereal Milk Live Resin Pod (1g)", "pod", "1g", 26.42,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/cereal-milk-live-resin-pod-1g-55297",
    tax="not-included", deal=SP_DEAL, thc="85.97%", stock="In stock", notes=SP_TAXNOTE)
add("Sunset Pipeline", "Strawberry Shortcake Live Resin Diamonds Pod (1g)", "pod", "1g", 26.42,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/strawberry-shortcake-live-resin-diamonds-stiiizy-pod",
    tax="not-included", deal=SP_DEAL, thc="86.87%", stock="In stock", notes=SP_TAXNOTE)
add("Sunset Pipeline", "STIIIZY BAR battery (dual-pod battery)", "battery", "1 ea", 24.02,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/stiiizy-stiiizy-bar",
    tax="not-included", stock="In stock",
    notes="Hardware: holds two 1g STIIIZY pods. " + SP_TAXNOTE)

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

# Two more sale-page all-in-ones, own product pages opened in the closing pass
add("Sunset Pipeline", "Pineapple Express All-In-One (1g)", "aio", "1g", 28.82,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/pineapple-express-stiiizy-all-in-one",
    tax="not-included", deal=SP_DEAL, thc="85.4%", stock="In stock", is_new=True,
    notes="Product page read line by line 2026-09-15: '1g $28.82', THC 85.4%, CBD 0.21%. " + SP_TAXNOTE)
add("Sunset Pipeline", "Purple Haze Live Resin Diamonds All-In-One (1g)", "aio", "1g", 32.02,
    "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/product/purple-haze-live-resin-diamonds-stiiizy-all-in-one",
    tax="not-included", deal=SP_DEAL, thc="83.31%", stock="In stock", is_new=True,
    notes="Product page read line by line 2026-09-15: '1g $32.02', THC 83.31%, CBD 0.19%. " + SP_TAXNOTE)

# ===========================================================================
# BLOOMERANG (live 2026-09-15 unless noted)
# ===========================================================================
BR_NOTE = ("Bloomerang product pages print no tax line - treat as PRE-TAX until the receipt says otherwise. "
           "Verified live 2026-09-15. FLAG: the STIIIZY brand page itself lists only 6 pods (all 0.5g); the 1g "
           "pods and several 0.5g pods are reachable only from their own product URLs or from the store's 'More "
           "by STIIIZY' / related-products modules, so each one is dated by the page it was actually read on.")
BR_BRANDPAGE = BR_NOTE + " Price re-read on the STIIIZY brand page on 2026-09-15."
BR_OWNPAGE = BR_NOTE + " Price re-read on the store's own product page on 2026-09-15."
BR_CARRIED_05 = (BR_NOTE + " Price read 2026-09-14; the SKU did not appear on the brand page on 2026-09-15 and "
                 "its own product page was not re-opened, so it is marked not re-checked today.")
BR_MODULE = (BR_NOTE + " Price and THC read 2026-09-15 from the 'You might also like' module on another "
              "Bloomerang product page (the store's own page), NOT from this SKU's own product page - click "
              "through to confirm before buying.")
BR_LIVE_1G = (BR_NOTE + " Own product page opened and read line by line 2026-09-15: '$19.33', "
              "'1 unit x $19.33 = $19.33'.")
BR_CARRIED_1G = (BR_NOTE + " Price read 2026-09-14; the SKU is not listed on the brand page on 2026-09-15 and "
                 "its own product page was not re-opened, so it is marked not re-checked today.")

BR_URL = "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/%s/"
# (strain, thc, slug, verified, is_new, notes)
_br_05 = [
    ("GDP", "84.03%", "05g-gdp-premium-thc-pod-stiiizy-6081732", "live", False, BR_BRANDPAGE),
    ("Biscotti", "85.1%", "05g-biscotti-premium-thc-pod-stiiizy-6081728", "live", False, BR_BRANDPAGE),
    ("Apple Fritter", "88.56%", "05g-apple-fritter-premium-thc-pod-stiiizy-6081726", "live", False, BR_BRANDPAGE),
    ("Strawnana", "87.35%", "05g-strawnana-premium-thc-pod-stiiizy-6081749", "live", False, BR_BRANDPAGE),
    ("Strawberry Cough", "86.42%", "05g-strawberry-cough-premium-thc-pod-stiiizy-6081748", "live", False, BR_BRANDPAGE),
    ("Skywalker OG", "89.82%", "05g-skywalker-og-premium-thc-pod-stiiizy-6081745", "live", False, BR_BRANDPAGE),
    ("Premium Jack", "87.66%", "05g-premium-jack-premium-thc-pod-stiiizy-6081742", "live", False, BR_OWNPAGE),
    ("Pineapple Express", "89.58%", "05g-pineapple-express-premium-thc-pod-stiiizy-6081740", "live", False, BR_OWNPAGE),
    ("OG Kush", "86.71%", "05g-og-kush-premium-thc-pod-stiiizy-6081738", "live", True, BR_BRANDPAGE),
    ("Orange Sunset", "85.5%", "05g-orange-sunset-premium-thc-pod-stiiizy-6081739", "carried", False, BR_CARRIED_05),
    ("Pineapple Runtz", "84.01%", "05g-pineapple-runtz-premium-thc-pod-stiiizy-6562326", "carried", False, BR_CARRIED_05),
    ("Blue Burst", "85.86%", "05g-blue-burst-premium-thc-pod-stiiizy-6157192", "live-module", True, BR_MODULE),
]
for strain, thc, slug, verified, isnew, notes in _br_05:
    add("Bloomerang", "0.5g %s / Premium THC Pod / STIIIZY" % strain, "pod", "0.5g", 11.04,
        BR_URL % slug, tax="not-stated", thc=thc, stock="In stock",
        verified=verified, is_new=isnew, notes=notes)

_br_1g = [
    ("OG Kush", "88.32%", "1g-og-kush-premium-thc-pod-stiiizy-6082043", "live", False, BR_LIVE_1G),
    ("Birthday Cake", "83.54%", "1g-birthday-cake-premium-thc-pod-stiiizy-6157198", "live", True, BR_LIVE_1G),
    ("Skywalker OG", "87.7%", "1g-skywalker-og-premium-thc-pod-stiiizy-6157204", "live", True, BR_LIVE_1G),
    ("Do-Si-Dos", "86.11%", "1g-do-si-dos-premium-thc-pod-stiiizy-8682066", "live", True, BR_LIVE_1G),
    ("Watermelon Z", "85.35%", "1g-watermelon-z-premium-thc-pod-stiiizy-6082089", "carried", False, BR_CARRIED_1G),
    ("Strawberry Cough", "85.61%", "1g-strawberry-cough-premium-thc-pod-stiiizy-6082071", "carried", False, BR_CARRIED_1G),
]
for strain, thc, slug, verified, isnew, notes in _br_1g:
    if strain == "Do-Si-Dos":
        notes = notes + (" FLAG: the store's page for Do-Si-Dos carries the Birthday Cake strain description "
                         "(copy/paste error on the retailer's own page) - the product name, THC and price are "
                         "consistent, the flavour text is not.")
    add("Bloomerang", "1g %s / Premium THC POD / STIIIZY" % strain, "pod", "1g", 19.33,
        BR_URL % slug, tax="not-stated", thc=thc, stock="In stock",
        verified=verified, is_new=isnew, notes=notes)

add("Bloomerang", "1g AIO Premium Jack / Disposable Pen / STIIIZY", "aio", "1g", 20.25,
    "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/1g-aio-premium-jack-disposable-pen-stiiizy-7795879/",
    tax="not-stated", thc="80.56%", stock="In stock",
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
    ("OG Kush ORG Pod (1g)", "87.76%", "In stock", False),
]
for prod, thc, stock, isnew in _um:
    add("Urbana - Mission", prod, "pod", "1g", 24.00, UM, tax="not-stated", thc=thc, stock=stock,
        is_new=isnew, notes=UM_NOTE)
add("Urbana - Mission", "White Widow LQD Pod (Live Resin Liquid Diamonds, 1g)", "pod", "1g", 26.00,
    UM, tax="not-stated", thc="84.43-86.46%", stock="In stock", notes=UM_NOTE)

# more STIIIZY pods read on the same live menu page (chunk 2)
_um2 = [
    ("Skywalker OG ORG Pod (1g)", 24.00, "88.03%", "In stock", "pod-hybrid-skywalker-og-org-pod-1g-179475"),
    ("White Raspberry Org Pod (1g)", 24.00, "87.22%", "Only 7 left", "pod-indica-white-raspberry-org-pod-1g-179459"),
    ("Gelato ORG Pod (1g)", 24.00, "87.71-88.83%", "In stock", "pod-hybrid-gelato-org-pod-1g-284683"),
    ("Mango CBD ORG Pod (1g)", 26.00, "45.77% THC / 38.44% CBD", "Only 8 left", "pod-cbd-mango-cbd-org-pod-1g-179537"),
    ("Northern Lights Lqd Pod (1g)", 26.00, "85.06-87.49%", "Only 9 left", "pod-indica-northern-lights-lqd-pod-1g-179566"),
]
for prod, price, thc, stock, slug in _um2:
    add("Urbana - Mission", prod, "pod", "1g", price, UM + "/" + slug, tax="not-stated",
        thc=thc, stock=stock, is_new=False, notes=UM_NOTE)

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
    tax="included", verified="live", is_new=False,
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
    tax="not-included", stock="OUT OF STOCK (re-confirmed 2026-09-15 - notify-me button only)",
    notes="Page re-opened and read again 2026-09-15: still '1g $26.00' with an 'Out of stock' banner and 'Notify "
          "me when it's back'. This page printed no tax line and no THC value (CBD 0.52% only); Pipeline product "
          "pages generally state tax is added at checkout.")
add("North Beach Pipeline", "STIIIZY Bar Battery", "battery", "1 ea", 27.62,
    "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-bar-stiiizy-battery",
    tax="not-included", verified="carried",
    notes="Verified 2026-09-14; not re-read on 2026-09-15. Pipeline product pages state tax is added at checkout.")

# ---------------------------------------------------------------------------
# FLAGS (things a human should look at)
# ---------------------------------------------------------------------------
flags = [
    ("FLAG", "PRICE CORRECTION vs the earlier snapshot taken earlier today (2026-09-15): STIIIZY Parkmerced's own "
             "product pages now print a struck-through list price AND the price charged - 0.5g Original pods 'Each "
             "$10.00 $13.00 -23%' with 'Add 1 to Bag - $10.00', and 1g Original pods 'Each $20.00 $23.00 -13%' with "
             "'Add 1 to Bag - $20.00'. The earlier pass listed $13.00 / $23.00 as the price charged. Either the "
             "price moved during the day or the earlier read picked up the list price; the numbers in this table "
             "are the add-to-bag prices read off the product pages on 2026-09-15.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-pod-apple-fritter-0.5g/v/4a1efda5-e372-4132-b9f7-84c9b4ddf555"),
    ("FLAG", "'OTD' (out the door) is the store's OWN shorthand on Parkmerced's menu deal codes - 'CA - III Daily - "
             ".5g OG Pod $10 OTD (B)' and 'CA - III Daily - 1g OG Pod $20 OTD (B)'. It is supported by the store's "
             "brand-operated listing, which states 'ALL PRICES ARE OUT THE DOOR *Tax included*'. The check-out "
             "screen itself still prints no tax line, so the receipt is the final word.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-pod-og-kush-1g/v/38d3a611-f255-451b-bef5-d02b6d7b83d6"),
    ("FLAG", "The $20.00 1g OG pod is described on the store's brand-operated listing as a SUNDAYS & WEDNESDAYS "
             "offer, but the store's own menu carries it as a DAILY deal code ('CA - III Daily - 1g OG Pod $20 "
             "OTD'). Both sources are the store's; they disagree on the days. This site prices 1g Original pods "
             "at $20.00 every day - confirm the days in store before relying on it.",
     "https://weedmaps.com/dispensaries/stiiizy-parkmerced"),
    ("FLAG", "Parkmerced's Liquid Diamonds pods ($14.00 / 0.5g) carry NO 'OTD' deal code - only the store-wide 'ALL "
             "PRICES ARE OUT THE DOOR *Tax included*' statement covers them, and they print no 'was' price. Their "
             "tax treatment is therefore inferred from the store-level statement, not from an item-level line.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-liquid-diamonds-pod-strawberry-milkshake-0.5g/v/03ca8ce9-e213-420a-99d3-88a18b051dc1"),
    ("FLAG", "The STIIIZY 'Buy 2, get 1, 50% off' deal appears on product pages only as an internal deal code "
             "'CA - B2G150 - Stiiizy (10/25 -TBD) MMJV3*'. The percentage pattern matches the store listing's 'Buy "
             "2, get 1, 50% off', but the full terms are not published online - ask the budtender.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-pod-pineapple-runtz-1g/v/b28a7bb7-f8f4-41a6-a9f4-0bf912a75add"),
    ("FLAG", "Urbana - Geary (one of your three anchor stores) carries NO Stiiizy-format pods. Re-checked on "
             "2026-09-15: the live vape menu's own brand filter lists only CLAYBOURNE CO., GLOBS, JETTY, PAX LABS, "
             "TERP and TIMELESS, and its only sub-categories are All In One and 510-thread Cartridge - none of "
             "which mount in a STIIIZY pen. Closest Urbana with STIIIZY pods is Urbana Mission at $24.00/1g.",
     "https://shop.urbananow.com/geary/menu/vapes-3322"),
    ("FLAG", "Sunset Pipeline's STIIIZY prices are the POST-DISCOUNT prices under the '30% OFF STIIIZY PODS & "
             "ALL-IN-ONE VAPES' sale (re-read line by line on 2026-09-15 in this pass - all 22 items still show "
             "the same prices as the morning read). The pre-discount prices are not printed, so a 'was' price "
             "cannot be shown, and tax is added at checkout.",
     "https://www.pipelinedispensary.com/stores/sunset-pipeline-dispensary/specials/sale/3241"),
    ("FLAG", "Bloomerang's STIIIZY brand page lists only SIX pods (all 0.5g, $11.04). The 1g pods and several 0.5g "
             "pods exist only at their own product URLs. Two Bloomerang pages also carry the wrong strain "
             "description (the 1g Do-Si-Dos page prints the Birthday Cake description; the 0.5g Premium Jack page "
             "prints the Pineapple Express description) - product name, THC and price are consistent, the flavour "
             "text is not.",
     "https://bloomerangsf.com/menu/brands/stiiizy-585591/"),
    ("FLAG", "North Beach Pipeline's STIIIZY Blue Burst Pod ($26.00) is still out of stock - re-confirmed "
             "2026-09-15 ('Notify me when it's back'). The page prints no tax line and no THC value (CBD 0.52% "
             "only); Pipeline product pages generally state tax is added at checkout.",
     "https://www.pipelinedispensary.com/stores/north-beach-pipeline/product/stiiizy-blue-burst-pod"),
    ("FLAG", "Four Bloomerang SKUs (0.5g Orange Sunset, 0.5g Pineapple Runtz at $11.04 and 1g Watermelon Z / 1g "
             "Strawberry Cough at $19.33) were read on 2026-09-14 but were NOT re-opened on 2026-09-15. They are "
             "kept and marked 'not re-checked today' - click through before relying on them.",
     "https://bloomerangsf.com/menu/brands/stiiizy-585591/"),
    ("FLAG", "One new Bloomerang SKU (0.5g Blue Burst, $11.04) was priced from the store's related-products module "
             "on another Bloomerang product page, not from its own product page. It is labelled 'read on a "
             "related page' rather than 'read' - open its own page before buying.",
     "https://bloomerangsf.com/menu/products/stiiizy-585591/vapes/05g-og-kush-premium-thc-pod-stiiizy-6081738/"),
    ("FLAG", "Bloomerang and Urbana print no tax line on product pages. Their prices are therefore shown as "
             "'tax not stated' and treated as PRE-TAX on this site - never guessed to be included.",
     "https://bloomerangsf.com/menu/brands/stiiizy-585591/"),
    ("FLAG", "The STIIIZY D2C store loaded with 'DELIVERY - Los Angeles, CA' as the default location in our fetch. "
             "Whether that delivery service covers 94122 must be confirmed at checkout; the STIIIZY pick-up store "
             "(Parkmerced) is the alternative.",
     "https://shop.stiiizy.com/category/Vapes?tab=schedule"),
    ("INFO", "How the 'est. out-the-door' figure on this site is calculated: CA cannabis excise tax is 15% of gross "
             "receipts and the excise is itself part of the amount subject to sales tax; San Francisco's combined "
             "sales/use tax rate is 8.625% (7.25% statewide base + 1.375% district). Formula used: (price x 1.15) x "
             "1.08625. It is an ESTIMATE for comparison only - any local cannabis business tax a retailer passes on "
             "would raise it, and medical patients may be exempt from some of it.",
     "https://cdtfa.ca.gov/industry/cannabis/tax-facts.htm"),
    ("INFO", "Prices move constantly - two prices on this list moved during a single day. Every entry carries the "
             "date it was read, how it was read, and a direct link to the page it came from. Entries not re-opened "
             "in the latest pass say so instead of being silently re-dated.",
     None),
    ("FLAG", "CORRECTION to the earlier snapshot: its Magic Melon 0.5g pod link ended ...65e1e695c1b0, but the "
             "store's own menu links ...65e1b695c1b0 (one character differs) and that product page loads correctly "
             "('Magic Melon - 0.5g', $10.00, THC 86.038%). The link in this table is the corrected one.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-pod-magic-melon-0.5g/v/fbf83bc4-249c-48c8-b91d-65e1b695c1b0"),
    ("FLAG", "COVERAGE: STIIIZY Parkmerced's vape menu (STIIIZY filter, price ascending) runs to 8 pages; only "
             "pages 1-5 (everything up to $20.00: all 0.5g pods and all-in-ones, Liquid Diamonds 0.5g, CBD items, "
             "and the first 1g pods/all-in-ones) were read line by line in this pass. Pages 6-8 (higher-priced 1g "
             "items) were NOT scanned, so any SKUs living there are missing from this table rather than verified "
             "absent.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/vapes/nb/eg3?brand=STIIIZY&order_by=price&order_dir=asc&page=6"),
    ("FLAG", "The Watermelon Z 1g all-in-one is listed here at $23.00 from the earlier read, but every other 1g "
             "Original all-in-one on menu pages 4-5 shows $23.00 -> $20.00, and this row's own notes say both "
             "numbers are printed while recording no 'was' price. Re-open the product page before relying on the "
             "$23.00.",
     "https://stiiizy.dispensary.shop/parkmerced/rec/cartridges/pdp/stiiizy-original-all-in-one-watermelon-z-1g/v/e365c19e-ae4b-4b37-b399-f85816e6f3c8"),
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
