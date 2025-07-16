import os
import psycopg2
import pandas as pd
import hashlib
from qdrant_client import QdrantClient, models
import uuid

from preprocess_job import extract_description, canonicalize_url

def insert(job_csv_path):
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        database=os.environ["POSTGRES_DB"],
        port=os.environ["POSTGRES_PORT"]
    )
    cursor = conn.cursor()
    
    client = QdrantClient("http://localhost:6333")
    collection_name = "aijob"
    model_name = "BAAI/bge-base-en-v1.5"

    df = pd.read_csv(job_csv_path)
    description_extracted_list = [] # for label studio annotation

    for i in range(len(df)):
        # extract description
        description = df.iloc[i]['description']
        description_extracted = extract_description(description)
        description_extracted_list.append(description_extracted)
               
        # canonicalize url
        url_norm = canonicalize_url(df.iloc[i]['url'])
        
        # generate hash
        title_norm = df.iloc[i]['title'].strip().lower()
        company_norm = df.iloc[i]['company'].strip().lower()
        combined = title_norm + company_norm + url_norm
        hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        # insert into postgres
        cursor.execute("""
            INSERT INTO jobs (hash, title, company, url, description, description_extracted) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (hash) DO NOTHING
            """, 
            (hash, df.iloc[i]['title'], df.iloc[i]['company'], url_norm, description, description_extracted)
        )
        conn.commit()
        
        # check if job exist
        exist = False
        if cursor.rowcount == 0:
            print(f"[!] Duplicate hash detected: {hash}, nothing inserted.")
            exist = True
        
        # insert into qdrant
        if not exist:
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=models.Document(text=description_extracted, model=model_name),
                payload={
                    "hash": hash,
                }
            )
            
            client.upsert(
                collection_name=collection_name,
                points=[point]
            )
            
        print(f"processed job {i + 1}")
    
    return description_extracted_list
            