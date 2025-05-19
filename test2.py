from dotenv import load_dotenv
import os
import getpass
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.tracers import LangChainTracer
from pydantic import BaseModel, Field

load_dotenv()

tracer = LangChainTracer(project_name="aijob")

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

class AddInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

class MulInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")
    
class MyClass():
    def __init__(self):
        self.constant = 1
    
    @tool(args_schema=AddInput)
    def add(self, a: int, b: int) -> int:
        """Adds two numbers"""
        return a + b + self.constant

    @tool(args_schema=MulInput)
    def mul(self, a: int, b: int) -> int:
        """Multiply two numbers"""
        return (a * b) + self.constant

myclass = MyClass()
tools = [myclass.add, myclass.mul]

langgraph_agent_executor = create_react_agent(model, tools)

query = "what is 2 multiply by 3, then add the result to 4?"
messages = langgraph_agent_executor.invoke({"messages": [("human", query)]}, config={"callbacks": [tracer]})
for m in messages['messages']:
    print("-----------------------------------------------------------")
    print(m)
    print("-----------------------------------------------------------")
    

