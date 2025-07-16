import spacy

from convert_format import labelstudio_to_spacy, spacy_to_binary

train_data = labelstudio_to_spacy("./recommend/annotation1.json")


