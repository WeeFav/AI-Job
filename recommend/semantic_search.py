from qdrant_client import QdrantClient, models

client = QdrantClient("http://localhost:6333") #connecting to local Qdrant instance

collection_name = "aijob"
model_name = "BAAI/bge-base-en-v1.5"
resume_path = "resume_de.txt"

with open(resume_path, 'r') as file:
    resume = file.read()

results = client.query_points(
    collection_name=collection_name,
    query=models.Document(text=resume, model=model_name),
    limit=5,
    with_payload=True
)

for point in results.points:
    print(point.payload['hash'], point.score)
    