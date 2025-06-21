from playwright.sync_api import sync_playwright, Playwright
import time
import pandas as pd
import math

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

def scrape(jobs_to_scrape):
    jobs_per_page = 25
    pages = math.ceil(jobs_to_scrape / jobs_per_page)
    
    with sync_playwright() as playwright:
        jobs = {
            'title': [],
            'company': [],
            'description': [], 
            'url': []
        }
        
        # open browser and navigate to jobright
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        context = browser.new_context(storage_state="auth/linkedin_auth.json")
        page = context.new_page()

        page.goto("https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=103644278&keywords=software%20internship&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")
        
        for page_num in range(1, pages + 1):
            ul_locator = page.locator("xpath=//div[contains(@class, 'scaffold-layout__list ')]/div/ul")
            ul_locator.wait_for()
            
            # get job list
            lis = ul_locator.locator("xpath=/li")
            
            for i in range(lis.count()):
                if jobs_to_scrape == 0:
                    break
                li_locator = lis.nth(i) 
                li_locator.click()
            
                title = page.locator("div.job-details-jobs-unified-top-card__job-title").inner_text()
                company = page.locator("div.job-details-jobs-unified-top-card__company-name").inner_text()
                description = page.locator("xpath=//div[@id='job-details']/div[@class='mt4']").inner_text()
                
                print(description)
                
                apply_locator = page.locator("button#jobs-apply-button-id").first
                apply_locator.wait_for()
                apply_text = apply_locator.locator("span.artdeco-button__text").inner_text()
                
                if apply_text == "Apply":
                    try:
                        with page.expect_popup() as popup_info:
                            apply_locator.click()
                        new_page = popup_info.value
                        url = new_page.url
                        new_page.close()
                    except TimeoutError:
                        print("Timeout: No popup appeared within 30 seconds")
                        url = page.url
                elif apply_text == "Easy Apply":
                    url = page.url
                
                jobs['title'].append(title)
                jobs['company'].append(company)
                jobs['description'].append(description)
                jobs['url'].append(url)
                jobs_to_scrape -= 1
                
                page.pause()
            
            # click pagination
            if page_num is not pages:
                pagination_locator = page.locator("ul.jobs-search-pagination__pages")
                pagination_locator.get_by_text(f"{str(page_num + 1)}").click()
                            
        context.close()
        browser.close() 
        
        pd.DataFrame(jobs).to_csv("./jobs.csv", index=False, encoding="utf-8")   
            
if __name__ == '__main__':
    scrape()