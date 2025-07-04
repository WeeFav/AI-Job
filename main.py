import scrape.jobright
import scrape.linkedin
from preprocess_job import preprocess

scrape.linkedin.scrape(25)
# preprocess("./jobs.csv")
# scrape.jobright.scrape(5)