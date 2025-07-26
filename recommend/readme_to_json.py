# Used for converting skill abbreviations from https://github.com/wuyichen24/software-engineering-abbreviations-acronyms/blob/master/README.md to a json file

import json
import re
import string

def normalize(text):
    # lowercase
    text = text.lower()
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

with open("./README.md", "r", encoding="utf-8") as f:
    md_text = f.read()

result = {}
current_abbreviation = None

lines = md_text.splitlines()
for line in lines:
    # Match abbreviation line like "- **AADD**"
    abbr_match = re.match(r'^-\s+\*\*(.+?)\*\*$', line.strip())
    if abbr_match:
        current_abbreviation = abbr_match.group(1)
        current_abbreviation = normalize(current_abbreviation)
        continue

    # Match link line like "- [Term](link)"
    link_match = re.match(r'^-\s+\[(.+?)\]\((.+?)\)$', line.strip())
    if link_match and current_abbreviation:
        term = link_match.group(1)
        term = normalize(term)
        result[current_abbreviation] = term
        current_abbreviation = None  # reset for next entry
        continue
    
    # Match term line like "- Term"
    term_match = re.match(r'^-\s+(.+?)$', line.strip())
    if term_match and current_abbreviation:
        term = term_match.group(1)
        term = normalize(term)
        result[current_abbreviation] = term
        current_abbreviation = None  # reset for next entry
        continue
    
    
# Save to JSON file
with open("abbreviations.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

