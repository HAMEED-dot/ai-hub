import streamlit as st
import google.generativeai as genai

# --- Gemini Setup ---
genai.configure(api_key="AIzaSyBUq1cGxapzhWncpdFa5SfKHcTTfemTtqw")  # Replace with your key
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Basic Page Setup ---
st.set_page_config(page_title="Youth Wellness AI", page_icon="💬", layout="centered")
st.title("💬 Youth Mental Wellness Companion")
st.caption("Confidential • Supportive • AI-powered")

DISCLAIMER = (
    "⚠ I’m an AI prototype for general wellness support, not a medical professional. "
    "If you ever feel unsafe, please reach out to a trusted adult or call your local helpline."
)
st.info(DISCLAIMER)

# --- Mood Check-in ---
st.subheader("How are you feeling today?")
mood = st.select_slider(
    "Mood",
    options=["😞", "😕", "😐", "🙂", "😄"],
    value="😐",
    label_visibility="collapsed"
)
st.write(f"Your mood today: {mood}")

# --- Crisis Detection Keywords ---
CRISIS_KEYWORDS = ["suicide", "kill myself", "hurt myself", "self-harm"]

def crisis_check(user_text: str) -> bool:
    return any(word in user_text.lower() for word in CRISIS_KEYWORDS)

# --- Chat Section ---
st.subheader("Chat with the AI Companion")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New message
user_input = st.chat_input("Type how you feel...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    if crisis_check(user_input):
        ai_response = (
            "💜 I hear you and I’m really sorry you’re feeling this way. "
            "You deserve support right now. Please reach out to someone you trust or call your local helpline."
        )
    else:
        # Use Gemini for AI-generated supportive response
        response = model.generate_content(
            f"You are a kind and supportive AI for youth mental wellness. "
            f"Respond empathetically to this input: {user_input}"
        )
        ai_response = response.text

    # Store AI message
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.rerun()

# --- Resources ---
st.subheader("📚 Helpful Resources")
st.markdown("""
- 🧘 Breathing & grounding exercises  
- 📖 Study stress & exam anxiety tips  
- 🤝 Talk to a trusted adult or school counselor  
- 🆘 [Find a local helpline](https://findahelpline.com)
""")