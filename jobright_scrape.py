from playwright.sync_api import sync_playwright
import time

jobs_to_scrape = 10
jobs_per_page = 10

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
        # open browser and navigate to jobright
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()

        page.goto("https://jobright.ai/jobs/recommend")
        
        # scroll until all jobs are visible
        scroll_locator = page.locator("div#scrollableDiv")
        scroll_locator.wait_for()
        ul_locator = page.locator("ul.ant-list-items")
        ul_locator.wait_for()
        
        for i in range(jobs_to_scrape // jobs_per_page):
            scroll_locator.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")
            time.sleep(2) # wait for jobs to load
        
        # get job list
        divs = ul_locator.locator("xpath=/div")
        job_ids = [divs.nth(i).get_attribute("id") for i in range(divs.count())]
        # scape each job
        for job_id in job_ids:
            page.goto(f"https://jobright.ai/jobs/info/{job_id}")
            company = page.locator("h2.index_company-row__vOzgg").inner_text().split("\n")[0]
            title = page.locator("h1.index_job-title__sStdA").text_content()
            apply_url = page.locator("a.index_origin__7NnDG").get_attribute("href")
            print("Company:", company)
            print("Title:", title)
            print("URL: ", apply_url)
        
        # page.click("xpath=//*[@id='6843a5ecc28f21afd582aad4']")

        
if __name__ == '__main__':
    main()