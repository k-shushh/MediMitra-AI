# MediMitra AI 🩺

**MediMitra AI** is an AI-powered medical assistant that analyzes user-described symptoms and predicts possible diseases using machine learning. It also provides an easy-to-understand explanation of the prediction using an LLM.

The goal of MediMitra is to help users better understand their symptoms and encourage informed healthcare decisions.

⚠️ **Disclaimer:** MediMitra AI is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.

---

# 🌐 Live Demo

You can try MediMitra here:

**Frontend:**
https://medimitra-ai-k-shushh.streamlit.app/

**Backend API Docs:**
https://medimitra-api.onrender.com/docs

---

# ✨ Features

* 🧠 Machine learning–based disease prediction
* 💬 Natural language symptom input
* 🤖 LLM-generated medical explanation
* 📊 Confidence score for predictions
* 🌐 Deployed full-stack system (frontend + backend)

---

# 🏗️ System Architecture

User Input (Streamlit UI)
↓
Symptom Extraction (NLP)
↓
ML Disease Prediction Model
↓
LLM Explanation Generation
↓
Prediction + Explanation Returned to User

---

# 📂 Project Structure

```
medimitra-ai
│
├── llm
│   ├── explain_result.py
│   └── symptom_extractor.py
│
├── medimitra
│   ├── __init__.py
│   ├── nlp_utils.py
│   └── predict.py
│
├── model
│   ├── disease_model.pkl
│   ├── label_encoder.pkl
│   └── symptom_columns.pkl
│
├── app.py
├── frontend.py
├── requirements.txt
├── train_model.py
└── README.md
```

---

# ⚙️ How It Works

### 1. User describes symptoms

Example input:

```
I have headache, nausea, visual disturbances and sensitivity to light
```

### 2. Symptom Extraction

The NLP module identifies known symptoms from the text.

Example:

```
["nausea", "headache", "visual disturbances", "sensitivity to light"]
```

### 3. Disease Prediction

A trained ML model predicts the most likely disease and provides a confidence score.

Example output:

```
Predicted Disease: Migraine
Confidence: 20.5%
```

### 4. LLM Explanation

An LLM generates a simple explanation of the prediction for the user.

---

# 🧪 How to Test MediMitra

You can test MediMitra in two ways.

---

## Option 1 — Using the Live Website

1. Open the Streamlit app link
2. Type your symptoms in the chat input
3. Press Enter
4. View the predicted disease, confidence score, and explanation

### Example test inputs

Try entering:

```
I have excessive hunger, polyuria, weight loss and fatigue
```

```
I have headache, chest pain, dizziness and loss of balance
```

```
I have yellowing of eyes, dark urine, fatigue and itching
```

---

## Option 2 — Using the API

You can test the backend API directly.

1. Open the API docs link:

```
https://medimitra-api.onrender.com/docs
```

2. Find the **POST /chat** endpoint

3. Click **Try it out**

4. Use this request body:

```json
{
 "message": "I have excessive hunger, polyuria, weight loss and fatigue"
}
```

5. Click **Execute**

Example response:

```json
{
  "predicted_disease": "Diabetes",
  "confidence": 37,
  "explanation": "Based on the symptoms described..."
}
```

---

# 🚀 Running the Project Locally

### 1. Clone the repository

```
git clone https://github.com/k-shushh/MediMitra-AI.git
cd medimitra-ai
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Set environment variable

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 4. Run the backend

```
uvicorn app:app --reload
```

API will start at:

```
http://127.0.0.1:8000
```

---

### 5. Run the frontend

```
streamlit run frontend.py
```

---

# 📊 Machine Learning Model

The disease prediction model is trained using medical symptom datasets.

Model pipeline includes:

* symptom feature encoding
* probability-based disease prediction
* confidence thresholding for uncertain predictions

---

# 🔮 Future Improvements

* Doctor recommendation system
* Multi-language support
* Medical knowledge graph integration
* Symptom severity analysis
* Patient history tracking

---

# 👩‍💻 Author

Khushi Gupta

---

# 📜 License

This project is intended for educational and research purposes.


