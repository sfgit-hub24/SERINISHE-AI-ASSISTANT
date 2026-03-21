import streamlit as st
from datetime import date, timedelta, datetime

st.set_page_config(page_title="Serenishe", layout="centered")

# -----------------------------
# SIMPLE LOCAL AUTH SYSTEM
# -----------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------
# UI STYLING (IMPROVED)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #f6f2ff;
    color: #2d2d2d;
}

/* USER MESSAGE */
.chat-user {
    background-color: #4a90e2;
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
    font-size: 15px;
}

/* BOT MESSAGE */
.chat-bot {
    background-color: #e9ddff;
    color: #2d2d2d;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
    font-size: 15px;
}

/* BUTTONS */
.stButton>button {
    border-radius: 12px;
    padding: 8px 18px;
    font-weight: 500;
}

/* INPUT BOX */
input {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# AUTH UI
# -----------------------------
if not st.session_state.user:
    st.title("🌸 Serenishe")
    st.subheader("Your Calm Space 💙")

    menu = ["Login", "Sign Up"]
    choice = st.radio("Select", menu, horizontal=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.session_state.user = email
                st.success("Logged in 💖")
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        if st.button("Create Account"):
            if email in st.session_state.users:
                st.error("User already exists")
            else:
                st.session_state.users[email] = password
                st.success("Account created! Please login 💙")

# -----------------------------
# MAIN APP
# -----------------------------
else:
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.image("serinishe_logo.png", width=250)

    st.markdown("<h2 style='text-align:center;'>🌸 Serenishe</h2>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    if "mood_data" not in st.session_state:
        st.session_state.mood_data = []

    if "mode" not in st.session_state:
        st.session_state.mode = None

    st.sidebar.success(f"Logged in as {st.session_state.user} ✅")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    option = st.sidebar.selectbox(
        "Choose Feature",
        ["Chat 💬", "Mood Tracker 😊", "Panic Mode 🚨", "Chat History 📜", "Period Tracker 🩸"]
    )

    def get_ai_response(text):
        text = text.lower()

        if "stress" in text or "overwhelmed" in text:
            return "I hear you 💙 Let’s slow things down together. Take a deep breath 🫁"
        elif "sad" in text:
            return "I’m here with you 💙 You’re not alone."
        elif "anxious" in text or "panic" in text:
            return "You’re safe 💙 Breathe with me."
        else:
            return "I’m here for you 💬 Tell me what’s on your mind."

    if option == "Chat 💬":
        st.subheader("💬 Talk to Serenishe")

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

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bot'>🌸 {msg['content']}</div>", unsafe_allow_html=True)

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

        if st.session_state.mode == "breathing":
            st.info("Let’s breathe together 🫁")
            st.write("Inhale 4 → Hold 4 → Exhale 6")

            if st.button("Done"):
                st.session_state.mode = None
                st.rerun()

        if st.session_state.mode == "exercise":
            st.info("Let’s reset your mind 🌿")
            st.write("✨ Stretch • 💧 Hydrate • 🚶 Walk • 🫁 Breathe")

            if st.button("Done "):
                st.session_state.mode = None
                st.rerun()

    elif option == "Mood Tracker 😊":
        st.subheader("😊 Mood Tracker")

        mood = st.radio("How do you feel?", ["😊 Happy", "😐 Okay", "😔 Sad", "😣 Stressed"])

        if st.button("Save Mood"):
            mood_map = {"😊 Happy": 4, "😐 Okay": 3, "😔 Sad": 2, "😣 Stressed": 1}
            st.session_state.mood_data.append({
                "time": datetime.now().strftime("%H:%M"),
                "value": mood_map[mood]
            })
            st.success("Saved 💙")

        if st.session_state.mood_data:
            values = [m["value"] for m in st.session_state.mood_data]
            st.line_chart(values)

    elif option == "Panic Mode 🚨":
        st.subheader("🚨 Panic Support")
        st.error("You're safe 💙 Stay with me")

        if st.button("Start Breathing"):
            st.info("Inhale 4 → Hold 4 → Exhale 6")

        if st.button("Try Something Else"):
            st.write("✨ Splash water • Sit down • Focus around you")

        if st.button("🚨 SOS"):
            st.warning("Contacting emergency support 🚨")

    elif option == "Chat History 📜":
        st.subheader("📜 Chat History")

        for chat in reversed(st.session_state.chat_log):
            st.write(chat)

    elif option == "Period Tracker 🩸":
        st.subheader("🩸 Period Tracker")

        last = st.date_input("Last Period", date.today())
        cycle = st.slider("Cycle Length", 21, 35, 28)

        if st.button("Predict"):
            st.success(f"Next period: {last + timedelta(days=cycle)}")

    st.markdown("---")
    st.caption("🌸 Serenishe | Your calm space 💙")
