from qdrant_client import QdrantClient, models

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