from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import pandas as pd
import uuid

client = QdrantClient("http://localhost:6333") #connecting to local Qdrant instance

collection_name = "aijob"
model_name = "BAAI/bge-base-en-v1.5"
df = pd.read_csv("./jobs_extracted.csv")
     
# client.create_collection(
#     collection_name=collection_name,
#     vectors_config=models.VectorParams(
#         size=client.get_embedding_size(model_name),
#         distance=models.Distance.COSINE
#     )
# )    

points = []

for i in range(len(df)):
    hash = df.iloc[i]["hash"]
    title = df.iloc[i]["title"]
    company = df.iloc[i]["company"]
    url = df.iloc[i]["url"]
    description = df.iloc[i]["description"]
    description_extracted = df.iloc[i]["description_extracted"]

    exists = client.scroll(
        collection_name=collection_name,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(key="hash", match=models.MatchValue(value=hash))
            ]
        ),
        with_payload=False,
        with_vectors=False,
    )
    
    
    if len(exists[0]) > 0:
        print("Duplicate job found; skipping insert.")
        continue
    else:
        point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=models.Document(text=description_extracted, model=model_name),
            payload={
                "hash": hash,
                "title": title,
                "company": company,
                "url": url,
                "description": description,
                "description_extracted": description_extracted,
            }
        )
    
    points.append(point)

client.upsert(
    collection_name=collection_name,
    points=points
)