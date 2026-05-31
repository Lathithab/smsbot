import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NYCKEL_TOKEN_URL = "https://www.nyckel.com/connect/token"
NYCKEL_API_URL = "https://www.nyckel.com/v1/functions/sms-spam-identifier/invoke"

import streamlit as st

CLIENT_ID = st.secrets["nyckel"]["CLIENT_ID"]
CLIENT_SECRET = st.secrets["nyckel"]["CLIENT_SECRET"]


def get_nyckel_token() -> str | None:
    """Fetch OAuth token from Nyckel."""
    try:
        result = requests.post(
            NYCKEL_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            timeout=10,
        )
        result.raise_for_status()
        return result.json().get("access_token")
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch Nyckel token: %s", e)
        return None


def check_spam(message: str, access_token: str) -> tuple[str, float, str]:
    """Classify a message as spam or ham using Nyckel's SMS Spam Identifier."""
    try:
        result = requests.post(
            NYCKEL_API_URL,
            json={"data": message},
            headers={
                "accessToken": access_token,
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        result.raise_for_status()

        response = result.json()
        label = response.get("labelName", "unknown").lower()
        confidence = response.get("confidence", 0) * 100

        return label, confidence, _build_advice(label, confidence)

    except requests.exceptions.Timeout:
        return "error", 0, "⚠️ Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        logger.error("Nyckel API error: %s", e)
        return "error", 0, "⚠️ Could not reach the spam detection service. Please try again."


def _build_advice(label: str, confidence: float) -> str:
    if label == "spam":
        return (
            "💡 **Safety tips:**\n"
            "- 🚫 Don't click any links or download attachments\n"
            "- 🔒 Never share personal info or OTP codes\n"
            "- 📞 If it's from a known contact, confirm through another channel\n"
            "- ⚠️ Mark the message as spam in your messaging app\n"
            "- 🌐 Google the company or offer to verify legitimacy\n"
            "- 🧐 Watch for spelling mistakes or suspicious URLs"
        )
    elif label == "ham":
        return (
            "💡 **Stay cautious:**\n"
            "- 🧐 Double-check links before clicking\n"
            "- 🔒 Avoid sharing sensitive info if something feels off\n"
            "- ⚠️ Watch for grammar mistakes or weird sender addresses\n"
            "- 🌐 If in doubt, verify through official sources"
        )
    else:
        return "⚠️ Could not determine the message type. Please try again."