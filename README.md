# VapePods — Stiiizy Pod Deals, San Francisco (94122 / Stonestown)

Verified deals on vape pods that fit a **STIIIZY pod pen**, near Stonestown, Sunset Pipeline (Irving St)
and Urbana (Geary Blvd). Every entry lists:

- **base price** and any active deal / sale it's part of
- **tax status** — included, not included, or (honestly) not stated by the store
- **an official link** to the exact product/menu page so you can verify it yourself

## Live site

**https://buffedlizard55-lab.github.io/VapePods/**

Deployed from this branch by `.github/workflows/deploy-pages.yml` (GitHub Actions → `actions/deploy-pages`).

## Snapshot date

Prices verified line-by-line on **2026-09-14** from official store sources only. Cannabis prices change
constantly — re-verify on the linked official page before you go.

## What's inside

| Path | What it is |
| --- | --- |
| `site/index.html` | The static site (single page, no dependencies) |
| `site/style.css` | Styling |
| `site/app.js` | Rendering + filters (store / type / tax / sort) |
| `site/data.js` | Generated master data (entries, stores, flags) — do not edit by hand |
| `build/build.py` | Source of truth: all verified entries, stores, flags; regenerates `site/data.js` |
| `.github/workflows/deploy-pages.yml` | Rebuild + deploy to GitHub Pages on push |

To refresh data: edit `build/build.py` (each entry carries its source URL + how it was verified),
run `python3 build/build.py`, commit, push.

## Verification policy (no hallucinations)

1. **Official sources only** — prices read from the retailer's own domain, or from the search index of
   that official page (such entries are explicitly marked "search index — click to confirm").
2. **Live vs. index** — "live" means the official page was fetched and read during verification.
3. **No third-party prices** — aggregators, deal blogs and unofficial lookalike shops were excluded
   (see the flags section on the site).
4. **Tax status never assumed** — taken from the store's own printed statement; otherwise marked
   "not stated".
5. Distances are straight-line estimates computed from listed addresses.

## Flagged irregularities (summary)

- **Urbana Geary carries no Stiiizy-format pods** online as of the snapshot (24-item menu checked;
  TERP/PAX/Jetty/Claybourne/Globs/Timeless only). Urbana **Mission** (33 29th St) does — STIIIZY 1g pods at $24.
- **stiiizy.com product pages are geo-restricted** from non-CA networks; D2C prices were taken from the
  live `shop.stiiizy.com` pages (tax-included, explicitly marked) with two items from the search index (flagged).
- **STIIIZY Parkmerced in-store menu is a JS app** — per-product prices not machine-verifiable; deal
  graphics are images; the "discounted menu" linktree was down ("Deployment Paused") at check time.
- **North Beach Pipeline STIIIZY Blue Burst pod ($26.00) was out of stock** at check time.
- Sunset Pipeline's listed STIIIZY prices are **post-discount** under their "30% OFF STIIIZY PODS &
  ALL-IN-ONE VAPES" sale; pre-discount prices are not printed (back-calculations are labeled as derivations).
- SF tax stack: 15% CA cannabis excise (CDTFA) + 8.625% SF combined sales tax + SF local cannabis
  business tax (reported 2.5–5%, confirm on receipt).

21+ (18+ with medical). Not affiliated with any store or brand.
