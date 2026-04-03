from datetime import datetime

def get_year(date_str):
    if not date_str:
        return None
    return int(date_str[:4])

def apply_rules(claim, person_data):
    event_year = get_year(claim["date"])
    birth_year = get_year(person_data.get("birth"))
    death_year = get_year(person_data.get("death"))

    errors = []

    # Rule 1: Before birth
    if birth_year and event_year < birth_year:
        errors.append("Event happened before birth")

    # Rule 2: After death
    if death_year and event_year > death_year:
        errors.append("Event happened after death")

    # Rule 3: Marriage minimum age
    if claim["event_type"] == "marriage":
        if birth_year and (event_year - birth_year) < 15:
            errors.append("Marriage before age 15")

    # Rule 4: Job minimum age
    if claim["event_type"] in ["work", "role"]:
        if birth_year and (event_year - birth_year) < 18:
            errors.append("Job before age 18")

    # Rule 5: Nobel Prize existence
    if claim["event_type"] == "award":
        if event_year < 1901:
            errors.append("Nobel Prize did not exist before 1901")

    return errors