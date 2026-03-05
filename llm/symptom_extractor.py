
def extract_symptoms(user_input: str, known_symptoms):
    """
    Extracts known symptoms from free-text user input.
    Matches both underscore form (back_pain) and space form (back pain).

    user_input:     raw string from the user
    known_symptoms: list of symptom column names e.g. ["back_pain", "fever", ...]
    """

    user_input = user_input.lower().strip()

    normalised_input = user_input.replace("_", " ").replace(",", " ")

    found = []

    for symptom in known_symptoms:
        readable = symptom.lower().replace("_", " ")

        if readable in normalised_input:
            found.append(symptom)

    seen = set()
    unique_found = []
    for s in found:
        if s not in seen:
            seen.add(s)
            unique_found.append(s)

    return unique_found