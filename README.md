📉 Telecom Customer Churn Analysis & Prediction
An end-to-end data analytics project that uses SQL Server, Power BI and Python (Random Forest) to find out why telecom customers leave, and which new customers are most at risk of leaving. The prediction model is deployed as a Streamlit web app.
🔗 Live App: `https://YOUR-APP-NAME.streamlit.app`  (replace with your Streamlit link)
---
📌 Table of Contents
Project Overview
Problem Statement
Objectives
Tools & Technologies
Project Architecture
Dataset
Step 1: ETL in SQL Server
Step 2: Transformation in Power BI
Step 3: Power BI Measures
Step 4: Dashboard
Step 5: Churn Prediction with Python
Step 6: Deployment with Streamlit
Key Findings
Business Recommendations
Limitations & Next Steps
Repository Structure
How to Run Locally
Acknowledgements
Author
---
📖 Project Overview
Customer churn is the percentage of customers who stop using a company's service. Winning a new customer costs more than keeping an existing one, so telecom companies need to know who is leaving, why, and who will leave next.
This project covers the full data lifecycle:
cleaning raw customer data in SQL Server
analysing churn patterns in a Power BI report
training a Random Forest model in Python
serving predictions through a Streamlit app
The same approach can be applied to banking, retail, subscription services and healthcare platforms.
❓ Problem Statement
Telecom companies lose revenue every time a customer leaves. The business needs answers to three questions:
Which customers are leaving?
Why are they leaving?
Which new customers are likely to leave next, so the company can act before it happens?
🎯 Objectives
Build an ETL pipeline in SQL Server (staging table → production table → views)
Clean the data and handle null values
Analyse churn by demographics, geography, payment and account details, and services used
Study churner profiles to support targeted marketing campaigns
Predict future churners with a machine learning model
Make the model usable through a deployed web app
🛠️ Tools & Technologies
Tool	Used for
SQL Server (SSMS)	Data storage, ETL pipeline, views
Power BI (Power Query, DAX)	Transformations, measures, interactive report
Python (pandas, NumPy, scikit-learn, matplotlib, seaborn, joblib)	Preprocessing, Random Forest model, evaluation
Streamlit	Web app for single and batch predictions
GitHub + Streamlit Community Cloud	Code hosting and free deployment
🏗️ Project Architecture
```
Raw CSV Dataset
      ↓
SQL Server  (stg_Churn → prod_Churn → vw_ChurnData / vw_JoinData)
      ↓
Power BI Report  (churn analysis + prediction pages)
      ↓
Python Random Forest  (train on Stayed/Churned, predict on Joined)
      ↓
Streamlit App  (single customer + batch prediction)
```
🗂️ Dataset
Existing customers (Stayed / Churned): about 6,000 customers, used to train and test the model
New joiners (Joined): 411 customers, used for prediction
Total in the report: 6,418 customers
Attributes: demographics (gender, age, marital status, state), services (phone, internet, streaming, security), contract and billing (contract type, payment method, monthly charge, total charges, refunds, revenue), `Customer_Status`, `Churn_Category` and `Churn_Reason`
---
Step 1: ETL in SQL Server
1. Create the database and load the data
```sql
CREATE DATABASE db_Churn;
```
The CSV was imported into a staging table (`stg_Churn`) with the Import Wizard. `Customer_ID` is the primary key, nulls were allowed to avoid load errors, and `BIT` columns were changed to `VARCHAR(50)`.
2. Explore the data
Distribution queries were run for gender, contract type, revenue by customer status and customers by state.
```sql
SELECT Contract,
       COUNT(Contract) AS TotalCount,
       COUNT(Contract) * 1.0 / (SELECT COUNT(*) FROM stg_Churn) AS Percentage
FROM stg_Churn
GROUP BY Contract;
```
3. Check for nulls
A `SUM(CASE WHEN column IS NULL THEN 1 ELSE 0 END)` query counts the nulls in every column.
4. Clean the data into a production table
Nulls are replaced with meaningful defaults using `ISNULL`:
Column type	Replaced with	Why
`Value_Deal`, `Internet_Type`	`'None'`	Customer has no deal or no internet
Service columns (`Multiple_Lines`, `Streaming_TV`, ...)	`'No'`	Service is not used
`Churn_Category`, `Churn_Reason`	`'Others'`	Customer did not churn
```sql
SELECT Customer_ID, Gender, Age,
       ISNULL(Value_Deal, 'None') AS Value_Deal,
       ISNULL(Multiple_Lines, 'No') AS Multiple_Lines
       -- ... remaining columns
INTO db_Churn.dbo.prod_Churn
FROM db_Churn.dbo.stg_Churn;
```
5. Create views
```sql
CREATE VIEW vw_ChurnData AS
SELECT * FROM prod_Churn WHERE Customer_Status IN ('Churned', 'Stayed');

CREATE VIEW vw_JoinData AS
SELECT * FROM prod_Churn WHERE Customer_Status = 'Joined';
```
`vw_ChurnData`: customers with a known outcome, used for analysis and model training
`vw_JoinData`: new customers with no outcome yet, used for prediction
> **Why two tables?** The staging table keeps the raw data untouched. The production table holds the cleaned data used for analysis, so the pipeline can be rebuilt safely.
Full script: `Sql Code.sql`
Step 2: Transformation in Power BI
Calculated columns and tables created in Power Query:
Item	Logic
Churn Status	1 if `Customer_Status = "Churned"`, else 0
Monthly Charge Range	< 20, 20-50, 50-100, > 100
Age Group	< 20, 20-35, 36-50, > 50 (with a sorting column)
Tenure Group	< 6, 6-12, 12-18, 18-24, ≥ 24 months (with a sorting column)
Services table	Service columns unpivoted into Services and Status columns
```dax
Age_Group =
SWITCH(
    TRUE(),
    prod_Churn[Age] < 20, "< 20",
    prod_Churn[Age] <= 35, "20-35",
    prod_Churn[Age] <= 50, "36-50",
    "> 50"
)
```
Step 3: Power BI Measures
```dax
Total_Customer = COUNT(prod_Churn[Customer_ID])

New Joiners =
CALCULATE(
    COUNT(prod_Churn[Customer_ID]),
    prod_Churn[Customer_Status] = "Joined"
)

Total Churn = SUM(prod_Churn[Churn_Status])

Churn Rate = DIVIDE([Total Churn], [Total_Customer])
```
`Churn Rate` is formatted as a percentage (27%). `DIVIDE` is used instead of `/` to avoid division-by-zero errors.
Step 4: Power BI Dashboard
The report has three pages: Home, Churn Analysis and Churn Prediction.
Headline KPIs: 6,418 customers · 1,732 churned · 411 new joiners · 27% churn rate
Churn Analysis page
Demographic: age group, gender
Account: contract, payment method, tenure group
Geographic: top states by churn rate
Churn distribution: churn category and reason
Services: internet type and service usage
Churn Prediction page
Predicted churners by age group, marital status, tenure group, contract and state
A customer list with monthly charge, revenue, refunds and referrals
Dashboard Preview
<img width="1206" height="737" alt="Home page" src="https://github.com/user-attachments/assets/73c25190-08a6-4325-a8af-fb7e5e96b6e0" />
<img width="1278" height="746" alt="Churn analysis page" src="https://github.com/user-attachments/assets/b0c6ed4f-fcaf-4e73-990d-2841a9f06004" />
<img width="1201" height="731" alt="Churn prediction page" src="https://github.com/user-attachments/assets/4fc8b1d6-168c-49dc-9d17-11ef96d7c815" />
---
Step 5: Churn Prediction with Python
Algorithm: Random Forest Classifier (100 trees)
Why Random Forest?
Works well with a mix of numeric and categorical features
Captures non-linear patterns
Reduces overfitting by combining many decision trees
Provides feature importance
Process
Load `vw_ChurnData` (Stayed and Churned customers)
Drop `Customer_ID`, `Churn_Category` and `Churn_Reason` (the last two are only known after a customer leaves, so they would leak the answer)
Label-encode the categorical columns
Split 80% training and 20% testing
Train the model and evaluate it
Apply the model to `vw_JoinData` (new joiners) and export the predicted churners
Model performance (20% test set, 1,202 customers)
Metric	Result
Accuracy	84%
Precision (churn)	78%
Recall (churn)	65%
F1-score (churn)	71%
```
Confusion Matrix
                  Predicted Stayed   Predicted Churned
Actual Stayed            783                 64
Actual Churned           126                229
```
Accuracy alone can mislead because about 70% of customers stayed, so precision and recall for the churn class matter more. Recall of 65% means the model catches about 2 out of 3 real churners.
Prediction result: the model flagged 378 of 411 new joiners as likely churners (see Limitations).
Code: `Prediction Code.ipynb` and `train_model.py`
---
Step 6: Deployment with Streamlit
The trained model is saved with `joblib` and served by a Streamlit app (`app.py`).
App features
Tab	What it does
🔍 Single customer	Fill in a customer's details and get a churn probability, a risk level and a suggested retention action
📂 Batch prediction	Upload a CSV or Excel file of new customers, get them ranked by churn risk, and download the results
📊 About the model	Accuracy, precision, recall and the top feature importances
Risk levels: High = 60% or more · Medium = 30% to 60% · Low = below 30%
`Total_Revenue` is calculated automatically in the app as Total Charges − Refunds + Extra Data Charges + Long Distance Charges, which matches the dataset exactly.
How to deploy (free)
Train and save the model (only needed if you change the data or code):
```bash
   python train_model.py
   ```
This creates `churn_model.joblib`.
Push these files to a GitHub repository: `app.py`, `churn_model.joblib`, `requirements.txt`, `train_model.py`
Go to share.streamlit.io and sign in with GitHub.
Click Create app → Deploy a public app from GitHub.
Select the repository, the `main` branch and set the main file path to `app.py`.
Click Deploy. After a few minutes the app is live at a public link.
Add the link to the top of this README.
> **Tip:** if deployment shows a scikit-learn version error, run `python train_model.py` again with the same version listed in `requirements.txt` and upload the new `churn_model.joblib`.
---
🔍 Key Findings
Overall churn rate is 27%: 1,732 of 6,418 customers churned.
Contract type is the strongest driver. Month-to-month customers churn at 47%, one-year at 11% and two-year at only 3%.
Competitors are the top reason for leaving. 761 of the 1,732 churners (about 44%) left for a competitor.
Fiber Optic customers are most likely to leave (41% churn rate, against 19% for DSL). This may point to a price or service-quality issue.
Payment method matters. Mailed Check (38%) and Bank Withdrawal (34%) customers churn far more than Credit Card customers (15%).
Older customers and some regions churn more. Customers over 50 have the highest churn rate (31%), and Jammu & Kashmir has the highest state churn rate (57%).
Tenure is not a strong driver here. Churn stays around 26% to 27.5% across tenure groups.
> Churn *rate* shows how risky a group is. It is not the same as the *number* of churners, which depends on the group's size.
💡 Business Recommendations
Encourage long-term contracts with discounts or loyalty rewards for month-to-month customers
Review Fiber Optic pricing and service quality
Nudge Mailed Check and Bank Withdrawal customers towards card or auto-pay with incentives
Offer bundled service packages to customers using few services
Target high-risk customers from the prediction list with personalised retention campaigns
Study competitor offers, since they are the most common reason for leaving
⚠️ Limitations & Next Steps
The model flags a very high share of new joiners (378 of 411, about 92%). Historical churn is only around 27%. The model uses cumulative fields such as `Total_Charges` and `Total_Revenue`, which are naturally low for new customers and resemble past churners. Next step: retrain using only features known at signup, and rank customers by churn probability instead of a yes/no label (the app already shows probabilities).
Recall for churners is 65%. About 1 in 3 churners is missed. Options: class weights, a lower decision threshold, hyperparameter tuning and comparing other models.
Only one model was trained (Random Forest with default settings). Next: compare with Logistic Regression and XGBoost using recall, F1 and ROC-AUC with cross-validation.
Label encoding is fine for tree models but should be replaced with one-hot encoding for linear models.
Possible leakage: cumulative revenue and charge fields should be reviewed.
📁 Repository Structure
```
├── Churn Analysis.pbix       # Power BI report
├── Sql Code.sql              # ETL, cleaning and views
├── Prediction Code.ipynb     # Model training and prediction notebook
├── train_model.py            # Trains the model and saves churn_model.joblib
├── app.py                    # Streamlit web app
├── churn_model.joblib        # Saved model, encoders and column order
├── churn_data.xlsx           # Training data (Stayed / Churned)
├── requirements.txt          # Python libraries for the app
└── README.md
```
▶️ How to Run Locally
```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME

# 2. Install the libraries
pip install -r requirements.txt

# 3. (Optional) retrain the model
python train_model.py

# 4. Start the app
streamlit run app.py
```
🙏 Acknowledgements
This project follows the structure of the PivotalStats "End-to-End Churn Analysis" portfolio tutorial for the SQL ETL, Power BI and Random Forest workflow. The Streamlit deployment, churn-probability risk levels, batch scoring and the findings and limitations sections are my own additions.
👨‍💻 Author
Arpit Kumar
B.Tech Computer Science & Engineering, Lovely Professional University
