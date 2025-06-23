import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import time
from google.api_core.exceptions import ResourceExhausted
from utils import canonicalize_url
import hashlib

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
)

df = pd.read_csv("./jobs.csv")

prompt = """
Here's a job description. Please extract only the subtitles and paragraphs that describe what the role is about, responsibilities, required skills, or who they are looking for. 
Do not include paragraphs that only describe the company, values, benefits. 
Do not summarize, only remove irrelevant text.
Do not add any markdown formatting, only keep plain text.
"""

for i in range(len(df)):
    # extract job description
    description = df.iloc[i]['description']

    messages = [
        ("system", prompt),
        ("human", description)
    ]
    
    while True:
        try:
            ai_msg = llm.invoke(messages)
            break
        except ResourceExhausted as e:
            print(f"Retrying in 60 seconds...")
            time.sleep(60)
    
    df.loc[i, "description_extracted"] = ai_msg.content
    
    # canonicalize url
    url_norm = canonicalize_url(df.iloc[i]['url'])
    df.loc[i, "url"] = url_norm
    
    # generate hash
    title_norm = df.iloc[i]['title'].strip().lower()
    company_norm = df.iloc[i]['company'].strip().lower()
    combined = title_norm + company_norm + url_norm
    hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
    df.loc[i, "hash"] = hash
    
    print(f"processed job {i + 1}")

column_order = ['hash', 'title', 'company', 'url', 'description', 'description_extracted']    
df = df[column_order]
df.to_csv("./jobs_extracted.csv", index=False, encoding="utf-8")   

