import requests
import streamlit as st

# ---- Settings ----------------------------------------------------------
BUSINESS = "a retail clothing company"
LABELS = ["positive", "neutral", "negative"]
GUIDE = """Label the comment with exactly one word: positive, neutral, or negative.
Judge the customer's overall feeling about their order.
- positive: clearly happy or satisfied. Praise, would recommend or buy again.
- negative: clearly unhappy. Mostly complaints, a return, a defect, or a serious problem.
- neutral: lukewarm, mixed, or flat. Says it is ok, fine, or average; has good and bad points that
  roughly balance out; or only states facts with no real feeling.
A small complaint inside an otherwise happy comment is still positive.
A small compliment inside an unhappy comment is still negative.
When the comment is truly in the middle, answer neutral. Sarcasm counts as negative.
Answer with the one word only."""

EXAMPLES = """Examples:
Comment: Perfect fit and so soft. Already ordered a second color!
Label: positive

Comment: It's fine. Does the job, nothing special.
Label: neutral

Comment: Cute but the fabric is thinner than I hoped. Not sure if I'll keep it.
Label: neutral

Comment: Zipper broke on the first wear and it came late. Returning it.
Label: negative

Comment: Runs a little snug but I love it, kept it.
Label: positive

Comment: Looks nice but way too small and the stitching is coming loose.
Label: negative"""
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
