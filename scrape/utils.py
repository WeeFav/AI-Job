from qdrant_client import QdrantClient, models
from qdrant_client.models import Filter, FieldCondition, MatchValue
import psycopg2
import psycopg2.extras 
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

def create():
    client = QdrantClient("http://localhost:6333")
    collection_name = "aijob"
    model_name = "BAAI/bge-base-en-v1.5"

    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=client.get_embedding_size(model_name),
            distance=models.Distance.COSINE
        )
    )
    
def update_qdrant_playload():
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        database=os.environ["POSTGRES_DB"],
        port=os.environ["POSTGRES_PORT"]
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    qdrant_client = QdrantClient("http://localhost:6333")
    collection_name = "aijob"
    
    cursor.execute("""
        SELECT * FROM jobs
        """ 
    )    
    
    jobs = cursor.fetchall()
    
    for job in jobs:
        timestamp = job["timestamp"]
        # Convert ISO format to Unix float
        unix_time = timestamp.timestamp()
        
        hash = job["hash"]
       
        filter = Filter(
            must=[
                FieldCondition(
                    key="hash",
                    match=MatchValue(value=hash)
                )
            ]
        )

        hits = qdrant_client.scroll(
            collection_name=collection_name,
            scroll_filter=filter,
            limit=1
        )

        if len(hits[0]) == 0:
            print(f"Point with hash {hash} not found")
            continue
            
        point_ids = [point.id for point in hits[0]]      
            
        qdrant_client.set_payload(
            collection_name=collection_name,
            payload={"timestamp": unix_time},  # new field
            points=point_ids
        )
        print(f"Updated {hash}")

if __name__ == '__main__':
    update_qdrant_playload()        
        
