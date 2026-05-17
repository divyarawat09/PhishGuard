import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data={
"url_length":[20,120,80,15,90,130],
"http":[0,1,1,0,1,1],
"at":[0,1,0,0,1,1],
"ip":[0,1,0,0,1,1],
"keywords":[0,3,2,0,4,5],
"label":[0,2,1,0,2,2]
}

df=pd.DataFrame(data)

X=df.drop("label",axis=1)

y=df["label"]

model=RandomForestClassifier()

model.fit(X,y)

joblib.dump(model,"model.pkl")

print("Model Trained")