from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

try:
    from backend.feature_engineering import FEATURE_COLUMNS, build_feature_frame
except ModuleNotFoundError:
    from feature_engineering import FEATURE_COLUMNS, build_feature_frame

BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw_urls.csv"
MODEL_PATH = BASE_DIR / "model.pkl"
METRICS_PATH = BASE_DIR / "model_metrics.txt"


def main() -> None:
    df = pd.read_csv(RAW_DATA_PATH)

    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'url' and 'label' columns")

    X = build_feature_frame(df["url"].astype(str).tolist())
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=16,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, digits=4)

    joblib.dump(model, MODEL_PATH)

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        f.write(f"Rows: {len(df)}\n")
        f.write(f"Features: {', '.join(FEATURE_COLUMNS)}\n")
        f.write(f"Test accuracy: {acc:.4f}\n\n")
        f.write("Classification report:\n")
        f.write(report)

    print(f"Model trained and saved to {MODEL_PATH}")
    print(f"Metrics saved to {METRICS_PATH}")


if __name__ == "__main__":
    main()
