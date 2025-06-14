from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
import getpass
import os
from dotenv import load_dotenv
from langchain import hub
import time
load_dotenv()

sync_browser = create_sync_playwright_browser(headless=False) # initiate browser
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser) # wrap browser in langchain toolkit
tools = toolkit.get_tools()

prompt = hub.pull("hwchase17/react")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

url = "https://careers.oceaneering.com/global/en/job/OCINGLOBAL29365"
cmd = f"""
Go to {url} and apply to the job using a generated user profile 
"""

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
command = {
    "input": cmd
}

agent_executor.invoke(command)