from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tracers import LangChainTracer
import asyncio

# tracer = LangChainTracer(project_name="aijob")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

async def main():
    agent = Agent(
        task="Apply to https://external-mythics.icims.com/jobs/4185/genai-ml-software-engineer-co-op/login",
        llm=llm,
        use_vision=False,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())