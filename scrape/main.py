import argparse
import pandas as pd

from linkedin import scrape_linkedin
from jobright import scrape_jobright
from insert import insert
from label_studio_annotate import 

def main(args):
    if args.job_site == 'LinkedIn':
        jobs = scrape_linkedin(args.num_jobs)
    elif args.job_site == 'Jobright':
        jobs = scrape_jobright(args.num_jobs, args.type)
    
    pd.DataFrame(jobs).to_csv("./jobs.csv", index=False, encoding="utf-8")
    
    description_extracted_list = insert("./jobs.csv")
    
    if args.annotate:
        
       
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--job_site', type=str, required=False, default='LinkedIn', choices=['LinkedIn', 'Jobright'])
    parser.add_argument('--num_jobs', type=int, required=False, default=10)
    parser.add_argument('--type', type=str, required=False, default='recommend', choices=['recommend', 'applied'])
    parser.add_argument('--annotate', action='store_true')
    args = parser.parse_args()
    main(args)