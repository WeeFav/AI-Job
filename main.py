from tools.navigate import NavigateTool
from tools.extract_text import ExtractTextTool
from tools.click import ClickTool
from tools.fill import FillTool
from tools.extract_html import ExtractHTMLTool
from tools.select import SelectTool
from dotenv import load_dotenv
import os
import getpass
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tracers import LangChainTracer
import asyncio
from playwright.async_api import async_playwright

load_dotenv()

tracer = LangChainTracer(project_name="aijob")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

async def main():
    tool_cls = [
        NavigateTool,
        ExtractTextTool,
        ClickTool,
        FillTool,
        ExtractHTMLTool,
        SelectTool
    ]

    playwright = await async_playwright().start()
    async_browser = await playwright.chromium.launch(headless=False)
    tools = [t.from_browser(async_browser=async_browser) for t in tool_cls]

    print(tools)

    langgraph_agent_executor = create_react_agent(model, tools)

    url = "http://localhost:5173/"
    query = f"""
    Navigate to {url} and determine if a job application form is immediately visible or hidden behind an 'Apply' button or link.
    If necessary, click the appropriate button to reveal the form.

    Once the form is visible:
    1. Extract all visible form fields (inputs, textareas, select boxes, file uploads).
    2. For each field, infer what kind of data is expected based on its label, name, or placeholder.
    3. Automatically generate realistic, fake sample data to fill in the fields. Do not ask for input or clarification.

    Examples:
    - Name → John Doe  
    - Email → johndoe@example.com  
    - Phone → 555-123-4567  
    - LinkedIn → https://linkedin.com/in/johndoe  
    - Resume → resume.pdf  
    - Address → 123 Main St, New York, NY  
    - Website → https://johndoe.dev  
    - Cover Letter → "I am excited to apply for this position..."
    - Expected Salary → 85000

    Only respond with the actions needed to fill the form using the format 'text=...' for selectors.
    """


        
    async for step in langgraph_agent_executor.astream({"messages": [("human", query)]}, config={"callbacks": [tracer], "recursion_limit": 100}):
        print(step)
        print("------------------------------------------------------------------------")
        
    await async_browser.close()
    await playwright.stop()
    
if __name__ == "__main__":
    asyncio.run(main())

