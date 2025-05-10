from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser

sync_browser = create_sync_playwright_browser(headless=False) # initiate browser
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser) # wrap browser in langchain toolkit
tools = toolkit.get_tools()

tools_by_name = {tool.name: tool for tool in tools}
navigate_tool = tools_by_name["navigate_browser"]
get_elements_tool = tools_by_name["get_elements"]
current_webpage_tool = tools_by_name["current_webpage"]

url = "https://geaerospace.wd5.myworkdayjobs.com/GE_ExternalSite/job/Evendale/AI-Digital-Technology-Intern_R5009391"
# url = "https://web.archive.org/web/20230428133211/https://cnn.com/world"
navigate_tool.run(
    {"url": url}
)
page, page_url = current_webpage_tool.run(None)
page.wait_for_selector(".css-12ug2mi")

x = get_elements_tool.run(
    {"selector": ".css-12ug2mi"}
)
print(x)

