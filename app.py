import streamlit as st
import time
import google.generativeai as genai
import re

# --- Setup ---
st.set_page_config(page_title="Youth AI Companion", page_icon="💬", layout="wide")

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! 👋 How are you feeling today? Let’s chat whenever you’re ready."}
    ]
if "mood" not in st.session_state:
    st.session_state.mood = "😐"  # default

# --- Mood Selector (separate UI section, not inside chat) ---
st.sidebar.header("💙 Your Mood")
st.session_state.mood = st.sidebar.select_slider(
    "How’s your mood today?",
    options=["😞", "😕", "😐", "🙂", "😄"],
    value=st.session_state.mood
)


# --- Sanitizer (strip unsafe HTML if Gemini returns some) ---
def sanitize_text(text: str) -> str:
    return re.sub(r"<.*?>", "", text)


# --- Chat Display with `st.chat_message` ---
# This is the fixed part. It uses the native Streamlit component.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(sanitize_text(msg["content"]))

# --- User Input ---
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display the new user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("💭 Thinking..."):
        time.sleep(1)  # simulate delay

        # --- AI Response ---
        try:
            response = model.generate_content(
                f"You are a kind and supportive AI for youth mental wellness. "
                f"Respond empathetically to this input: {user_input}. "
                f"User’s mood: {st.session_state.mood}"
            )

            if hasattr(response, "text"):
                ai_response = response.text
            elif hasattr(response, "candidates") and len(response.candidates) > 0:
                ai_response = response.candidates[0].content.parts[0].text
            else:
                ai_response = "⚠ Sorry, I couldn’t generate a response."
        except Exception:
            ai_response = f"(DEBUG MODE) I heard you say '{user_input}'. Mood: {st.session_state.mood}."

        # Store and display assistant response
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)