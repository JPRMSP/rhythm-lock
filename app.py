import streamlit as st
import time
import json
import os

# Set the page config
st.set_page_config(page_title="Keystroke Biometric Authentication", layout="centered")
st.title("🔐 Keystroke Pattern Authentication")
st.markdown("A Simple Behavioral Biometric System using Typing Rhythm (No ML, No Dataset)")

# Function to record time between keystrokes
def record_timing():
    if "last_time" not in st.session_state:
        st.session_state.last_time = time.time()
        return 0
    else:
        now = time.time()
        diff = now - st.session_state.last_time
        st.session_state.last_time = now
        return round(diff, 3)

# Load saved pattern
def load_saved_pattern():
    if os.path.exists("pattern.json"):
        with open("pattern.json", "r") as f:
            return json.load(f)
    return None

# Save typing pattern
def save_pattern(pattern):
    with open("pattern.json", "w") as f:
        json.dump(pattern, f)

# Reset timing state
def reset():
    st.session_state.key_times = []
    st.session_state.last_time = None

# Initialize session
if "key_times" not in st.session_state:
    reset()

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📝 Enroll", "🔐 Authenticate", "📊 View Saved Pattern"])

# ---------------------- TAB 1: ENROLL ----------------------
with tab1:
    st.subheader("Step 1: Enroll Your Typing Pattern")
    st.markdown("Type the password **exactly** once to capture your typing rhythm and save it.")
    
    # Define the fixed password
    password = "secure123"
    st.write(f"Password to type: **{password}**")

    # Input box
    typed = st.text_input("Type the password here:", key="enroll_input", type="password", on_change=record_timing)

    if typed:
        if len(typed) > 1:
            st.session_state.key_times.append(record_timing())

    # Reset button
    if st.button("🔁 Reset"):
        reset()
        st.success("Reset successful.")

    # Save button
    if st.button("✅ Save Pattern"):
        if typed == password and len(st.session_state.key_times) == len(password) - 1:
            save_pattern(st.session_state.key_times)
            st.success("Typing pattern saved successfully!")
        else:
            st.warning("Please type the password correctly before saving.")

# ---------------------- TAB 2: AUTHENTICATE ----------------------
with tab2:
    st.subheader("Step 2: Authenticate Using Typing Rhythm")
    st.markdown("Type the same password. We’ll check if your timing pattern matches.")

    typed_auth = st.text_input("Type the password here:", key="auth_input", type="password", on_change=record_timing)

    if typed_auth:
        if len(typed_auth) > 1:
            st.session_state.key_times.append(record_timing())

    if st.button("🔍 Authenticate"):
        stored = load_saved_pattern()
        if not stored:
            st.error("No pattern saved yet. Please enroll first.")
        elif typed_auth != password:
            st.error("Password incorrect. Try again.")
        elif len(st.session_state.key_times) != len(stored):
            st.error("Pattern length mismatch. Try again.")
        else:
            diff = sum(abs(a - b) for a, b in zip(st.session_state.key_times, stored))
            if diff < 1.0:  # threshold in seconds
                st.success("✅ Access Granted")
            else:
                st.error("❌ Access Denied")
            st.info(f"Timing difference: `{round(diff, 3)}s`")
        reset()

# ---------------------- TAB 3: VIEW SAVED PATTERN ----------------------
with tab3:
    st.subheader("Stored Typing Pattern")
    pattern = load_saved_pattern()
    if pattern:
        st.code(f"Keystroke timing pattern: {pattern}")
        st.success("Pattern loaded from pattern.json")
    else:
        st.warning("No pattern saved yet.")
