import streamlit as st
import streamlit.components.v1 as components
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("index.html") as f:
    html_content = f.read()
    components.html(html_content, height=800)


model = joblib.load("model.pkl")

def extract_features(url):

    features = []

    features.append(len(url))
    features.append(1 if "http://" in url else 0)
    features.append(1 if "@" in url else 0)
    features.append(1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0)

    keywords = ["login", "verify", "bank", "secure", "update", "free"]

    score = sum(word in url.lower() for word in keywords)

    features.append(score)

    return features

st.set_page_config(page_title="PhishGuard", page_icon="🔐")

st.title("🔐 PhishGuard AI Phishing Detector")
st.write("Enter a URL below to check if it's safe or dangerous")

url = st.text_input("Enter Website URL")

if st.button("Analyze"):

    if url == "":
        st.warning("Please enter a URL")
    else:

        features = [extract_features(url)]
        prediction = model.predict(features)[0]

        if prediction == 0:
            st.success("SAFE WEBSITE ✅")

        elif prediction == 1:
            st.warning("SUSPICIOUS WEBSITE ⚠️")

        else:
            st.error("DANGEROUS WEBSITE ❌")
