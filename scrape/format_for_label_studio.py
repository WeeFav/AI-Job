import pandas as pd

df = pd.read_csv("./qdrant_jobs.csv")

all_text_list = []

for index, row in df.iterrows():
    description_extracted = row['description_extracted']
    text_list = description_extracted.split("\n")
    text_list = list(filter(lambda x: x != "", text_list))
    all_text_list.extend(text_list)

all_text_str = "\n".join(all_text_list)
with open("./label_studio_text", "w", encoding="utf-8") as f:
    f.write(all_text_str)
    