from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import pandas as pd

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
    hash = df[i]["hash"]
    title = df[i]["title"]
    company = df[i]["company"]
    url = df[i]["url"]
    description = df[i]["description"]
    description_extracted = df[i]["description_extracted"]

    exists = client.retrieve(
        collection_name=collection_name,
        ids=[hash]
    )
    
    if len(exists) > 0:
        print("Duplicate job found; skipping insert.")
        continue
    else:
        point = models.PointStruct(
            id=hash,
            vector=models.Document(text=description_extracted, model=model_name),
            payload={
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