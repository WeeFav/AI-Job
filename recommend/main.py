import argparse
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import NamedVector, SearchRequest, Filter, FieldCondition, Range
from datetime import datetime, timedelta
import os
import psycopg2
import psycopg2.extras
import spacy
from collections import defaultdict
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv
load_dotenv()

client = QdrantClient("http://localhost:6333") # connecting to local Qdrant instance
collection_name = "aijob"
model_name = "BAAI/bge-base-en-v1.5"
    
conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        database=os.environ["POSTGRES_DB"],
        port=os.environ["POSTGRES_PORT"]
    )
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

ner_model = "./ner_model_7_23"
stop_words = set(stopwords.words("english"))

with open("./abbreviations.json", "r", encoding="utf-8") as f:
    abbreviations = json.load(f)
    
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def normalize(text: str):
    # lowercase
    text = text.lower()
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # tokenize
    tokens = word_tokenize(text)
    nomralized_tokens = []
    for token in tokens:
        # expand abbreviation
        if token in abbreviations:
            token = abbreviations[token]
        # remove stop words
        if token in stop_words:
            continue
        nomralized_tokens.append(token)
    
    
    return " ".join(nomralized_tokens)    

def extract_skills(description_extracted):
    nlp = spacy.load(ner_model)
    doc = nlp(description_extracted)
    
    educations = set()
    majors = set()
    skills = defaultdict(int)
    
    for ent in doc.ents:
        if ent.label_ == "EDU":
            educations.add(ent.text)
        elif ent.label_ == "MJR":
            majors.add(ent.text)
        else:
            text = normalize(ent.text)
            skills[text] += 1
    
    return educations, majors, skills

def embedd_skills(skills: dict):
    # Separate skills and weights
    skills = list(skills.keys())
    weights = np.array([skills[skill] for skill in skills])

    # Embed each skill
    embeddings = embedding_model.encode(skills)  # shape: (N, 384)

    # Normalize weights
    weights = weights / weights.sum()

    # Compute weighted average
    weighted_embedding = np.average(embeddings, axis=0, weights=weights)
    return weighted_embedding
    
def keyword_scoring(job_hash):
    # If cache not available, extract skills and cache
    cursor.execute("""
        SELECT * FROM skills
        WHERE job_hash = %s
        """,
        (job_hash,) 
    )    
    result = cursor.fetchone()

    if result:
        skills = result["skills"]
        educations = result["educations"]
        majors = result["majors"]
        embedding = result["embedding"]
    else:
        cursor.execute("""
            SELECT * FROM jobs
            WHERE job_hash = %s
            """,
            (job_hash,) 
        )    
        result = cursor.fetchone()
        assert(result)            

        description_extracted = result["description_extracted"]
        educations, majors, skills = extract_skills(description_extracted)
        weighted_embedding = embedd_skills(skills)
        
        # save to postgres
        
    
    # Normalized match

    # Fuzzy match

    # Embedding similarity (pairwise similarity matrix using sentence_transformers.util.cos_sim)

def main(args):
    
    # upload resume
    with open(args.resume, 'r') as file:
        resume = file.read()
    
    # compute scores for top 100 jobs within the time range
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
        limit=100,
        with_payload=True
    )
    
    # Layered NER scoring
    
    # Use cached normalized_skills, and embedding if available
    

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
