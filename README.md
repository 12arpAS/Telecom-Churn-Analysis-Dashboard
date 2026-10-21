# Telecom Customer Churn Predictor

Streamlit app that predicts churn using a Random Forest trained on past customers.

**Pipeline:** SQL Server (ETL) -> Power BI (analysis) -> Python Random Forest -> Streamlit app

## Run locally
```
pip install -r requirements.txt
python train_model.py      # trains and saves churn_model.joblib
streamlit run app.py
```

## Features
- Single customer prediction with churn probability and risk level
- Batch upload (CSV/Excel) with ranked risk list and CSV download
- Model facts and feature importance

## Model
Random Forest (100 trees), 80/20 split: accuracy 84%, churn precision 78%, churn recall 65%.
