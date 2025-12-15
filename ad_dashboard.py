import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.LLM_helper import generate_summary, generate_recommended_action

DATA_PATH = "user/data.csv"

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("Admin Dashboard – User Feedback")

# ---------- Load Data Safely ----------
if not os.path.exists(DATA_PATH) or os.stat(DATA_PATH).st_size == 0:
    st.info("No submissions yet.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# ---------- Ensure Required Columns ----------
for col in ["timestamp", "rating", "review", "summary", "recommended_action"]:
    if col not in df.columns:
        df[col] = ""

# ---------- Parse Timestamp (for filtering & sorting only) ----------
df["timestamp_dt"] = pd.to_datetime(
    df["timestamp"],
    format="%H:%M:%S, %d/%m/%Y",
    errors="coerce"
)

# ---------- Generate ----------
with st.spinner("Generating AI insights where missing..."):
    for idx in range(len(df)):
        if pd.isna(df.at[idx, "summary"]) or df.at[idx, "summary"] == "":
            df.at[idx, "summary"] = generate_summary(df.at[idx, "review"])

        if pd.isna(df.at[idx, "recommended_action"]) or df.at[idx, "recommended_action"] == "":
            df.at[idx, "recommended_action"] = generate_recommended_action(
                df.at[idx, "review"],
                df.at[idx, "rating"]
            )

    df.to_csv(DATA_PATH, index=False)

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")

# Rating range filter (default 1–5)
rating_from, rating_to = st.sidebar.slider(
    "Rating Range",
    min_value=1,
    max_value=5,
    value=(1, 5)
)

# Rating sorting
rating_sort = st.sidebar.selectbox(
    "Sort by Rating",
    ["None", "High → Low", "Low → High"],
    index=0
)

# Date ordering (default Latest First)
date_filter = st.sidebar.selectbox(
    "Date Order",
    ["Latest First", "Oldest First", "Custom Range"],
    index=0
)

# ---------- APPLY FILTERS ----------
filtered_df = df.copy()

# Rating range filter
filtered_df = filtered_df[
    (filtered_df["rating"] >= rating_from) &
    (filtered_df["rating"] <= rating_to)
]

# Date filter
if date_filter == "Custom Range":
    min_date = filtered_df["timestamp_dt"].min().date()
    max_date = filtered_df["timestamp_dt"].max().date()

    start_date, end_date = st.sidebar.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    filtered_df = filtered_df[
        (filtered_df["timestamp_dt"].dt.date >= start_date) &
        (filtered_df["timestamp_dt"].dt.date <= end_date)
    ]

elif date_filter == "Latest First":
    filtered_df = filtered_df.sort_values("timestamp_dt", ascending=False)

elif date_filter == "Oldest First":
    filtered_df = filtered_df.sort_values("timestamp_dt", ascending=True)

# Rating sorting (applied last)
if rating_sort == "High → Low":
    filtered_df = filtered_df.sort_values("rating", ascending=False)

elif rating_sort == "Low → High":
    filtered_df = filtered_df.sort_values("rating", ascending=True)

# ---------- METRICS ----------
st.subheader("📈 Metrics (Filtered View)")

if filtered_df.empty:
    st.warning("No reviews match the selected filters.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Reviews", len(filtered_df))

    with col2:
        st.metric("Average Rating", round(filtered_df["rating"].mean(), 2))

st.divider()

# ---------- DISPLAY REVIEWS ----------
st.subheader("🗂️ Reviews")

for _, row in filtered_df.iterrows():
    with st.container():
        st.markdown(f"**Submitted:** {row['timestamp']}")
        st.markdown(f"**Rating:** {row['rating']}")
        st.markdown(f"**Review:** {row['review']}")
        st.markdown(f"**Summary:** {row['summary']}")
        st.markdown("**Recommended Actions:**")
        st.text(row["recommended_action"])
        st.divider()
