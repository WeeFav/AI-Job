import pandas as pd
import os
import string
from label_studio_sdk.client import LabelStudio
import spacy
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
    project = ls.projects.get(id=1)
    ls.import_tasks()
    
    # Load the custom model
    ner_model = "ner_model_50"
    nlp = spacy.load(f"./recommend/{ner_model}")

    preannotations = []

    # Process texts in batch using nlp.pipe()
    for doc in nlp.pipe(all_text_list, batch_size=16):  # Adjust batch_size as needed
        preannotation = {"data": {}, "predictions": []}
        preannotation["data"]["text"] = doc.text
        prediction = {"model_version": ner_model}
        
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
        
        prediction["result"] = results
        preannotation["predictions"].append(prediction)
        preannotations.append(preannotation)

    ls.predictions.create(result=preannotations)

if __name__ == '__main__':
    df = pd.read_csv("./scrape/jobs.csv")
    description_list = df["description"].to_list()
    annotate(description_list)
