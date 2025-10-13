import streamlit as st
from streamlit_chat import message
from spam_checker import get_nyckel_token, check_spam

st.set_page_config(page_title="Cindy the Cyber Companion", layout="wide")
st.title("Cindy the Cyber Companion")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "token" not in st.session_state:
    st.session_state.token = None

# Get token once and cache it in session state
if st.session_state.token is None:
    st.session_state.token = get_nyckel_token()
    if st.session_state.token is None:
        st.error("❌ Failed to authenticate with Nyckel. Please check your credentials.")
        st.stop()


# Bot greeting message
st.markdown("""
<div style='display: flex; justify-content: flex-start; margin-bottom: 10px;'>
    <div style='background-color: #E5E5EA; color: black; padding: 10px 15px; border-radius: 18px; max-width: 70%; word-wrap: break-word;'>
        Hello, I'm your cyber companion, Cindy! 👋 Check any suspicious message with me! Paste your message here to me so I can check it out!
    </div>
</div>
""", unsafe_allow_html=True)

st.chat_message("Hello, I'm your cyber companion, Cindy! 👋 Check any suspicious message with me! Paste your message here to me so I can check it out!", is_user=False)

        

incoming_sms = st.text_input("Paste your message here:", placeholder="Enter a message to check...")

if st.button("Check message", type="primary"):
    if incoming_sms.strip():
        with st.spinner("Analyzing message..."):
            label, confidence, advice = check_spam(incoming_sms, st.session_state.token)
            st.session_state.history.append((incoming_sms, label, confidence, advice))
        st.rerun()
    else:
        st.warning("Please enter a message!")

# Show message history as a conversation
if st.session_state.history:
    st.subheader(f"Message History ({len(st.session_state.history)})")
    
    for i, (msg, label, confidence, adv) in enumerate(reversed(st.session_state.history), 1):
        # User message (right-aligned)
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-end; margin-bottom: 10px;'>
            <div style='background-color: #007AFF; color: white; padding: 10px 15px; border-radius: 18px; max-width: 70%; word-wrap: break-word;'>
                {msg}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bot response (left-aligned)
        color = "#FF3B30" if label.lower() == "spam" else "#34C759"
        icon = "🚨" if label.lower() == "spam" else "✅"
        
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-start; margin-bottom: 10px;'>
            <div style='background-color: #E5E5EA; color: black; padding: 10px 15px; border-radius: 18px; max-width: 70%; word-wrap: break-word;'>
                <strong style='color: {color};'>{icon} {label}</strong><br/>
                Prediction confidence: {confidence:.1f}%<br/>
                <em>{adv}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
else:
    st.info("No messages checked yet. Start by entering an SMS above!")

# Sidebar for info
with st.sidebar:
    st.subheader("About")
    st.write("""
    This app uses **Nyckel's SMS Spam Identifier** to detect spam messages with AI.
    
    - **Spam Detection**: Identifies unwanted promotional and scam messages
    - **Confidence Score**: Shows how certain the AI is about its classification
    - **Message History**: Keeps track of all checked messages
    """)
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
