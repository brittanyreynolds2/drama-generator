import streamlit as st
import pandas as pd
import openai
import os

st.set_page_config(page_title="Drama Generator", layout="centered")

st.title("🎭 Property Management Drama Generator")
st.markdown("Inject a little chaos. Respond like a pro.")

# Upload OpenAI API Key
openai_key = st.text_input("Enter your OpenAI API Key", type="password")
if openai_key:
    openai.api_key = openai_key

# Load scenarios
@st.cache_data
def load_scenarios():
    return pd.read_csv("scenarios.csv")

df = load_scenarios()

# Dropdown for scenario selection
selected = st.selectbox("Choose your drama scenario:", df["Title"].tolist())

# Display scenario content
scenario = df[df["Title"] == selected].iloc[0]
st.subheader("📬 The Situation:")
st.markdown(scenario["Scenario"])

st.subheader("🧠 How Would You Respond?")
user_input = st.text_area("Write your response here...")

# Get coaching feedback using OpenAI
if st.button("🧑‍🏫 Get Feedback") and user_input and openai_key:
    with st.spinner("Getting coaching feedback..."):
        prompt = f"""You're a workplace conflict coach helping someone respond professionally to a property management issue. 
Here’s the scenario: "{scenario['Scenario']}"
Here’s their drafted response: "{user_input}"
Provide specific coaching feedback: what's good, what could be improved, and what to say instead."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        feedback = response.choices[0].message.content
        st.success("Here’s your coaching feedback:")
        st.markdown(feedback)
