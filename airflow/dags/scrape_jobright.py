from playwright.sync_api import sync_playwright, Error
import time
import math
import pandas as pd

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
        
        context.storage_state(path="auth/jobright_auth.json")
    
def scrape_jobright(jobs_to_scrape, type):
    if type == 'recommend':
        jobs_per_page = 10
    elif type == 'applied':
        jobs_per_page = 20
        
    pages = math.ceil(jobs_to_scrape / jobs_per_page)
    
    jobs = {
        'title': [],
        'company': [],
        'description': [], 
        'url': []
    }
    
    with sync_playwright() as playwright:
        # open browser and navigate to jobright
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        context = browser.new_context(storage_state="./auths/jobright_auth.json")
        page = context.new_page()

        page.goto(f"https://jobright.ai/jobs/{type}")
        
        # scroll until all jobs are visible
        scroll_locator = page.locator("div#scrollableDiv")
        scroll_locator.wait_for()
        ul_locator = page.locator("ul.ant-list-items")
        ul_locator.wait_for()
        
        for i in range(pages - 1):
            scroll_locator.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")
            time.sleep(2) # wait for jobs to load
        
        # get job list
        divs = ul_locator.locator("xpath=/div")
        job_ids = [divs.nth(i).get_attribute("id") for i in range(divs.count())]
        
        # scape each job
        for job_id in job_ids:
            if jobs_to_scrape == 0:
                break
            page.goto(f"https://jobright.ai/jobs/info/{job_id}")
            company = page.locator("h2.index_company-row__vOzgg").inner_text().split("\n")[0]
            title = page.locator("h1.index_job-title__sStdA").text_content()
            url = page.locator("a.index_origin__7NnDG").get_attribute("href")

            description = ""
            summary = page.locator("p.index_company-summary__8nWbU").inner_text()            
            description += "Summary: \n" + summary + "\n\n"
            
            # Responsibilities
            try:
                responsibility = page.locator("xpath=//div[preceding-sibling::div[h2[text()='Responsibilities']]]").inner_text()
                description += "Responsibilities: \n" + responsibility + "\n\n"
            except Error as e:
                print(f"Failed to scrape Responsibilities: {e}")
            
            # Qualification
            try: 
                description += "Qualification: \n"
                
                qualification_locator = page.locator("xpath=//section[@id='skills-section']//div[@class='index_flex-col__Y_QL8']")
                for i in range(qualification_locator.count()):
                    sub_title = qualification_locator.nth(i).locator("h4.index_qualifications-sub-title__IA6rq").inner_text()
                    list_divs = qualification_locator.nth(i).locator('xpath=/div')
                    required_qualification = "\n".join(["  -" + list_divs.nth(i).inner_text() for i in range(list_divs.count())])
                    description += sub_title + "\n"
                    description += required_qualification + "\n\n"
            except Error as e:
                print(f"Failed to scrape Qualification: {e}")
                
            jobs['title'].append(title)
            jobs['company'].append(company)
            jobs['description'].append(description)
            jobs['url'].append(url)
            print(title, company)
            jobs_to_scrape -= 1
        
        context.close()
        browser.close() 
        
        pd.DataFrame(jobs).to_csv("./jobs.csv", index=False, encoding="utf-8")   