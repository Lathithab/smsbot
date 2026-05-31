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
    st.markdown("---")
    st.subheader("🧪 Try these examples")
    sample_messages = [
        "Congratulations! You've won a R5,000 Woolworths voucher. Click here to claim: bit.ly/claim-now",
        "Your OTP is 482910. Do not share this with anyone.",
        "Hi, are we still meeting at 3pm today?",
        "URGENT: Your account has been suspended. Verify now at secure-login.co.za",
    ]
    for sample in sample_messages:
        if st.button(sample[:50] + "...", use_container_width=True, key=sample):
            st.session_state.prefill = sample
            st.rerun()

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

# Handle prefilled sample message
if "prefill" in st.session_state:
    prefill = st.session_state.pop("prefill")
    # Process it directly as if the user typed it
    with st.chat_message("user"):
        st.markdown(prefill)
    with st.chat_message("assistant", avatar="🛡️"):
        with st.spinner("Analysing..."):
            label, confidence, advice = check_spam(prefill, st.session_state.token)
        if label.lower() == "spam":
            st.error(f"🚨 **SPAM** — {confidence:.1f}% confidence")
        elif label.lower() == "error":
            st.warning("⚠️ Could not classify this message.")
        else:
            st.success(f"✅ **Safe** — {confidence:.1f}% confidence")
        st.progress(confidence / 100)
        st.markdown(advice)
    st.session_state.history.append((prefill, label, confidence, advice))



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