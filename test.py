from playwright.sync_api import sync_playwright, Error
import time
import math
import pandas as pd

def scrape():
    with sync_playwright() as playwright:
        # open browser and navigate to jobright
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False,
        )
        context = browser.new_context(storage_state="auth/jobright_auth.json")
        page = context.new_page()

        page.goto("https://jobright.ai/jobs/info/6858ae13d02a4449794ed1bc")
        
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
        
            
        print(title, company)
        
        context.close()
        browser.close() 
        
if __name__ == '__main__':
    scrape()