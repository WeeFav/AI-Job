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
from sentence_transformers.util import cos_sim
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

ner_model = "ner_models/7_28"
stop_words = set(stopwords.words("english"))

with open("skills_abbreviations.json", "r", encoding="utf-8") as f:
    skills_abbreviations = json.load(f)
with open("education_abbreviations.json", "r", encoding="utf-8") as f:
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
    
    return educations, majors, skills, doc

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


def compute_skill_embeddings_similarity(r_embeddings: dict, j_embeddings: dict, r_skills: dict, j_skills: dict):
    j_skills_list = list(j_embeddings.keys())
    r_skills_list = list(r_embeddings.keys())
    
    similarity_matrix = cos_sim([j_embeddings[skill] for skill in j_skills_list], [r_embeddings[skill] for skill in r_skills_list])
    
    total_weight = sum(j_skills.values())  # Normalization factor
    score_sum = 0

    for j, j_skill in enumerate(j_skills_list):
        # Best matching resume keyword
        best_match_score = 0
        for r, r_skill in enumerate(r_skills_list):
            sim = similarity_matrix[j][r]
            weighted_sim = sim * min(j_skills[j_skill], r_skills[r_skill]) # weighted by overlap frequency
            best_match_score = max(best_match_score, weighted_sim) # keep best match score
            
        # Weight by job keyword importance
        score_sum += best_match_score * j_skills[j_skill]

    final_score = score_sum / total_weight
    return final_score             
    
    
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
    freq_score = (0.5 * cosine_score) + (0.5 * jaccard_score)    

    # Embedding similarity (pairwise similarity matrix using sentence_transformers.util.cos_sim)
    embed_score = compute_skill_embeddings_similarity(r_embeddings, j_embeddings, r_skills, j_skills)
    
    # education match
    if len(j_educations) > 0 and len(j_educations.intersection(r_educations)) == 0:
        edu_score = 0
    else:
        edu_score = 1
        
    # major match
    if len(j_majors) > 0 and len(j_majors.intersection(r_majors)) == 0:
        major_score = 0
    else:
        major_score = 1
    
    return freq_score, embed_score, edu_score, major_score

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
        freq_score, embed_score, edu_score, major_score = keyword_scoring(job_hash, r_educations, r_majors, r_skills, r_embeddings)
        # final score from [description embedding score, keyword frequency score, keyword embedding score, education match score, major match score]
        score = (0.4 * point.score) + (0.2 * freq_score) + (0.3 * embed_score) + (0.05 * edu_score) + (0.05 * major_score) 
        scores[job_hash] = score
    
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)    
    
    print(ranked)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', type=str, required=True)
    args = parser.parse_args()
    main(args)
    
    
    
    

