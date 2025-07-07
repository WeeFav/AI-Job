from insert_vector_db import insert # this import needs to be the first or else it will cause some weird error
import scrape.jobright
import scrape.linkedin
from preprocess_job import preprocess

# scrape.linkedin.scrape(50)
# scrape.jobright.scrape(5)

# preprocess("./jobs.csv")
insert("./qdrant_jobs.csv")
