import re


def normalize_symptom(text: str) -> str:
    """Converts any symptom string to lowercase_underscore form."""
    return text.lower().strip().replace(" ", "_")


def clean_text(text: str) -> str:
    """Strips non-alpha characters except commas and spaces."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z, ]', '', text)
    return text


def clean_user_input(user_input: str, valid_symptoms: list) -> list:
    """
    Splits a comma-separated symptom string and returns only
    symptoms that exist in the known symptom list.

    Example:
        clean_user_input("Back Pain, Fever, xyz", symptom_columns)
        → ["back_pain", "fever"]
    """
    raw = user_input.split(",")
    normalised = [normalize_symptom(s) for s in raw]
    return [s for s in normalised if s in valid_symptoms]