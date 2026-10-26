# -*- coding: utf-8 -*-
"""Playwright screenshot renderer: HTML -> 1920x1080 PNG.

Usage: python render.py <html_path> <out_png>
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def render(html_path: str, out_png: str, width: int = 1920, height: int = 1080) -> None:
    html_path = Path(html_path).resolve()
    out_png = Path(out_png).resolve()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
        )
        page.goto(html_path.as_uri())
        page.wait_for_timeout(1200)  # let fonts/images settle
        page.screenshot(path=str(out_png), type="png")
        browser.close()
    print(f"OK -> {out_png}")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
