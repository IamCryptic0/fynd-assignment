import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv(dotenv_path=".env")
load_dotenv()

GEMINI_API_KEY = (
    st.secrets.get("GEMINI_API_KEY")
    if "GEMINI_API_KEY" in st.secrets
    else os.getenv("GEMINI_API_KEY")
)
genai.configure(api_key=GEMINI_API_KEY)

def generate_user_response(review_text, rating):

    prompt = f"""
You are a customer support AI for an e-commerce platform.

User Rating: {rating} stars
User Review: "{review_text}"

Write a polite, empathetic, and helpful response.
Keep it short (1–2 sentences).
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip()

def generate_summary(review_text):
    prompt = f"""
Summarize the following customer review in ONE concise sentence.

Review:
"{review_text}"
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip()

# def generate_recommended_action(review_text, rating):
#     prompt = f"""
# You are a product manager.

# User rating: {rating}
# User review:
# "{review_text}"

# Suggest ONE clear action the team should take.
# """

#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=prompt
#     )

#     return response.text.strip()

def generate_recommended_action(review_text, rating):
    prompt = f"""
You are a product manager reviewing customer feedback.

User rating: {rating}
User review:
"{review_text}"

Based on the feedback, suggest 2 to 3 recommended actions for the internal team.

STRICT RULES (must follow exactly):
- Each action must be ONLY 2–3 words
- Each action must be on a new line
- Do NOT use full sentences
- Do NOT include explanations or reasoning
- Do NOT use bullet points, numbering, or punctuation
- Use short operational verbs only (e.g., Monitor trends, Investigate issue, Improve UX, Escalate issue)

Good examples:
Monitor trends
Investigate issue
Check quality
Contact user

Bad examples (do NOT do this):
Investigate root cause of sentiment
Improve the feedback collection process
Monitor review patterns for similar feedback

Return ONLY the actions, nothing else.
"""


    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip()

