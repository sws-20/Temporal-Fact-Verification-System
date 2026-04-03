import json

def calculate_score(file):
    data = json.load(open(file))

    correct = 0
    wrong = 0
    not_verified = 0        # ← was missing entirely
    rule_violations = 0

    for claim in data:
        if claim["wikidata_verification"] == "correct":
            correct += 1
        elif claim["wikidata_verification"] == "wrong":
            wrong += 1
        else:
            not_verified += 1   # ← catch "not_verified" status
        
        if claim["rule_errors"]:
            rule_violations += 1

    print("Rule Violations:", rule_violations)

    score = correct / (correct + wrong) if (correct + wrong) > 0 else 0

    print("\n=== RELIABILITY REPORT ===")
    print("Correct:", correct)
    print("Wrong:", wrong)
    print("Not Verified:", not_verified)
    print("Reliability Score:", round(score, 2))

def main():
    person = input("Person name: ")
    file = f"verification_{person.replace(' ', '_')}.json"
    calculate_score(file)

if __name__ == "__main__":
    main()