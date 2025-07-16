import json
from spacy.tokens import DocBin
from tqdm import tqdm
import spacy

def labelstudio_to_spacy(raw_annotation_path):
    with open(raw_annotation_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
        
    train_data = []
    for task in raw:
        if task["annotations"][0]["was_cancelled"] or len(task["annotations"][0]["result"]) == 0:
            continue
        
        labels = []
        text = task["data"]["description_extracted"]
        annotations = task["annotations"][0]["result"]
        for annotation in annotations:
            start = annotation["value"]["start"]
            end = annotation["value"]["end"]
            entity = annotation["value"]["labels"][0] # only 1 label per string
            labels.append((start, end, entity))
        train_data.append((text, {"entities": labels}))
        
    return train_data

def spacy_to_binary(train_data, binary_path):
    nlp = spacy.blank("pt")
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