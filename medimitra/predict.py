import joblib
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model")

model = joblib.load(os.path.join(MODEL_PATH, "disease_model.pkl"))
label_encoder = joblib.load(os.path.join(MODEL_PATH, "label_encoder.pkl"))
symptom_columns = joblib.load(os.path.join(MODEL_PATH, "symptom_columns.pkl"))


def predict_disease(symptom_list):
    """
    symptom_list: list of symptom strings e.g. ["back_pain", "fever"]
    """

    row = {col: 1 if col in symptom_list else 0 for col in symptom_columns}
    X = pd.DataFrame([row])

    probabilities = model.predict_proba(X)[0]
    predicted_index = np.argmax(probabilities)
    confidence = float(np.max(probabilities))
    disease = label_encoder.inverse_transform([predicted_index])[0]

    print("Input symptoms:", symptom_list)
    print("Matched features (sum):", X.sum(axis=1).values[0])

    # Confidence threshold
    if confidence < 0.10:
        return {
            "disease": "Uncertain",
            "confidence": round(confidence * 100, 2)
        }

    return {
        "disease": disease,
        "confidence": round(confidence * 100, 2)
    }