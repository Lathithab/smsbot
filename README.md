🛡️ Cyber Companion Chatbot

Cyber Companion Chatbot is an AI-powered chatbot that detects potential spam messages in real time. Built with Streamlit for the frontend and Nyckel’s SMS Spam Identifier API for machine learning, this bot provides users with a confidence score and friendly advice on whether a message is safe or risky.

Features

Spam Detection: Quickly classifies SMS or text messages as spam or safe.

Confidence Score: Shows the likelihood that a message is spam.

Friendly Advice: Provides actionable guidance to keep users safe.

Chat-Style UI: Uses st.chat_input and st.chat_message for a modern, interactive interface.

Typing Animations & Emojis: Makes chatting with the bot feel natural and engaging.

Demo

You can deploy and try the bot live on Streamlit Cloud:
(https://edumzansi.streamlit.app/)



Installation (Local)

Clone the repository:

git clone https://github.com/Lathithab/smsbot.git
cd smsbot


Create a virtual environment and activate it:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Add your Nyckel credentials in spam_checker.py or use Streamlit secrets:

import streamlit as st
CLIENT_ID = st.secrets["NYCKEL_CLIENT_ID"]
CLIENT_SECRET = st.secrets["NYCKEL_CLIENT_SECRET"]


Run the app:

streamlit run app.py

How it Works

User types a message into the chat input.

The bot sends the message to Nyckel’s SMS Spam Identifier API.

The API returns a label (spam or ham) and a confidence score.

The bot displays the label, confidence, and advice with emojis and timestamp.

Tech Stack

Frontend: Streamlit

Spam Classification: Nyckel AI Functions

Python Libraries: requests, nyckel

Future Enhancements

Integrate with SMS gateways (Twilio, Africa’s Talking) to check real SMS messages.

Add Telegram / WhatsApp integration.

Store chat history and analytics in Firebase or Google Sheets.
