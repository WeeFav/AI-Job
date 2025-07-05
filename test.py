from playwright.sync_api import sync_playwright, Playwright, Error
import time
import pandas as pd
import math


with sync_playwright() as playwright:
    # open browser and navigate to jobright
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False,
    )
    context = browser.new_context(storage_state="auth/linkedin_auth.json")
    page = context.new_page()

    page.goto(f"https://www.linkedin.com/jobs/search/?currentJobId=4261256984")

    title = page.locator("div.job-details-jobs-unified-top-card__job-title").inner_text()
    company = page.locator("div.job-details-jobs-unified-top-card__company-name").inner_text()
    description = page.locator("xpath=//div[@id='job-details']/div[@class='mt4']").inner_text()
                    
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
    
    print(title, company)
    print(description == "")

context.close()
browser.close() 
    
