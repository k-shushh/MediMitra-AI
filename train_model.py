import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report

print("Loading dataset...")

df_train = pd.read_csv("extracted_dataset\Training.csv")
df_test  = pd.read_csv("extracted_dataset\Testing.csv")

def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace(".", "_", regex=False)
    )
    return df

df_train = clean_columns(df_train)
df_test  = clean_columns(df_test)

print("Train shape:", df_train.shape)
print("Test shape:",  df_test.shape)
print("Unique diseases:", df_train["prognosis"].nunique())

X_train    = df_train.drop("prognosis", axis=1)
y_train_raw = df_train["prognosis"]

X_test     = df_test.drop("prognosis", axis=1)
y_test_raw  = df_test["prognosis"]

symptom_columns = X_train.columns.tolist()
print(f"Total symptoms: {len(symptom_columns)}")

le = LabelEncoder()
y_train = le.fit_transform(y_train_raw)
y_test  = le.transform(y_test_raw)

print("Training model...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred, average="macro")

print(f"\nMacro F1 Score: {round(f1, 4)}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0))

os.makedirs("model", exist_ok=True)

joblib.dump(model,           "model/disease_model.pkl")
joblib.dump(le,              "model/label_encoder.pkl")
joblib.dump(symptom_columns, "model/symptom_columns.pkl")  

print("\nModel and encoders saved successfully.")
print("Saved symptoms:", symptom_columns[:5], "...")