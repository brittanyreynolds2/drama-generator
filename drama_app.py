
import streamlit as st
import openai

st.set_page_config(page_title="Drama Generator", layout="centered")

# Load API key securely (set in Streamlit Cloud -> Secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Scenario setup
scenario_intro = """
You are a frustrated tenant. Your air conditioner has been broken for three days in July, and no one has given you a status update. You are hot, tired, and frustrated. You want answers.
"""
initial_message = "Hi, I’m calling because it’s been *three days* without AC and I haven’t heard anything back. It’s July! This is not okay."

# App UI
st.title("🏠 Property Management Drama Generator")
st.subheader("Scenario: Angry Tenant – Broken AC")

# Chat setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": scenario_intro},
        {"role": "assistant", "content": initial_message}
    ]

# Display existing messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User response input
if user_input := st.chat_input("How do you respond?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state.messages,
        temperature=0.7,
    )
    reply = response.choices[0].message
    st.session_state.messages.append(reply)

    with st.chat_message("assistant"):
        st.markdown(reply.content)

# Feedback after 3+ turns
if len(st.session_state.messages) >= 7:
    st.divider()
    st.subheader("📋 AI Feedback")
    feedback_prompt = """
You are a coach reviewing how a property manager handled a tenant complaint. Based on the conversation, rate their:
- Communication tone
- Empathy
- Conflict resolution
- Professionalism

Give constructive feedback in 3–4 sentences.
"""
    feedback_messages = st.session_state.messages + [{"role": "user", "content": feedback_prompt}]
    feedback = openai.ChatCompletion.create(
        model="gpt-4",
        messages=feedback_messages,
        temperature=0.5
    )
    st.markdown(feedback.choices[0].message.content)
