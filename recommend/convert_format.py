import json
from spacy.tokens import DocBin
from tqdm import tqdm
import spacy
import random

def labelstudio_to_spacy(raw_annotation_path):
    with open(raw_annotation_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
        
    annotated_data = []
    empty_data = []
    for task in raw:
        if len(task["annotations"][0]["result"]) > 0:
            labels = []
            text = task["data"]["description_extracted"]
            annotations = task["annotations"][0]["result"]
            window = -1
            for annotation in annotations:
                start = annotation["value"]["start"]
                end = annotation["value"]["end"]
                entity = annotation["value"]["labels"][0] # only 1 label per string

                if start <= window:
                    print("Found overlap, skipping...")
                    continue
                window = start
                
                labels.append((start, end, entity))
            annotated_data.append((text, {"entities": labels}))
        elif task["annotations"][0]["was_cancelled"]:
            text = task["data"]["description_extracted"]
            empty_data.append((text, {"entities": []}))
    
    selected_empty = random.sample(empty_data, 300)
    annotated_data.extend(selected_empty)
        
    return annotated_data

def spacy_to_binary(train_data, binary_path):
    nlp = spacy.blank("en")
    db = DocBin()
    
    for text, annot in tqdm(train_data): 
        doc = nlp.make_doc(text) 
        seen_tokens = set()
        has_overlap = False
        ents = []
        
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
                continue
            
            # check for overlap at token level
            span_tokens = set(range(span.start, span.end))
            if seen_tokens & span_tokens:
                print(f"Overlapping span: ({start}, {end}, '{label}') in '{text}'")
                continue  
            seen_tokens |= span_tokens
            ents.append(span)
        
        doc.ents = ents 
        db.add(doc)
            
    db.to_disk(binary_path)