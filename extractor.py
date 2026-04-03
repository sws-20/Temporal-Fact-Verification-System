import re
import json
import spacy
from pathlib import Path
from dateutil import parser as dateutil_parser

nlp = spacy.load("en_core_web_sm")

DATE_PATTERNS = [
    (r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|August"
     r"|September|October|November|December)\s+(\d{4})\b", "day"),
    (r"\b(January|February|March|April|May|June|July|August|September"
     r"|October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b", "day"),
    (r"\b(\d{4})-(\d{2})-(\d{2})\b", "day"),
    (r"\b(January|February|March|April|May|June|July|August|September"
     r"|October|November|December)\s+(\d{4})\b", "month"),
    (r"\b(1[0-9]{3}|20[0-9]{2})\b", "year"),
]

EVENT_TRIGGERS = {
    "birth": ["born"],
    "death": ["died", "passed away"],
    "award": ["won", "awarded", "prize", "award", "nominated"],
    "education": ["studied", "graduated", "university", "college"],
    "role": ["elected", "appointed", "served", "president", "ceo", "director"],
    "work": ["worked", "joined", "hired", "starred", "founded"],
    "marriage": ["married"]
}

def normalize_date(date_string, precision):
    try:
        dt = dateutil_parser.parse(date_string)
        if precision == "year":
            return f"{dt.year}-01-01"
        elif precision == "month":
            return f"{dt.year}-{dt.month:02d}-01"
        else:
            return f"{dt.year}-{dt.month:02d}-{dt.day:02d}"
    except:
        return None

def extract_dates(text):
    dates = []
    for pattern, precision in DATE_PATTERNS:
        for m in re.finditer(pattern, text):
            raw = m.group(0)
            iso = normalize_date(raw, precision)
            if iso:
                dates.append((raw, iso, precision))
    return dates

def classify_event(sentence):
    s = sentence.lower()
    for etype, words in EVENT_TRIGGERS.items():
        if any(w in s for w in words):
            return etype
    return "other"

def extract_claims(text, person_name):
    doc = nlp(text)
    claims = []

    for sent in doc.sents:
        sentence = sent.text.strip()
        dates = extract_dates(sentence)
        event_type = classify_event(sentence)

        for raw, iso, precision in dates:
            claims.append({
                "person": person_name,
                "event_type": event_type,
                "date": iso,
                "precision": precision,
                "sentence": sentence
            })

    return claims

def main():
    person = input("Person name: ")
    file = f"articles/{person.replace(' ', '_')}.txt"

    text = Path(file).read_text(encoding="utf-8")
    claims = extract_claims(text, person)

    out = f"claims_{person.replace(' ', '_')}.json"
    with open(out, "w") as f:
        json.dump(claims, f, indent=2)

    print("Claims extracted:", len(claims))

if __name__ == "__main__":
    main()