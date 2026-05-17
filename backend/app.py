import streamlit as st
import streamlit.components.v1 as components
import joblib
import re
import os

st.set_page_config(page_title="PhishGuard", layout="wide")

try:
    with open("backend/style.css", "r") as f:
        css_content = f.read()
    with open("backend/index.html", "r") as f:
        html_content = f.read()
    
    full_code = f"<style>{css_content}</style>{html_content}"
    components.html(full_code, height=600, scrolling=True)

except FileNotFoundError:
    st.error("Make sure index.html and style.css are in the 'backend' folder!")

try:
    model = joblib.load("backend/model.pkl")
except Exception as e:
    st.warning("Model file not found. Please check the path.")

def extract_features(url):
    features = []
    features.append(len(url))
    features.append(1 if "http://" in url else 0)
    features.append(1 if "@" in url else 0)
    
    ip_pattern = r"\d+\.\d+\.\d+\.\d+"
    features.append(1 if re.search(ip_pattern, url) else 0)
    
    keywords = ["login", "verify", "bank", "secure", "update", "free"]
    for word in keywords:
        features.append(1 if word in url.lower() else 0)
    
    return [features]

url_input = st.text_input("Enter URL to analyze:")
if st.button("Analyze"):
    if url_input:
        data = extract_features(url_input)
        prediction = model.predict(data)
        
        if prediction[0] == 1:
            st.error("⚠️ Warning: This looks like a Phishing URL!")
        else:
            st.success("✅ This URL appears to be safe.")
