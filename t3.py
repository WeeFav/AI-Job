from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto("https://geaerospace.wd5.myworkdayjobs.com/GE_ExternalSite/job/Evendale/AI-Digital-Technology-Intern_R5009391")
    page.get_by_role("button", name="Apply").click()