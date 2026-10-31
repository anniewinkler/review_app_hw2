# Think Pink Clothing: feedback app (starter)

Imagine you run a clothing company. Customers leave feedback, you store it, and you analyze the
data later. The app has two tabs.

**Customer tab:** type a comment and choose a star rating (1 to 5) and choose 
true to size, runs small, or runs large. The app labels the comment
(positive or negative) and saves it to `feedback.csv`.

**Owner tab:** the analysis, which shows:
1. how many comments are positive vs negative,
2. the average star rating for each label
3. how many comments are true to size, runs small, or runs large 
4. the comments to read carefully: a positive label with a low rating, or a negative label
   with a high rating (or a label that is unclear).

The app starts empty. Add comments live. `demo_comments.csv` has 20 fictional comments with
ratings that you can type in (or copy from) to fill it up.

## Files
- `app.py`: the Streamlit app
- `labeler.py`: the function that asks the LLM for a label
- `logo.png`, `logo.svg`: the company logo
- `demo_comments.csv`: sample comments to type in, not loaded automatically
- `requirements.txt`: packages Streamlit Cloud installs for you

## Run it online for free (no terminal)
1. Put these files in a public GitHub repository (upload them in the browser).
2. On share.streamlit.io, create an app from the repository, main file `app.py`.
3. Under Advanced settings, add a secret: `GROQ_API_KEY = "your key"` (a free Groq key, no credit card).
Saved files can disappear when the app restarts, so use the Download CSV button.

## If something goes wrong
- `KeyError: 'GROQ_API_KEY'` means the secret is missing or named differently. Add it under the app's Secrets.
- A 404 error means the model was retired. Find a current one at console.groq.com/docs/models and change `MODEL` in `labeler.py`.
- A 429 error means too many requests. Wait a minute and try again.
