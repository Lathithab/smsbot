import streamlit as st
from spam_checker import get_nyckel_token, check_spam

st.set_page_config(page_title="Cindy the Cyber Companion", page_icon="🛡️")
st.title("🛡️ Cindy the Cyber Companion")

# --- Session state init ---
if "history" not in st.session_state:
    st.session_state.history = []
if "token" not in st.session_state:
    with st.spinner("Connecting to spam detection service..."):
        st.session_state.token = get_nyckel_token()
    if st.session_state.token is None:
        st.error("❌ Failed to authenticate. Please check your Nyckel credentials.")
        st.stop()

# --- Sidebar ---
with st.sidebar:
    st.subheader("About Cindy")
    st.write("""
    Cindy uses **Nyckel's SMS Spam Identifier** to detect spam with AI.

    - 🔍 **Spam Detection** — flags scams and unwanted messages  
    - 📊 **Confidence Score** — shows how certain the AI is  
    - 💬 **Chat History** — tracks all checked messages  
    """)
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()
    st.caption(f"Messages checked: {len(st.session_state.history)}")

# --- Chat history display ---
# Greeting
with st.chat_message("assistant", avatar="🛡️"):
    st.markdown(
        "Hi! I'm **Cindy**, your cyber companion. "
        "Paste any suspicious message below and I'll tell you if it's spam! 👇"
    )

# Render history
for msg, label, confidence, advice in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(msg)
    with st.chat_message("assistant", avatar="🛡️"):
        if label.lower() == "spam":
            st.error(f"🚨 **SPAM** — {confidence:.1f}% confidence")
        elif label.lower() == "error":
            st.warning("⚠️ Could not classify this message.")
        else:
            st.success(f"✅ **Safe** — {confidence:.1f}% confidence")
        st.progress(confidence / 100)
        st.markdown(advice)

# --- Chat input (sits at bottom, submits on Enter) ---
incoming_sms = st.chat_input("Paste a message to check...")

if incoming_sms:
    if not incoming_sms.strip():
        st.warning("Please enter a message!")
    else:
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(incoming_sms)

        with st.chat_message("assistant", avatar="🛡️"):
            with st.spinner("Analysing..."):
                # Retry token if needed
                if st.session_state.token is None:
                    st.session_state.token = get_nyckel_token()

                label, confidence, advice = check_spam(incoming_sms, st.session_state.token)

            if label.lower() == "spam":
                st.error(f"🚨 **SPAM** — {confidence:.1f}% confidence")
            elif label.lower() == "error":
                st.warning("⚠️ Could not classify this message.")
            else:
                st.success(f"✅ **Safe** — {confidence:.1f}% confidence")
            st.progress(confidence / 100)
            st.markdown(advice)

        st.session_state.history.append((incoming_sms, label, confidence, advice))