from dotenv import load_dotenv
import os
import getpass
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool
from langsmith import traceable
from langchain_core.tracers import LangChainTracer
from langchain import hub
from bs4 import BeautifulSoup
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright
import asyncio
from pydantic import BaseModel, Field

load_dotenv()

tracer = LangChainTracer(project_name="aijob")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

class NavigateToolInput(BaseModel):
    """Input for NavigateToolInput."""
    url: str = Field(..., description="url to navigate to")
    
class ExtractTextToolInput(BaseModel):
    """Explicit no-args input for ExtractTextTool."""

class ClickToolInput(BaseModel):
    """Input for ClickTool."""
    selector: str = Field(..., description="CSS selector for the element to click")
    
class PlaywrightTools():
    def __init__(self):
        pass
        
    async def async_init(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()  

    async def navigate(self, url: str) -> str:
        """Navigate a browser to the specified URL"""
        response = await self.page.goto(url)
        status = response.status if response else "unknown"
        return f"Navigating to {url} returned status code {status}"
    
    async def extract_text(self) -> str:
        """Extract all the text on the current webpage"""
        html_content = await self.page.content()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "lxml")

        return " ".join(text for text in soup.stripped_strings)
    
    async def click(self, selector: str) -> str:
        """Click on an element with the given CSS selector"""
        try:
            await self.page.click(
                selector,
                timeout=1000,
            )
        except PlaywrightTimeoutError:
            return f"Unable to click on element '{selector}'"
        except SyntaxError as e:
            return str(e)
        return f"Clicked element '{selector}'"

async def main():
    playwright_tools = PlaywrightTools()
    await playwright_tools.async_init()
    
    navigate_tool = StructuredTool(
        name="navigate_tool",
        func=playwright_tools.navigate,
        description="Navigate a browser to the specified URL",
        args_schema=NavigateToolInput
    )

    extract_text_tool = StructuredTool(
        name="extract_text_tool",
        func=playwright_tools.extract_text,
        description="Extract all the text on the current webpage",
        args_schema=ExtractTextToolInput
    )

    click_tool = StructuredTool(
        name="click_tool",
        func=playwright_tools.click,
        description="Click on an element with the given CSS selector",
        args_schema=ClickToolInput
    )

    tools = [navigate_tool, extract_text_tool, click_tool]

    langgraph_agent_executor = create_react_agent(model, tools)

    url = "http://localhost:5173/"
    query = f"Navigate to {url} and extract all text and print the text out."

    messages = await langgraph_agent_executor.ainvoke({"messages": [("human", query)]}, config={"callbacks": [tracer]})
    for m in messages['messages']:
        print("-----------------------------------------------------------")
        print(m)
        print("-----------------------------------------------------------")
    
    # Cleanup playwright
    await playwright_tools.browser.close()
    await playwright_tools.playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())