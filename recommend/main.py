import argparse
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import NamedVector, SearchRequest, Filter, FieldCondition, Range
from datetime import datetime, timedelta


def main(args):
    client = QdrantClient("http://localhost:6333") #connecting to local Qdrant instance
    collection_name = "aijob"
    model_name = "BAAI/bge-base-en-v1.5"
    
    # upload resume
    with open(args.resume, 'r') as file:
        resume = file.read()
    
    # compute scores for jobs within the time range
    thirty_days_ago = (datetime.now() - timedelta(days=30)).timestamp() # 30 days ago in Unix format
    print(f"Recommend jobs up to {datetime.fromtimestamp(thirty_days_ago).isoformat()}")
    
    embedding_model = TextEmbedding(model_name=model_name)
    embeddings_generator = embedding_model.embed(resume)
    embeddings_list = list(embeddings_generator)
    resume_embeddings = embeddings_list[0]
    
    results = client.search(
        collection_name=collection_name,
        query_vector=resume_embeddings,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=Range(gte=thirty_days_ago)
                )
            ]
        ),
        limit=1000,
        with_payload=True
    )


    print(f"Found {len(results)} jobs")
    for point in results:
        print(point.payload['hash'], point.score)
        
        
    # return scores from keyword match
    
    # recommend 100 jobs
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', type=str, required=True)
    args = parser.parse_args()
    main(args)
