from qdrant_client import QdrantClient, models
import pandas as pd
import uuid

client = QdrantClient("http://localhost:6333") #connecting to local Qdrant instance

collection_name = "aijob"
model_name = "BAAI/bge-base-en-v1.5"

def create():
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=client.get_embedding_size(model_name),
            distance=models.Distance.COSINE
        )
    )    

def insert():
    df = pd.read_csv("./qdrant_jobs.csv")
    points = []

    for i in range(len(df)):
        hash = df.iloc[i]["hash"]
        description_extracted = df.iloc[i]["description_extracted"]
        
        point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=models.Document(text=description_extracted, model=model_name),
            payload={
                "hash": hash,
            }
        )
        
        points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=points
    )

if __name__ == '__main__':
    # create()
    insert()