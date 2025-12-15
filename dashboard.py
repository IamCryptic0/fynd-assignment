import streamlit as st
import pandas as pd
import os
from datetime import datetime, timezone
from utils.LLM_helper import generate_user_response

DATA_PATH = "user/data.csv"

st.set_page_config(page_title="User Feedback", layout="centered")
st.title("Submit Your Review")


os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_PATH) or os.stat(DATA_PATH).st_size == 0:
    df = pd.DataFrame(columns=["timestamp", "rating", "review", "ai_response"])
    df.to_csv(DATA_PATH, index=False)
else:
    df = pd.read_csv(DATA_PATH)

rating = st.selectbox(
    "Select a rating", 
    options=["Select", 1, 2, 3, 4, 5],
    index=0
)
review = st.text_area("Write your review")

if st.button("Submit Review"):
    if rating == "Select":
        st.warning("Please select a rating before submitting.")
    elif not review.strip():
        st.warning("Please write a review before submitting.")
    else:
        with st.spinner("Submitting"):
            ai_response = generate_user_response(review, rating)

        new_row = {
            "timestamp": datetime.now().strftime("%H:%M:%S, %d/%m/%Y"),
            "rating": rating,
            "review": review,
            "ai_response": ai_response
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)

        st.success("Review submitted successfully!")
        st.write(ai_response)
