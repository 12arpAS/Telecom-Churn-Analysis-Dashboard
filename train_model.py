"""
Step 1: Train the Random Forest and save everything the app needs.
Run once:  python train_model.py
"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

DATA_PATH = "data/churn_data.xlsx"

# keep_default_na=False keeps the text "None" (e.g. Internet_Type = None) as a real category
data = pd.read_excel(DATA_PATH, keep_default_na=False)

# Drop columns not used for prediction (same as your notebook)
data = data.drop(["Customer_ID", "Churn_Category", "Churn_Reason"], axis=1)

columns_to_encode = [
    "Gender", "Married", "State", "Value_Deal", "Phone_Service", "Multiple_Lines",
    "Internet_Service", "Internet_Type", "Online_Security", "Online_Backup",
    "Device_Protection_Plan", "Premium_Support", "Streaming_TV", "Streaming_Movies",
    "Streaming_Music", "Unlimited_Data", "Contract", "Paperless_Billing",
    "Payment_Method",
]

label_encoders = {}
for col in columns_to_encode:
    label_encoders[col] = LabelEncoder()
    data[col] = label_encoders[col].fit_transform(data[col])

data["Customer_Status"] = data["Customer_Status"].map({"Stayed": 0, "Churned": 1})

X = data.drop("Customer_Status", axis=1)
y = data["Customer_Status"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model + encoders + column order (compress keeps the file small for GitHub)
joblib.dump(
    {
        "model": rf_model,
        "encoders": label_encoders,
        "feature_order": list(X.columns),
        "importances": dict(zip(X.columns, rf_model.feature_importances_)),
    },
    "churn_model.joblib",
    compress=3,
)
print("Saved churn_model.joblib")
