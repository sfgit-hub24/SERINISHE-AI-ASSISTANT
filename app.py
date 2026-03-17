import streamlit as st
from datetime import date, timedelta, datetime

st.set_page_config(page_title="Serenishe", layout="centered")

# -----------------------------
# UI STYLING
# -----------------------------
st.markdown("""
<style>
.chat-user {
    background-color: #cce5ff;
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin: 6px 0;
    text-align: right;
}
.chat-bot {
    background-color: #d9c6ff;
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin: 6px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER (LOGO)
# -----------------------------
col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.image("serinishe_logo.png", width=300)

st.markdown("<h1 style='text-align:center;'>🌸 Serenishe</h1>", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "mood_data" not in st.session_state:
    st.session_state.mood_data = []

if "mode" not in st.session_state:
    st.session_state.mode = None

# -----------------------------
# SIDEBAR
# -----------------------------
option = st.sidebar.selectbox(
    "Choose Feature",
    ["Chat 💬", "Mood Tracker 😊", "Panic Mode 🚨", "Chat History 📜", "Period Tracker 🩸"]
)

# -----------------------------
# AI RESPONSE
# -----------------------------
def get_ai_response(text):
    text = text.lower()

    if "stress" in text or "overwhelmed" in text:
        return """I hear you 💙 Things feel heavy right now.

Maybe we can slow things down together:

🫁 Take a few deep breaths  
🧠 Focus on just one small thing  
💬 Or talk it out with me"""

    elif "sad" in text or "not well" in text:
        return "I'm really sorry you're feeling this way 💙 I'm here with you. You can share anything."

    elif "anxious" in text or "panic" in text:
        return "You're safe 💙 Let’s slow things down together. I'm right here with you."

    else:
        return "I'm here for you 💬 Tell me what's on your mind."

# -----------------------------
# CHAT
# -----------------------------
if option == "Chat 💬":
    st.subheader("💬 Talk to Serenishe")

    st.markdown("### 💬 Continue your conversation below")

    # INPUT FIRST (scroll-like behavior)
    user_input = st.text_input("Type your message...")

    if st.button("Send"):
        if user_input:
            reply = get_ai_response(user_input)

            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "bot", "content": reply})

            st.session_state.chat_log.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "user": user_input,
                "bot": reply
            })

            st.rerun()

    # CHAT DISPLAY
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bot'>🌸 {msg['content']}</div>", unsafe_allow_html=True)

    # QUICK OPTIONS
    if len(st.session_state.messages) > 0:
        st.markdown("---")
        st.write("### 💡 What would help you right now?")

        col1, col2, col3 = st.columns(3)

        if col1.button("🫁 Calm Down"):
            st.session_state.mode = "breathing"

        if col2.button("🧠 Exercises"):
            st.session_state.mode = "exercise"

        if col3.button("💬 Continue Chat"):
            st.session_state.mode = None
            st.rerun()

    # BREATHING MODE
    if st.session_state.mode == "breathing":
        st.info("Let’s breathe together 🫁")

        st.write("""
Inhale for 4 seconds  
Hold for 4 seconds  
Exhale for 6 seconds  
""")

        if st.button("Done"):
            st.session_state.mode = None
            st.rerun()

    # EXERCISE MODE
    if st.session_state.mode == "exercise":
        st.info("Let’s reset your mind 🌿")

        st.write("""
✨ Stretch your shoulders  
✨ Drink water  
✨ Take a short walk  
✨ Deep breathing  
""")

        if st.button("Done "):
            st.session_state.mode = None
            st.rerun()

# -----------------------------
# MOOD TRACKER
# -----------------------------
elif option == "Mood Tracker 😊":
    st.subheader("😊 Mood Tracker")

    mood = st.radio("How do you feel?", ["😊 Happy", "😐 Okay", "😔 Sad", "😣 Stressed"])

    if st.button("Save Mood"):
        mood_map = {"😊 Happy": 4, "😐 Okay": 3, "😔 Sad": 2, "😣 Stressed": 1}

        st.session_state.mood_data.append({
            "time": datetime.now().strftime("%H:%M"),
            "value": mood_map[mood]
        })

        st.success("Mood saved 💙")

    if st.session_state.mood_data:
        st.write("### 📊 Mood Trend")
        values = [m["value"] for m in st.session_state.mood_data]
        st.line_chart(values)
        st.caption("1 = Stressed 😣 → 4 = Happy 😊")

# -----------------------------
# PANIC MODE
# -----------------------------
elif option == "Panic Mode 🚨":
    st.subheader("🚨 Panic Support")

    st.error("You're safe 💙 Stay with me")

    if st.button("Start Breathing"):
        st.write("Inhale 4 → Hold 4 → Exhale 6")

    if st.button("Try Something Else"):
        st.write("""
✨ Splash cold water  
✨ Sit down and relax  
✨ Focus on surroundings  
""")

    if st.button("🚨 SOS"):
        st.write("Calling your family member & emergency services immediately")

# -----------------------------
# CHAT HISTORY
# -----------------------------
elif option == "Chat History 📜":
    st.subheader("📜 Chat History")

    for chat in reversed(st.session_state.chat_log):
        st.write(chat)

# -----------------------------
# PERIOD TRACKER
# -----------------------------
elif option == "Period Tracker 🩸":
    st.subheader("🩸 Period Tracker")

    last = st.date_input("Last Period", date.today())
    cycle = st.slider("Cycle Length", 21, 35, 28)

    if st.button("Predict"):
        st.success(f"Next period: {last + timedelta(days=cycle)}")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🌸 Serenishe | Your calm space")

