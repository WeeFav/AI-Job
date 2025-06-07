from playwright.sync_api import sync_playwright
import time

def get_auth():
    """Only need when need to sign into google"""
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir="./user-data",
            channel="chrome",
            headless=False,
            no_viewport=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.new_page()
        page.goto("https://jobright.ai/jobs/recommend")
        
        page.pause()
        
        context.storage_state(path="auth.json")
    
def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()
        page.goto("https://jobright.ai/jobs/info/6843a5ecc28f21afd582aad4")
        # page.goto("https://jobright.ai/jobs/recommend")
        # page.click("xpath=//*[@id='6843a5ecc28f21afd582aad4']")
        apply_url = page.locator("a.index_origin__7NnDG").get_attribute("href")
        print(apply_url)
        
if __name__ == '__main__':
    main()