# app.py

from fastapi import FastAPI
from pydantic import BaseModel
from medimitra.predict import predict_disease
from llm.symptom_extractor import extract_symptoms
from llm.explain_result import explain_disease
import joblib

app = FastAPI()

known_symptoms = joblib.load("model/symptom_columns.pkl")

class SymptomRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "MediMitra API is running"}

@app.post("/chat")
def chat(request: SymptomRequest):

    print("User message:", request.message)

    extracted = extract_symptoms(request.message, known_symptoms)

    print("Extracted symptoms:", extracted)

    if not extracted:
        return {
            "predicted_disease": "Unable to detect symptoms",
            "confidence": 0,
            "explanation": "I couldn't identify any recognisable symptoms in your message. Try describing them more specifically, e.g. 'I have back pain, fever, and headache'."
        }

    prediction = predict_disease(extracted)

    if prediction["disease"] == "Uncertain":
        return {
            "predicted_disease": "Uncertain",
            "confidence": prediction["confidence"],
            "explanation": "The symptoms described are not strong enough for a reliable prediction. Please consult a doctor."
        }

    explanation = explain_disease(prediction["disease"], request.message)

    return {
        "predicted_disease": prediction["disease"],
        "confidence":        prediction["confidence"],
        "explanation":       explanation
    }