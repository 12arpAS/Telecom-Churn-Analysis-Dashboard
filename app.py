import joblib
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent  # works from the repo root or from a subfolder

st.set_page_config(page_title="Telecom Churn Predictor", page_icon="📉", layout="wide")


@st.cache_resource
def load_artifacts():
    return joblib.load(BASE_DIR / "churn_model.joblib")


art = load_artifacts()
model, encoders, feature_order = art["model"], art["encoders"], art["feature_order"]

DROP_COLS = ["Customer_ID", "Customer_Status", "Churn_Category", "Churn_Reason",
             "Customer_Status_Predicted", "Churn_Probability", "Risk_Level"]


def risk_level(p):
    return "High" if p >= 0.6 else "Medium" if p >= 0.3 else "Low"


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Same preprocessing as training: drop extra columns, label-encode, fix column order."""
    X = df.drop(columns=[c for c in DROP_COLS if c in df.columns]).copy()
    for col, enc in encoders.items():
        X[col] = X[col].astype(str).str.strip()
        unknown = set(X[col]) - set(enc.classes_)
        if unknown:
            raise ValueError(f"Column '{col}' has unseen values: {sorted(unknown)}. "
                             f"Allowed: {list(enc.classes_)}")
        X[col] = enc.transform(X[col])
    return X[feature_order]


st.title("📉 Telecom Customer Churn Predictor")
st.caption("Random Forest model trained on past Stayed / Churned customers. "
           "Predict one customer, or upload a file of new customers.")

tab1, tab2, tab3 = st.tabs(["🔍 Single customer", "📂 Batch prediction", "📊 About the model"])

# ---------------------------------------------------------------- Tab 1
with tab1:
    opts = lambda c: list(encoders[c].classes_)
    with st.form("single"):
        st.subheader("Customer profile")
        c1, c2, c3, c4 = st.columns(4)
        gender = c1.selectbox("Gender", opts("Gender"))
        age = c2.number_input("Age", 18, 100, 35)
        married = c3.selectbox("Married", opts("Married"))
        state = c4.selectbox("State", opts("State"))

        c1, c2, c3 = st.columns(3)
        referrals = c1.number_input("Number of referrals", 0, 20, 0)
        tenure = c2.number_input("Tenure (months)", 0, 100, 12)
        deal = c3.selectbox("Value deal", opts("Value_Deal"))

        st.subheader("Services")
        c1, c2, c3, c4 = st.columns(4)
        phone = c1.selectbox("Phone service", opts("Phone_Service"))
        lines = c2.selectbox("Multiple lines", opts("Multiple_Lines"))
        internet = c3.selectbox("Internet service", opts("Internet_Service"))
        itype = c4.selectbox("Internet type", opts("Internet_Type"))

        c1, c2, c3, c4 = st.columns(4)
        security = c1.selectbox("Online security", opts("Online_Security"))
        backup = c2.selectbox("Online backup", opts("Online_Backup"))
        protect = c3.selectbox("Device protection", opts("Device_Protection_Plan"))
        support = c4.selectbox("Premium support", opts("Premium_Support"))

        c1, c2, c3, c4 = st.columns(4)
        tv = c1.selectbox("Streaming TV", opts("Streaming_TV"))
        movies = c2.selectbox("Streaming movies", opts("Streaming_Movies"))
        music = c3.selectbox("Streaming music", opts("Streaming_Music"))
        unlimited = c4.selectbox("Unlimited data", opts("Unlimited_Data"))

        st.subheader("Contract and billing")
        c1, c2, c3 = st.columns(3)
        contract = c1.selectbox("Contract", opts("Contract"))
        paperless = c2.selectbox("Paperless billing", opts("Paperless_Billing"))
        payment = c3.selectbox("Payment method", opts("Payment_Method"))

        c1, c2, c3, c4, c5 = st.columns(5)
        monthly = c1.number_input("Monthly charge", 0.0, 500.0, 70.0)
        total_ch = c2.number_input("Total charges", 0.0, 20000.0, 800.0)
        refunds = c3.number_input("Total refunds", 0.0, 1000.0, 0.0)
        extra = c4.number_input("Extra data charges", 0.0, 500.0, 0.0)
        ld = c5.number_input("Long distance charges", 0.0, 10000.0, 100.0)

        submitted = st.form_submit_button("Predict churn", type="primary")

    if submitted:
        # Total_Revenue = Total_Charges - Refunds + Extra Data + Long Distance (matches your data)
        total_rev = total_ch - refunds + extra + ld
        row = pd.DataFrame([{
            "Gender": gender, "Age": age, "Married": married, "State": state,
            "Number_of_Referrals": referrals, "Tenure_in_Months": tenure,
            "Value_Deal": deal, "Phone_Service": phone, "Multiple_Lines": lines,
            "Internet_Service": internet, "Internet_Type": itype,
            "Online_Security": security, "Online_Backup": backup,
            "Device_Protection_Plan": protect, "Premium_Support": support,
            "Streaming_TV": tv, "Streaming_Movies": movies, "Streaming_Music": music,
            "Unlimited_Data": unlimited, "Contract": contract,
            "Paperless_Billing": paperless, "Payment_Method": payment,
            "Monthly_Charge": monthly, "Total_Charges": total_ch,
            "Total_Refunds": refunds, "Total_Extra_Data_Charges": extra,
            "Total_Long_Distance_Charges": ld, "Total_Revenue": total_rev,
        }])
        prob = float(model.predict_proba(prepare(row))[0, 1])
        level = risk_level(prob)

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Churn probability", f"{prob:.0%}")
        m2.metric("Risk level", level)
        m3.metric("Prediction", "Likely to churn" if prob >= 0.5 else "Likely to stay")
        st.progress(prob)

        if level == "High":
            st.error("High risk. Suggested action: offer a long-term contract discount "
                     "or a loyalty reward and have the retention team call this customer.")
        elif level == "Medium":
            st.warning("Medium risk. Suggested action: send a personalised offer or "
                       "a service check-in.")
        else:
            st.success("Low risk. Keep the customer happy with normal service.")

# ---------------------------------------------------------------- Tab 2
with tab2:
    st.subheader("Upload new customers (CSV or Excel)")
    st.write("Use the same columns as your `join datas.xlsx` file. "
             "`Customer_ID`, `Customer_Status`, `Churn_Category` and `Churn_Reason` "
             "are ignored if present.")
    up = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    if up is not None:
        try:
            # keep_default_na=False keeps the text "None" as a category
            df = (pd.read_csv(up, keep_default_na=False) if up.name.endswith(".csv")
                  else pd.read_excel(up, keep_default_na=False))
            probs = model.predict_proba(prepare(df))[:, 1]
            out = df.copy()
            out["Churn_Probability"] = probs.round(3)
            out["Customer_Status_Predicted"] = (probs >= 0.5).astype(int)
            out["Risk_Level"] = [risk_level(p) for p in probs]
            out = out.sort_values("Churn_Probability", ascending=False)

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Customers scored", len(out))
            k2.metric("Predicted churners", int(out["Customer_Status_Predicted"].sum()))
            k3.metric("High risk", int((out["Risk_Level"] == "High").sum()))
            k4.metric("Avg churn probability", f"{probs.mean():.0%}")

            st.write("Customers ranked by churn risk:")
            st.dataframe(out, use_container_width=True, height=400)
            st.download_button("Download predictions (CSV)",
                               out.to_csv(index=False).encode(),
                               "Churn_Predictions.csv", "text/csv")
        except Exception as e:
            st.error(f"Could not score the file: {e}")

# ---------------------------------------------------------------- Tab 3
with tab3:
    st.subheader("Model facts")
    st.write("- **Algorithm:** Random Forest (100 trees), 80/20 train-test split")
    st.write("- **Test accuracy:** 84%  |  **Precision (churn):** 78%  |  **Recall (churn):** 65%")
    st.write("- **Risk levels:** High is 60% or more, Medium is 30% to 60%, Low is below 30%")
    imp = (pd.Series(art["importances"]).sort_values(ascending=False).head(10))
    st.write("**Top 10 features by importance**")
    st.bar_chart(imp)
    st.info("Limitation: the model uses cumulative fields such as Total Charges and "
            "Total Revenue, which are naturally low for brand-new customers, so it "
            "can over-flag new joiners. Use the probability ranking, not only the yes/no label.")
