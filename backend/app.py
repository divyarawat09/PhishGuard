from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
from pathlib import Path

try:
    from backend.feature_engineering import build_feature_frame
except ModuleNotFoundError:
    from feature_engineering import build_feature_frame

app = Flask(__name__)
CORS(app)

MODEL_PATH = Path(__file__).with_name("model.pkl")
model = joblib.load(MODEL_PATH)

LABEL_MAP = {
    0: "Safe",
    1: "Suspicious",
    2: "Dangerous",
}


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True) or {}
    url = (payload.get("url") or "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    features_df = build_feature_frame([url])
    prediction = int(model.predict(features_df)[0])
    probabilities = model.predict_proba(features_df)[0]
    confidence = float(max(probabilities))

    return jsonify(
        {
            "result": LABEL_MAP.get(prediction, "Suspicious"),
            "confidence": round(confidence, 4),
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
