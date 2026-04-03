import requests
import json
from rules import apply_rules

HEADERS = {
    "User-Agent": "TemporalFactChecker/1.0 (student project)"
}

WIKIDATA_API = "https://www.wikidata.org/w/api.php"
ENTITY_API = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"

PROPERTY_MAP = {
    "birth": "P569",
    "death": "P570",
    "award": "P166",
    "education": "P69",
    "role": "P39",
    "work": "P108",
    "marriage": "P26"
}

def get_wikidata_id(name):
    params = {
        "action": "wbsearchentities",
        "search": name,
        "language": "en",
        "format": "json"
    }

    try:
        r = requests.get(WIKIDATA_API, params=params, headers=HEADERS, timeout=10)

        print("Status Code:", r.status_code)
        print("Raw Response:", r.text[:200])  # DEBUG

        data = r.json()

        if not data.get("search"):
            print("No results found for:", name)
            return None

        return data["search"][0]["id"]

    except Exception as e:
        print("Error fetching Wikidata ID:", e)
        return None

def fetch_property(qid, prop):
    url = ENTITY_API.format(qid)
    print("Fetching:", url) 
    r = requests.get(url, headers=HEADERS, timeout=10)  
    print("Status:", r.status_code, "| Body length:", len(r.text))
    
    if not r.ok or not r.text.strip():                  
        return []
    
    data = r.json()
    claims = data["entities"][qid]["claims"]
    return claims.get(prop, [])

def extract_year(date_str):
    if not date_str:
        return None
    return date_str[:4]

def verify_claim(qid, claim):
    event = claim["event_type"]
    date = claim["date"]
    year = extract_year(date)

    prop = PROPERTY_MAP.get(event)
    if not prop:
        return "not_verified"

    wd_claims = fetch_property(qid, prop)

    for c in wd_claims:
        try:
            wd_time = c["mainsnak"]["datavalue"]["value"]["time"]
            wd_year = wd_time[1:5]
            if wd_year == year:
                return "correct"
        except:
            pass

    return "wrong"


def build_person_data(qid):
    data = {}

    birth_claims = fetch_property(qid, "P569")
    death_claims = fetch_property(qid, "P570")

    try:
        if birth_claims:
            data["birth"] = birth_claims[0]["mainsnak"]["datavalue"]["value"]["time"][1:11]
    except:
        data["birth"] = None

    try:
        if death_claims:
            data["death"] = death_claims[0]["mainsnak"]["datavalue"]["value"]["time"][1:11]
    except:
        data["death"] = None

    return data


def main():
    person = input("Person name: ")
    claims_file = f"claims_{person.replace(' ', '_')}.json"

    claims = json.load(open(claims_file))
    qid = get_wikidata_id(person)

    if not qid:
        print("Cannot continue without Wikidata ID")
        return

    results = []
    person_data = build_person_data(qid)
    for claim in claims:
        result = verify_claim(qid, claim)
        rule_errors = apply_rules(claim, person_data)

        claim["wikidata_verification"] = result
        claim["rule_errors"] = rule_errors

        results.append(claim)


    out = f"verification_{person.replace(' ', '_')}.json"
    json.dump(results, open(out, "w"), indent=2)

    print("Verification complete")

if __name__ == "__main__":
    main()