#!/usr/bin/env python3
"""Test de fumée : ouvre index.html dans Chromium, parcourt chaque version et chaque onglet,
relève les erreurs JavaScript et les conflits du plan, et prend des captures dans tests/out/.

pip install playwright && playwright install chromium   (une fois)
python3 tests/smoke.py            # bureau 1300 px
python3 tests/smoke.py --mobile   # iPhone 390 px
"""
import asyncio, os, sys, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tests/out"; OUT.mkdir(parents=True, exist_ok=True)
MOBILE = "--mobile" in sys.argv
TABS = ["plan", "v3", "mat", "el", "murs", "res", "buy", "bud", "set"]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist", "--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 390, "height": 844} if MOBILE else {"width": 1300, "height": 1100}, has_touch=MOBILE)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.route("**/cdnjs.cloudflare.com/**", lambda r: r.fulfill(path=str(ROOT / "tests/vendor/three.min.js"), content_type="application/javascript"))
        await pg.route("https://fonts.**", lambda r: r.abort())
        await pg.goto((ROOT / "index.html").as_uri()); await pg.wait_for_timeout(1500)
        presets = await pg.evaluate("Object.keys(PRESETS)")
        for k in presets:
            await pg.click(f'[data-p="{k}"]'); await pg.wait_for_timeout(300)
            await pg.click('[data-tab="plan"]'); await pg.wait_for_timeout(200)
            w = (await pg.inner_text("#warns")).split("\n")[0]
            print(f"{k:12s} {w}")
            for t in TABS:
                await pg.click(f'[data-tab="{t}"]'); await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(OUT / f"{k}_{t}{'_m' if MOBILE else ''}.png"))
        print("Erreurs JS :", errs or "aucune")
        await b.close()
        sys.exit(1 if errs else 0)
asyncio.run(main())
