import os

import pandas as pd
import plotly.express as px
import streamlit as st

from labeler import label_comment

# ---- Settings ----------------------------------------------------------
TITLE = "Think Pink Clothing"
LOGO = "logo.png"
LOW_RATING, HIGH_RATING = 2, 4      # 2 stars or fewer is low, 4 stars or more is high
CSV_FILE = "feedback.csv"
COLUMNS = ["comment", "rating", "fit", "label"]
FIT_OPTIONS = ["True to size", "Runs small", "Runs large"]
FIT_COLORS = {"True to size": "#2BB38A", "Runs small": "#B34700", "Runs large": "#B34700"}
LABEL_ORDER = ["positive", "negative", "other", "unclear"]
LABEL_COLORS = {"positive": "#2BB38A", "negative": "#B34700", "other": "#9AA0A6", "unclear": "#6C5CE7"}
# ------------------------------------------------------------------------

st.set_page_config(page_title=TITLE, layout="wide")

# Handle missing logo gracefully
if os.path.exists(LOGO):
    st.image(LOGO, width=90)

st.title(TITLE)
st.caption("Customers leave feedback on clothing items & orders. This app labels the review and saves it in our database. The owner can analyze the data at a later time.")


def load_feedback():
    """Load saved feedback. A file from an older version of the app (different columns) is ignored."""
    if os.path.exists(CSV_FILE):
        saved = pd.read_csv(CSV_FILE)
        if all(c in saved.columns for c in COLUMNS):
            return saved[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)


df = load_feedback()

tab_customer, tab_owner = st.tabs(["Customer: leave feedback", "Owner: analyze the feedback"])

# ---- Customer tab: comment, stars, fit, get a label, save --------------------
with tab_customer:
    st.subheader("Tell us about your order")
    with st.form("feedback_form", clear_on_submit=True):
        comment = st.text_area("Your comment", max_chars=200)
        st.caption("Your rating")
        stars = st.feedback("stars")          # nothing until clicked, then 0 to 4
        st.caption("How did it fit?")
        fit = st.pills("How did it fit?", FIT_OPTIONS, selection_mode="single",
                       label_visibility="collapsed")   # nothing until clicked, then the option
        submitted = st.form_submit_button("Send feedback")

    if submitted:
        if not comment.strip() or stars is None or fit is None:
            st.error("Please type a comment, choose a star rating, and tell us how it fit.")
        else:
            try:
                label = label_comment(comment.strip())
            except Exception as e:
                st.error(f"Could not label the comment: {e}")
            else:
                new_row = pd.DataFrame([{"comment": comment.strip(), "rating": stars + 1,
                                         "fit": fit, "label": label}])
                pd.concat([df, new_row], ignore_index=True).to_csv(CSV_FILE, index=False)
                df = load_feedback()
                st.success("Thank you for your feedback!")
                st.caption(f"Behind the scenes, the app labeled it: {label}")

# ---- Owner tab: analyze the feedback ----------------------------------------
with tab_owner:
    if df.empty:
        st.info("No feedback yet. Switch to the customer tab and add the first comment.")
    else:
        # Comments to read carefully: the label and the rating disagree, or the label is unclear
        flag = ((df["label"] == "positive") & (df["rating"] <= LOW_RATING)) \
             | ((df["label"] == "negative") & (df["rating"] >= HIGH_RATING)) \
             | (df["label"] == "unclear")

        st.subheader("What are customers saying?")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Comments", len(df))
        m2.metric("True to size", f"{(df['fit'] == 'True to size').mean():.0%}")
        m3.metric("Positive comments", f"{(df['label'] == 'positive').mean():.0%}")
        m4.metric("Average stars", f"{df['rating'].mean():.1f}")
        m5.metric("Read carefully", int(flag.sum()))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption("Number of comments by fit")
            counts = df["fit"].value_counts().rename_axis("fit").reset_index(name="count")
            fig = px.bar(counts, x="fit", y="count", color="fit", text="count",
                         color_discrete_map=FIT_COLORS, category_orders={"fit": FIT_OPTIONS})
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Comments")
            st.plotly_chart(fig, width="stretch")

        with col2:
            st.caption("Average stars by fit")
            avg = df.groupby("fit")["rating"].mean().round(1).reset_index()
            fig = px.bar(avg, x="fit", y="rating", color="fit", text="rating",
                         color_discrete_map=FIT_COLORS, category_orders={"fit": FIT_OPTIONS},
                         range_y=[0, 5])
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Average stars")
            st.plotly_chart(fig, width="stretch")

        with col3:
            st.caption("Comment label by fit")
            by_fit = df.groupby(["fit", "label"]).size().reset_index(name="count")
            fig = px.bar(by_fit, x="fit", y="count", color="label",
                         color_discrete_map=LABEL_COLORS,
                         category_orders={"fit": FIT_OPTIONS, "label": LABEL_ORDER})
            fig.update_layout(xaxis_title=None, yaxis_title="Comments", legend_title_text=None)
            st.plotly_chart(fig, width="stretch")

        st.subheader("Read these carefully")
        st.caption("The label and the rating disagree (a positive comment with a low rating, a negative comment "
                   "with a high rating), or the label is unclear.")
        st.dataframe(df[flag], hide_index=True, width="stretch")

        with st.expander("All feedback"):
            st.dataframe(df, hide_index=True, width="stretch")
        st.download_button("Download CSV", df.to_csv(index=False), file_name="feedback.csv")
        st.caption("On the free Streamlit Cloud, the saved file can disappear when the app restarts. "
                   "Download your CSV to keep it.")
