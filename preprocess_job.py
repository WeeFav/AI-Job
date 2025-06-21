import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

df = pd.read_csv("./jobs.csv")

prompt = "Here's a job description. Please extract only the subtitles and paragraphs that describe what the role is about, responsibilities, required skills, or who they are looking for. Do not include paragraphs that only describe the company, values, benefits. Do not summarize, only remove irrelevant text."

for i in range(len(df)):
    print(f"processing job {i + 1}")
    description = df.iloc[i]['description']

    messages = [
        ("system", prompt),
        ("human", description)
    ]
    
    ai_msg = llm.invoke(messages)
    
    df.loc[i, "description_extracted"] = ai_msg.content
    
df.to_csv("./jobs_extracted.csv", index=False, encoding="utf-8")   

