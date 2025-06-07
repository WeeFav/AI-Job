from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto("https://stmicroelectronics.eightfold.ai/careers/job/563637158900324?domain=stmicroelectronics.com")
    time.sleep(2)
    page.click("text=Apply now", timeout=10000)
    time.sleep(2)
    elements = page.query_selector_all("input, textarea, select, label, button, a")

    raw_html = []
    for el in elements:
        if el.is_visible():
            html = el.evaluate("el => el.outerHTML")
            raw_html.append(html)
    
    print("\n".join(raw_html))
