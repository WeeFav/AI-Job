from dotenv import load_dotenv
import os
import getpass
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langsmith import traceable
from langchain_core.tracers import LangChainTracer
from langchain import hub
from bs4 import BeautifulSoup
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

load_dotenv()

tracer = LangChainTracer(project_name="aijob")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

class PlaywrightTools():
    def __init__(self, browser):
        self.sync_browser = browser
        self.page = self.sync_browser.new_page()

    @tool
    def navigate(self, url: str) -> str:
        """Navigate a browser to the specified URL"""
        response = self.page.goto(url)
        status = response.status if response else "unknown"
        return f"Navigating to {url} returned status code {status}"
    
    @tool
    def extract_text(self) -> str:
        """Extract all the text on the current webpage"""
        html_content = self.page.content()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "lxml")

        return " ".join(text for text in soup.stripped_strings)
    
    @tool
    def click(self, selector: str) -> str:
        """Click on an element with the given CSS selector"""
        try:
            self.page.click(
                selector,
                timeout=1000,
            )
        except PlaywrightTimeoutError:
            return f"Unable to click on element '{selector}'"
        except SyntaxError as e:
            return e
        return f"Clicked element '{selector}'"

# @tool
# def add(a: int, b: int) -> int:
#     """Adds two numbers"""
#     return a + b + 1

# @tool
# def mul(a: int, b: int) -> int:
#     """Multiply two numbers"""
#     return (a * b) + 1

tools = [add, mul]

langgraph_agent_executor = create_react_agent(model, tools)

query = "what is 2 multiply by 3, then add the result to 4?"
messages = langgraph_agent_executor.invoke({"messages": [("human", query)]}, config={"callbacks": [tracer]})
for m in messages['messages']:
    print("-----------------------------------------------------------")
    print(m)
    print("-----------------------------------------------------------")
    


