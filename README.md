# 🛡️ Cindy the Cyber Companion

A conversational AI app that detects SMS spam — built to help everyday people spot scams before it's too late.

**[▶️ Try it live](https://edumzansi.streamlit.app/)**

## What it does
Paste any suspicious message and Cindy will tell you if it's spam or safe, with a confidence score and actionable safety tips.

## Tech stack
- **Frontend** — Streamlit
- **Spam detection** — [Nyckel SMS Spam Identifier](https://www.nyckel.com) (ML API)
- **Auth** — OAuth2 client credentials
- **Deployment** — Streamlit Cloud

## Run locally
1. Clone the repo
2. Add your Nyckel credentials to `.streamlit/secrets.toml`:
```toml
   [nyckel]
   CLIENT_ID = "your-client-id"
   CLIENT_SECRET = "your-client-secret"
```
3. `pip install -r requirements.txt`
4. `streamlit run app.py`
