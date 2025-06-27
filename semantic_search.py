from qdrant_client import QdrantClient, models

client = QdrantClient("http://localhost:6333") #connecting to local Qdrant instance

collection_name = "aijob"
model_name = "BAAI/bge-base-en-v1.5"

results = client.query_points(
    collection_name=collection_name,
    query=models.Document(text=query, model=model_name),
    limit=limit,
    with_payload=True
)
    