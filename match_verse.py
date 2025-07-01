import json
from rapidfuzz import fuzz

with open("quran_verses_named.json", encoding="utf-8") as f:
    quran_data = json.load(f)

def find_best_match(text):
    best_score = 0
    best_match = None
    for verse in quran_data:
        score = fuzz.partial_ratio(text, verse["text"])
        if score > best_score:
            best_score = score
            best_match = verse
            best_match["score"] = best_score
    return best_match
