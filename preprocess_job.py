import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import time
from google.api_core.exceptions import ResourceExhausted
from utils import canonicalize_url
import hashlib
import psycopg2
import os

load_dotenv()

def preprocess(job_csv_path):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
    )
    
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        database=os.environ["POSTGRES_DB"],
        port=os.environ["POSTGRES_PORT"]
    )
    cursor = conn.cursor()

    df = pd.read_csv(job_csv_path)

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
                
        # canonicalize url
        url_norm = canonicalize_url(df.iloc[i]['url'])
        
        # generate hash
        title_norm = df.iloc[i]['title'].strip().lower()
        company_norm = df.iloc[i]['company'].strip().lower()
        combined = title_norm + company_norm + url_norm
        hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        cursor.execute("""
            INSERT INTO jobs (hash, title, company, url, description, description_extracted) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (hash) DO NOTHING
            """, 
            (hash, df.iloc[i]['title'], df.iloc[i]['company'], url_norm, description, ai_msg.content)
        )
        conn.commit()
        
        if cursor.rowcount == 0:
            print(f"[!] Duplicate hash detected: {hash}, nothing inserted.")
        
        print(f"processed job {i + 1}")
        
        
