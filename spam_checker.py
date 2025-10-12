import requests
import streamlit as st

# -----------------------------
# Nyckel Credentials
# -----------------------------
CLIENT_ID = st.secrets["nyckel"]["CLIENT_ID"]
CLIENT_SECRET = st.secrets["nyckel"]["CLIENT_SECRET"]

# Get authentication token
def get_nyckel_token():
    """Fetch OAuth token from Nyckel"""
    token_url = 'https://www.nyckel.com/connect/token'
    credentials = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    try:
        result = requests.post(token_url, data=credentials)
        print(f"Status Code: {result.status_code}")
        print(f"Response: {result.text}")
        result.raise_for_status()
        token_data = result.json()
        return token_data.get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Error getting token: {e}")
        print(f"Status Code: {result.status_code}")
        print(f"Response Body: {result.text}")
        return None


def check_spam(message: str, access_token: str):
    """
    Uses Nyckel SMS Spam Identifier to classify a message.
    
    Args:
        message: The message to check
        access_token: Nyckel API access token
    
    Returns:
        label: 'spam' or 'ham'
        confidence: confidence score as a percentage
        advice: user-friendly advice
    """
    try:
        # Nyckel API endpoint for SMS spam detection
        api_url = "https://www.nyckel.com/v1/functions/sms-spam-identifier/invoke"
        
        headers = {
            'accessToken': access_token,
            'Content-Type': 'application/json'
        }
        
        payload = {'data': message}
        
        result = requests.post(api_url, json=payload, headers=headers)
        result.raise_for_status()
        
        response = result.json()
        label = response.get("labelName", "unknown")
        confidence = response.get("confidence", 0) * 100  # convert to percentage

        # Generate advice based on label
 if label.lower() == "spam":
    advice = (
        f"⚠️ Heads up! This message looks like spam (I'm {confidence:.1f}% sure).\n\n"
        "💡 Tips:\n"
        "🚫 Don't click any links or download attachments.\n"
        "🔒 Never share personal info or OTP codes.\n"
        "📞 If it's from a known contact, confirm through another channel.\n"
        "⚠️ Mark the message as spam in your messaging app.\n"
        "🌐 Google the company, offer, or message content to verify legitimacy.\n"
        "🧐 Look for spelling mistakes or suspicious URLs."
    )
else:
    advice = (
        f"✅ This message seems safe (I'm {confidence:.1f}% sure).\n\n"
        "💡 Tips:\n"
        "🧐 Still double-check links before clicking.\n"
        "🔒 Avoid sharing sensitive info if something feels off.\n"
        "⚠️ Keep an eye out for grammar mistakes or weird sender addresses.\n"
        "🌐 If in doubt, ask a friend or verify through official sources."
    )
        return label, confidence, advice

    except Exception as e:
        return "error", 0, f"⚠️ Error checking message: {e}"


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # Get token first
    token = get_nyckel_token()
    
    if token:
        test_message = "Congratulations! You've won a free car! Click here to claim."
        label, confidence, advice = check_spam(test_message, token)
        
        print(f"Message: {test_message}")
        print(f"Label: {label}, Confidence: {confidence:.1f}%")
        print(f"Advice: {advice}")
    else:
        print("Failed to authenticate with Nyckel")
