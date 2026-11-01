import requests
import streamlit as st

# ---- Settings ----------------------------------------------------------
BUSINESS = "a retail clothing company"
LABELS = ["positive", "negative", "other"]
GUIDE = """Label the comment with exactly one word: positive, negative, or other.
- positive: the customer is happy with the item or order (fit, quality, look, feel, value).
- negative: the customer is unhappy with the item or order (fit, quality, defects, looks, value).
- other: the comment is only about something besides the item itself, such as the app or website,
  packaging, delivery or shipping, or customer service.
If the comment says anything about the item itself, label it by the item and not other.
If the comment about the item is lukewarm, pick the side it leans toward.
Sarcasm counts as negative.
Answer with the one word only."""

EXAMPLES = """Examples:
Comment: Perfect fit and so soft. Already ordered a second color!
Label: positive

Comment: Runs a little snug but I love it, kept it.
Label: positive

Comment: Looks nice but way too small and the stitching is coming loose.
Label: negative

Comment: Arrived late and the zipper was broken. Returning it.
Label: negative

Comment: The app kept crashing when I tried to check out. Took me three tries.
Label: other

Comment: Box was crushed and the bag was ripped open, but I haven't tried the clothes yet.
Label: other

Comment: Shipping took two weeks and nobody answered my emails.
Label: other"""
MODEL = "openai/gpt-oss-20b"   # if you get a 404, the model was retired: see console.groq.com/docs/models
URL = "https://api.groq.com/openai/v1/chat/completions"
# ------------------------------------------------------------------------


def label_comment(text):
    key = st.secrets["GROQ_API_KEY"]
    prompt = f"You label customer comments for {BUSINESS}.\n{GUIDE}\n\n{EXAMPLES}\n\nComment: {text}\nLabel:"
    response = requests.post(
        URL,
        headers={"Authorization": f"Bearer {key}"},
        json={"model": MODEL, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]
    label = answer.strip().lower().strip(".!\"'")   # tolerate stray punctuation
    return label if label in LABELS else "unclear"
