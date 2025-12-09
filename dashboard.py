import streamlit as st
import requests

st.set_page_config(
    page_title="PhishGuard Dashboard",
    layout="wide",
)

URL_API = "http://127.0.0.1:8000/check"
EMAIL_API = "http://127.0.0.1:8001/check_text"

st.title("🛡️ PhishGuard – Real-Time AI/ML Phishing Detection System")

tab_url, tab_email = st.tabs(["🌐 URL Scanner", "📧 Email/Text Scanner"])


# ==============================================================
#                     URL SCANNER
# ==============================================================
with tab_url:
    st.subheader("🔍 URL Scanner")

    url = st.text_input("Enter website URL:")

    if st.button("Scan URL"):
        try:
            res = requests.post(URL_API, json={"url": url}).json()
            final = res["final"]["final"]

            st.write("### 🔬 Final Result")

            if final == "SAFE":
                st.success("🟢 SAFE WEBSITE")
            else:
                st.error("🔴 PHISHING DETECTED – BLOCK IMMEDIATELY")

            st.write("### Engine-Wise Results")
            st.json(res["results"])

        except Exception as e:
            st.error("❌ URL API Offline")
            st.error(str(e))


# ==============================================================
#                   EMAIL / TEXT SCANNER
# ==============================================================
with tab_email:
    st.subheader("📧 Email / SMS / Text Scanner")

    text = st.text_area(
        "Paste suspicious email / sms / message body:",
        height=220
    )

    if st.button("Scan Text"):
        try:
            res = requests.post(EMAIL_API, json={"text": text}).json()

            final = res["final"]
            votes = res["votes"]

            st.write("### 🔬 Final Result")

            if final == "safe":
                st.success(f"🟢 SAFE (Votes for phishing: {votes})")
            else:
                st.error(f"🔴 PHISHING DETECTED (Votes: {votes}/4)")

            st.write("### 🧠 Engine Breakdown")
            st.json({
                "BERT Model": res["bert"],
                "Text Moderation API": res["textmod"],
                "Email Verification API": res["email_verify"],
                "Risk API": res["risk"],
            })

        except Exception as e:
            st.error("❌ Email/Text API Offline")
            st.error(str(e))