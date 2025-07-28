import pandas as pd
import os
import string
from label_studio_sdk.client import LabelStudio
from label_studio_sdk import Client
import spacy
import json
from dotenv import load_dotenv
load_dotenv()

LABEL_STUDIO_URL = 'http://localhost:8080'


def annotate(description_extracted_list):
    all_text_list = []

    for description_extracted in description_extracted_list:
        text_list = description_extracted.split("\n")
        text_list = list(filter(lambda x: x != "", text_list))
        text_list = list(map(lambda x: x.strip(string.whitespace + string.punctuation), text_list))
        all_text_list.extend(text_list)
    
    print(len(all_text_list))
    
    # Connect to the Label Studio
    ls = LabelStudio(base_url=LABEL_STUDIO_URL, api_key=os.environ['LABEL_STUDIO_API_KEY'])
    
    # Load the custom model
    ner_model = "ner_model_50"
    nlp = spacy.load(f"../recommend/{ner_model}")

    preannotations = []

    # Process texts in batch using nlp.pipe()
    for doc in nlp.pipe(all_text_list, batch_size=16):  # Adjust batch_size as needed
        preannotation = {"description_extracted": doc.text}
        
        results = []
        for ent in doc.ents:
            result = {
                "id": ent.label_ + "_" + str(ent.start_char),  # unique ID
                "from_name": "label",
                "to_name":"text",
                "type": "labels",
                "value": {
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "score": getattr(ent, "score", None) or 1.0,  # default to 1.0 if not available
                    "text": ent.text,
                    "labels": [ent.label_]
                }
            }
            results.append(result)
        
        preannotation["result"] = results
        preannotations.append(preannotation)
        
    ls.projects.import_tasks(id=1, request=preannotations, preannotated_from_fields=["result"])
    
def predict_from_task(start, end=None):
    ls = LabelStudio(base_url=LABEL_STUDIO_URL, api_key=os.environ['LABEL_STUDIO_API_KEY'])

    filters = {
        "conjunction": "and",
        "items": [
            {
                "filter": "filter:tasks:id",
                "operator": "greater_or_equal",
                "type": "Number",
                "value": start
            },
            {
                "filter": "filter:tasks:id",
                "operator": "less_or_equal",
                "type": "Number",
                "value": end
            }
        ]
    }
    query = {
        "filters": filters
    }
    
    tasks = list(ls.tasks.list(project=1, query=json.dumps(query)))
    print("Number of tasks filtered:", len(tasks))
        
    all_text_list = []
    for task in tasks:
        all_text_list.append(task.data['description_extracted'])
    
    # Load the custom model
    ner_model = "ner_model_7_24"
    nlp = spacy.load(f"../recommend/{ner_model}")
    
    for i, doc in enumerate(nlp.pipe(all_text_list, batch_size=16)):
        results = []
        for ent in doc.ents:
            result = {
                "id": ent.label_ + "_" + str(ent.start_char),  # unique ID
                "from_name": "label",
                "to_name":"text",
                "type": "labels",
                "value": {
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "score": getattr(ent, "score", None) or 1.0,  # default to 1.0 if not available
                    "text": ent.text,
                    "labels": [ent.label_]
                }
            }
            results.append(result)
    
        ls.predictions.create(task=tasks[i].id, result=results)
    

if __name__ == '__main__':
    # df = pd.read_csv("./jobs.csv")
    # description_list = df["description"].to_list()
    # annotate(description_list)
    predict_from_task(start=759, end=918)
