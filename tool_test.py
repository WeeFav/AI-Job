from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
import time

sync_browser = create_sync_playwright_browser(headless=False) # initiate browser
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser) # wrap browser in langchain toolkit
tools = toolkit.get_tools()

tools_by_name = {tool.name: tool for tool in tools}

url = "https://www.amazon.jobs/en/jobs/2808698/robotics-systems-dev-engineer-co-op-spring-fall-2025?cmpid=SPLICX0248M&ss=paid&utm_campaign=cxro&utm_content=job_posting&utm_medium=social_media&utm_source=jobright"

tools_by_name['navigate_browser'].run(
    {"url": url}
)

# tools_by_name['wait_page'].run({})


# x = tools_by_name['extract_html'].run({})
# print(x)

# page, _ = tools_by_name['current_webpage'].run({})

# result = page.click(selector=".apply-now-button")

# time.sleep(5)

result = tools_by_name['click_element'].run({
    "selector": "text=Apply now"
})

print(result)

