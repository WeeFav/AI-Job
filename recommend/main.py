import argparse
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import NamedVector, SearchRequest, Filter, FieldCondition, Range
from datetime import datetime, timedelta
import os
import math
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

with open("./skills_abbreviations.json", "r", encoding="utf-8") as f:
    skills_abbreviations = json.load(f)
with open("./education_abbreviations.json", "r", encoding="utf-8") as f:
    education_abbreviations = json.load(f)
    
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def normalize(text: str, abbr):
    # lowercase
    text = text.lower()
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # tokenize
    tokens = word_tokenize(text)
    nomralized_tokens = []
    for token in tokens:
        # expand abbreviation
        if token in abbr:
            token = abbr[token]
        # remove stop words
        if token in stop_words:
            continue
        nomralized_tokens.append(token)
    
    
    return " ".join(nomralized_tokens)    

def extract_keyword(description_extracted):
    nlp = spacy.load(ner_model)
    doc = nlp(description_extracted)
    
    educations = set()
    majors = set()
    skills = defaultdict(int)
    
    for ent in doc.ents:
        if ent.label_ == "EDU":
            text = normalize(ent.text, education_abbreviations)
            educations.add(text)
        elif ent.label_ == "MJR":
            text = normalize(ent.text, education_abbreviations)
            majors.add(text)
        else:
            text = normalize(ent.text, skills_abbreviations)
            skills[text] += 1
    
    return educations, majors, skills

def embed_skills(skills: dict) -> dict:
    skills_list = list(skills.keys())
    
    cursor.execute(
        """
        SELECT skill, embedding
        FROM embeddings
        WHERE skill = ANY(%s)
        """,
        (skills_list,)
    )
    rows = cursor.fetchall()
    
    embeddings = {}
    
    # cached skill embeddings
    for skill, embedding in rows:
        embeddings[skill] = np.array(embedding, dtype=float)
        
    # compute missing skill embeddings
    missing_skills = [skill for skill in skills_list if skill not in embeddings]
    
    if missing_skills:
        new_embs = embedding_model.encode(missing_skills, normalize_embeddings=True)
        
        # Add to dict
        for skill, emb in zip(missing_skills, new_embs):
            embeddings[skill] = emb
                
        # Insert new embeddings into Postgres
        insert_values = [(skill, emb.tolist()) for skill, emb in zip(missing_skills, new_embs)]
        cursor.executemany(
            """
            INSERT INTO keyword_embeddings (keyword, embedding) 
            VALUES (%s, %s) 
            ON CONFLICT (keyword) DO NOTHING
                 
            """,
            insert_values       
        )
        conn.commit()
    
    return embeddings
    

def cosine_similarity_freq(resume, jd):
    """
    Frequency-based cosine similarity between two keyword dictionaries.
    Return between 0 and 1
    """
    all_keys = set(resume) | set(jd)
    dot = sum(resume.get(k, 0) * jd.get(k, 0) for k in all_keys) # dot product of the two vectors (where the vectors are keyword frequency counts)
    norm_r = math.sqrt(sum(v**2 for v in resume.values()))
    norm_j = math.sqrt(sum(v**2 for v in jd.values()))
    return dot / (norm_r * norm_j) if norm_r and norm_j else 0
    
    
def adjusted_jaccard(resume, jd):
    """
    Coverage-based weighted Jaccard similarity (resume coverage of JD keywords).
    Denominator is sum of JD frequencies (target).
    Intersection over union (IOU)
    """
    numerator = sum(min(resume.get(k, 0), jd.get(k, 0)) for k in jd)
    denominator = sum(jd.values())
    return numerator / denominator if denominator else 0


def compute_skill_embeddings_similarity(r_embeddings: dict, j_embeddings: dict):
    similarity_matrix = {}
    for jk, j_emb in job_embs.items():
        similarity_matrix[jk] = {}
        for rk, r_emb in resume_embs.items():
            similarity_matrix[jk][rk] = cosine_sim(j_emb, r_emb)   


    total_weight = sum(job_freq.values())  # Normalization factor
    score_sum = 0

    for jk in job_freq:
        # Best matching resume keyword
        best_match_score = 0
        for rk in resume_freq:
            sim = similarity_matrix[jk][rk]
            weighted_sim = sim * min(resume_freq[rk], job_freq[jk])
            best_match_score = max(best_match_score, weighted_sim)
        
        # Weight by job keyword importance
        score_sum += best_match_score * job_freq[jk]

    final_score = score_sum / total_weight
    print("Weighted embedding similarity score:", final_score)             
    
def keyword_scoring(job_hash, r_educations, r_majors, r_skills, r_embeddings):
    cursor.execute("""
        SELECT * FROM skills
        WHERE job_hash = %s
        """,
        (job_hash,) 
    )    
    result = cursor.fetchone()

    if result:
        j_skills = result["skills"]
        j_educations = result["educations"]
        j_majors = result["majors"]
    else: # If keyword cache not available, extract and cache
        cursor.execute("""
            SELECT * FROM jobs
            WHERE job_hash = %s
            """,
            (job_hash,) 
        )    
        result = cursor.fetchone()
        assert(result)            

        description_extracted = result["description_extracted"]
        j_educations, j_majors, j_skills = extract_keyword(description_extracted)
        j_embeddings = embed_skills(j_skills)
        
        # save to postgres
        cursor.execute("""
            INSERT INTO skills (job_hash, skills, educations, majors)
            VALUES (%s, %s, %s, %s)
            """,
            (job_hash, json.dumps(j_skills), list(j_educations), list(j_majors))
        )
        conn.commit()    
        
    # Normalized match
    cosine_score = cosine_similarity_freq(r_skills, j_skills)
    jaccard_score = adjusted_jaccard(r_skills, j_skills)
    final_score = (w_cosine * cosine_score) + (w_jaccard * jaccard_score)    

    # Embedding similarity (pairwise similarity matrix using sentence_transformers.util.cos_sim)
    compute_skill_embeddings_similarity(r_embeddings, j_embeddings)
    
    return freq_score, fuzz_score, embed_score

def main(args):
    # --- 1. Resume ---
    
    # upload resume
    with open(args.resume, 'r') as file:
        resume = file.read()
        
    # extract keyword
    r_educations, r_majors, r_skills = extract_keyword(resume)
    r_embeddings = embed_skills(r_skills)
    
    # --- 2. Query top jobs ---
    
    # compute scores for top 100 jobs within the time range
    thirty_days_ago = (datetime.now() - timedelta(days=30)).timestamp() # 30 days ago in Unix format
    print(f"Recommend jobs up to {datetime.fromtimestamp(thirty_days_ago).isoformat()}")
    
    # embed resume
    embedding_model = TextEmbedding(model_name=model_name)
    embeddings_generator = embedding_model.embed(resume)
    embeddings_list = list(embeddings_generator)
    resume_embeddings = embeddings_list[0]
    
    # query vector db
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
    
    # --- 3. Score top jobs ---
    
    print(f"Scoring top {len(results)} jobs within the time range...")
    scores = {}
    
    for point in results:
        # Layered NER scoring
        job_hash = point.payload['hash']
        freq_score, fuzz_score, embed_score = keyword_scoring(job_hash, r_educations, r_majors, r_skills, r_embeddings)
        scores[job_hash] = [point.score, freq_score, fuzz_score, embed_score] # [description embedding score, keyword frequency score, fuzzy match score, keyword embedding score]
    
    
    
    
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', type=str, required=True)
    args = parser.parse_args()
    main(args)
    
    
    
    

