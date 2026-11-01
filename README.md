# Think Pink Clothing: feedback app

Customers leave feedback on clothing orders, the app labels each comment, and the owner analyzes the results.

**Customer tab:** type a comment (200 characters max), choose a star rating (1 to 5), and pick how it fit
(True to size, Runs small, Runs large). The app asks an LLM to label the comment as positive, negative, or other (not about the item itself, e.g. the app or packaging),
then saves everything to `feedback.csv`.

**Owner tab:** shows
1. the number of comments by fit,
2. the average star rating by fit,
3. positive / negative / other comments within each fit,
4. the comments to read carefully: a positive comment with a low rating, a negative comment with a high rating,
   or a label that is unclear.

## Files
- `app.py`: the Streamlit app
- `labeler.py`: asks the LLM to label a comment
- `requirements.txt`: packages Streamlit Cloud installs
- `logo.png`: optional company logo

## Run it on Streamlit Cloud
1. Put these files in a GitHub repository.
2. On share.streamlit.io, create an app from the repository, main file `app.py`.
3. Under Settings > Secrets, add: `GROQ_API_KEY = "your key"` (underscores, exactly this name).
Saved files can disappear when the app restarts, so use the Download CSV button.

## If something goes wrong
- `st.secrets has no key "GROQ_API_KEY"`: the secret is missing or named differently (check for hyphens).
- A 404 error: the model was retired. Pick a current one at console.groq.com/docs/models and change `MODEL` in `labeler.py`.
- A 429 error: too many requests. Wait a minute and try again.
