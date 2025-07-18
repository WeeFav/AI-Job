import spacy
import random
from spacy.training.example import Example

from convert_format import labelstudio_to_spacy, spacy_to_binary


def train():
    train_data = labelstudio_to_spacy("./recommend/annotation1.json")
    epochs = 50

    # Load a pretrained model
    nlp = spacy.load("en_core_web_sm")

    # Remove the existing NER
    nlp.remove_pipe("ner")

    # Add a new clean NER
    ner = nlp.add_pipe("ner")
    ner.add_label("TECH")
    ner.add_label("GEN")
    ner.add_label("EDU")
    ner.add_label("MJR")

    # Disable other components to avoid changing them
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        
        for epoch in range(epochs):
            print(f"Start epoch {epoch}")
            random.shuffle(train_data)
            losses = {}
            for text, annotations in train_data:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)

                nlp.update(
                    [example],
                    drop=0.2,
                    sgd=optimizer,
                    losses=losses
                )
            print(losses["ner"])

    nlp.to_disk("./recommend/ner_model_50")
    

def test():
    text = "Familiarity with data engineering concepts and tools (e.g., ETL processes, data warehousing)"
    nlp = spacy.load("./recommend/ner_model_50")
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)
    
if __name__ == '__main__':
    # train()
    # test()