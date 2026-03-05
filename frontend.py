
import html
import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = "https://medimitra-api.onrender.com/"

st.set_page_config(page_title="MediMitra AI", page_icon="🩺", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0E1117;
    color: #E8EAF0;
}

.medimitra-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #E8EAF0;
    margin-bottom: 0;
}
.medimitra-subtitle {
    font-size: 0.85rem;
    color: #6B7280;
    margin-top: 2px;
    margin-bottom: 20px;
}

/* Chat bubbles */
.user-bubble {
    background: linear-gradient(135deg, #5B21B6, #7C3AED);
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 6px 0 6px 15%;
    color: #fff;
    font-size: 0.95rem;
    line-height: 1.5;
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.bot-header {
    background-color: #1A1D27;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 4px;
    margin: 6px 15% 0 0;
    border: 1px solid #2A2F3D;
    border-bottom: none;
}
.bot-header .disease-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #A78BFA;
    margin-bottom: 6px;
}
.bot-header .confidence-badge {
    display: inline-block;
    background: #1E2433;
    border: 1px solid #374151;
    color: #9CA3AF;
    font-size: 0.78rem;
    padding: 2px 10px;
    border-radius: 20px;
}

/* Expander overrides to match bot bubble style */
.bot-cards {
    margin: 0 15% 6px 0;
}
.bot-cards [data-testid="stExpander"] {
    background-color: #1A1D27 !important;
    border: 1px solid #2A2F3D !important;
    border-top: none !important;
    border-radius: 0 !important;
}
.bot-cards [data-testid="stExpander"]:last-child {
    border-radius: 0 0 18px 18px !important;
}
.bot-cards [data-testid="stExpander"] summary {
    color: #D1D5DB !important;
    font-size: 0.9rem !important;
}
.bot-cards [data-testid="stExpander"] p {
    color: #9CA3AF;
    font-size: 0.88rem;
    line-height: 1.7;
}

.error-bubble {
    background-color: #1A1D27;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 6px 15% 6px 0;
    color: #F87171;
    font-size: 0.92rem;
    border: 1px solid #2A2F3D;
}

.disclaimer {
    font-size: 11.5px;
    color: #4B5563;
    text-align: center;
    margin-top: 12px;
    padding-top: 8px;
    border-top: 1px solid #1F2330;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col1:
    st.markdown('<div class="medimitra-title">🩺 MediMitra AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="medimitra-subtitle">Describe your symptoms and get an AI-powered assessment</div>', unsafe_allow_html=True)
with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, msg in enumerate(st.session_state.messages):

    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-bubble">{html.escape(msg["content"])}</div>',
            unsafe_allow_html=True
        )

    else:
        data = msg.get("data")

        if data is None or data["predicted_disease"] in ("Unable to detect symptoms", "Uncertain"):
            text = data["explanation"] if data else msg["content"]
            st.markdown(
                f'<div class="error-bubble">🤔 {html.escape(text)}</div>',
                unsafe_allow_html=True
            )

        else:
            disease    = html.escape(data["predicted_disease"])
            confidence = data["confidence"]
            explanation = data.get("explanation", {})

            st.markdown(f"""
                <div class="bot-header">
                    <div class="disease-name">🔬 {disease}</div>
                    <span class="confidence-badge">Confidence: {confidence}%</span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="bot-cards">', unsafe_allow_html=True)

            with st.expander("📋 About this condition"):
                st.write(explanation.get("about", "No information available."))

            with st.expander("⚠️ Why it may occur"):
                st.write(explanation.get("causes", "No information available."))

            with st.expander("✅ Precautions"):
                precautions = explanation.get("precautions", "")
                for line in precautions.split("\n"):
                    line = line.strip()
                    if line:
                        st.markdown(f"- {line}")

            st.markdown('</div>', unsafe_allow_html=True)

components.html("""
    <script>
        // Walk up to the Streamlit root and scroll to the bottom
        const root = window.parent.document.querySelector('.main');
        if (root) { root.scrollTo({ top: root.scrollHeight, behavior: 'smooth' }); }
    </script>
""", height=0)

user_input = st.chat_input("Describe your symptoms, e.g. I have back pain, fever and headache...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Analysing symptoms..."):
        try:
            response = requests.post(API_URL, json={"message": user_input}, timeout=30)
            response.raise_for_status()
            data = response.json()

            st.session_state.messages.append({
                "role":    "bot",
                "content": data.get("predicted_disease", ""),
                "data":    data
            })

        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "bot",
                "content": "Could not connect to the backend. Make sure the FastAPI server is running on port 8000.",
                "data": None
            })
        except requests.exceptions.Timeout:
            st.session_state.messages.append({
                "role": "bot",
                "content": "The request timed out. The backend may be overloaded.",
                "data": None
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "bot",
                "content": f"Unexpected error: {str(e)}",
                "data": None
            })

    st.rerun()

st.markdown(
    '<div class="disclaimer">⚠️ MediMitra AI is not a substitute for professional medical advice, '
    'diagnosis, or treatment. Always consult a qualified healthcare professional.</div>',
    unsafe_allow_html=True
)
