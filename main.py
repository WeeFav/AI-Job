from tools.navigate import NavigateTool
from tools.extract_text import ExtractTextTool
from tools.click import ClickTool
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
        ClickTool
    ]

    playwright = await async_playwright().start()
    async_browser = await playwright.chromium.launch(headless=False)
    tools = [t.from_browser(async_browser=async_browser) for t in tool_cls]

    print(tools)

    langgraph_agent_executor = create_react_agent(model, tools)

    url = "http://localhost:5173/"
    query = f"Navigate to {url}, extract all text, and click apply. Use selector format: 'text=...' "
    
    async for step in langgraph_agent_executor.astream({"messages": [("human", query)]}, config={"callbacks": [tracer]}):
        print(step)
        print("------------------------------------------------------------------------")
    
    # messages = await langgraph_agent_executor.ainvoke({"messages": [("human", query)]}, config={"callbacks": [tracer]})
    # for m in messages['messages']:
    #     print("-----------------------------------------------------------")
    #     print(m)
    #     print("-----------------------------------------------------------")
    
    await async_browser.close()
    await playwright.stop()
    
if __name__ == "__main__":
    asyncio.run(main())

