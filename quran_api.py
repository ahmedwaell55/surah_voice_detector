import requests
import json

with open("ar.muyassar.json", encoding="utf-8") as f:
    tafsir_data = json.load(f)

# Search by surah number and ayah number
def get_tafsir(surah, ayah):
    for entry in tafsir_data:
        if entry["ayah"] == ayah:
            if str(entry["surah"]).startswith(str(surah) + " "):
                return {"data": {"tafsir": entry["text"]}}
            if str(entry["surah"]).startswith(str(surah) + "-"):
                return {"data": {"tafsir": entry["text"]}}
            if str(entry["surah"]).split("-")[0].strip() == str(surah):
                return {"data": {"tafsir": entry["text"]}}
    return {"data": {"tafsir": "❌ Tafsir not found."}}


with open("en.ahmedali.json", encoding="utf-8") as f:
    translation_data = json.load(f)

# Function to get translation
def get_translation(surah, ayah):
    for entry in translation_data:
        if entry["ayah"] == ayah:
            if str(entry["surah"]).startswith(str(surah) + " "):
                return {"data": {"translation": entry["text"]}}
            if str(entry["surah"]).startswith(str(surah) + "-"):
                return {"data": {"translation": entry["text"]}}
            if str(entry["surah"]).split("-")[0].strip() == str(surah):
                return {"data": {"translation": entry["text"]}}
    return {"data": {"translation": "❌ Translation not found."}}