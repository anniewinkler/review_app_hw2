import requests
import streamlit as st

# ---- Settings ----------------------------------------------------------
BUSINESS = "a pizza delivery company"
LABELS = ["positive", "negative"]
GUIDE = """Label the comment with exactly one word: positive or negative.
If it has praise and a complaint, label by the bigger problem.
Sarcasm counts as negative."""
MODEL = "openai/gpt-oss-20b"   # if you get a 404, the model was retired: see console.groq.com/docs/models
URL = "https://api.groq.com/openai/v1/chat/completions"
# ------------------------------------------------------------------------


def label_comment(text):
    key = st.secrets["GROQ_API_KEY"]
    prompt = f"You label customer comments for {BUSINESS}.\n{GUIDE}\n\nComment: {text}"
    response = requests.post(
        URL,
        headers={"Authorization": f"Bearer {key}"},
        json={"model": MODEL, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]
    label = answer.strip().lower()
    return label if label in LABELS else "unclear"
