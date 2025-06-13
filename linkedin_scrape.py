from playwright.sync_api import sync_playwright
import time

jobs_to_scrape = 10
jobs_per_page = 25

def get_auth():
    """Only need when need to sign into LinkedIn"""
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir="./user-data",
            channel="chrome",
            headless=False,
            no_viewport=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.new_page()
        page.goto("https://www.linkedin.com/")
        
        page.pause()
        
        context.storage_state(path="auth/linkedin_auth.json")

def main():
    with sync_playwright() as playwright:
        # open browser and navigate to jobright
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        context = browser.new_context(storage_state="auth/linkedin_auth.json")
        page = context.new_page()

        page.goto("https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=103644278&keywords=software%20internship&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")
        ul_locator = page.locator("xpath=//div[contains(@class, 'scaffold-layout__list ')]/div/ul")
        ul_locator.wait_for()
        
        # get job list
        lis = ul_locator.locator("xpath=/li")
        for i in range(lis.count()):
            li_locator = lis.nth(i) 
            li_locator.click()
        
            title = page.locator("div.job-details-jobs-unified-top-card__job-title").inner_text()
            company = page.locator("div.job-details-jobs-unified-top-card__company-name").inner_text()
            
            print(title)

        
if __name__ == '__main__':
    main()