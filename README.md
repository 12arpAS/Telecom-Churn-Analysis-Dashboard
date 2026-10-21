# Telecom Customer Churn Analysis and Prediction

## 1. Introduction
In today’s competitive business environment, retaining customers is crucial for long-term success. Churn analysis is a key technique used to understand and reduce this customer attrition.  It involves examining customer data to identify patterns and reasons behind customer departures. By using advanced data analytics and machine learning, 
businesses can predict which customers are at risk of leaving and understand the factors driving their decisions.
This knowledge allows companies to take proactive steps to improve customer satisfaction and loyalty.
Customer retention is one of the most important factors affecting the growth and profitability of a telecommunications company. In a competitive market, customers may discontinue their services because of pricing, contract conditions, service quality, customer support, or changing needs.

**Telecom Customer Churn Analysis and Prediction** is an end-to-end data analytics project that combines SQL Server, Power BI, Python, and Machine Learning to understand customer behavior, analyze historical churn patterns, and identify customers who may be at risk of leaving.

The project follows a data-driven approach, beginning with data extraction and transformation in SQL Server, followed by interactive dashboard development in Power BI and predictive modeling using Python.

The ultimate goal is to transform raw customer data into meaningful business insights that can help improve customer retention and support better decision-making.

## 2. Abstract

Customer churn refers to the situation in which customers discontinue their relationship with a company. High churn can result in revenue loss, increased customer acquisition costs, and reduced business growth.

This project develops an end-to-end analytical solution for a telecommunications company. Microsoft SQL Server is used to store, explore, clean, and transform customer data through an ETL pipeline. Power BI is used to create interactive dashboards that analyze customer demographics, geographical distribution, account information, subscribed services, revenue, and churn behavior.

Python is used to build a Random Forest classification model that learns from historical customer records and predicts potential churn among newly joined customers. The model's performance is evaluated using a confusion matrix and classification report.

By integrating descriptive analytics, data visualization, and predictive analytics, the project demonstrates how organizations can understand past customer behavior and identify opportunities for proactive customer retention.

## 3. Problem Statement

Telecommunication companies manage large volumes of customer data, including demographic details, subscription information, payment methods, service usage, contract types, and revenue records.

However, raw data alone does not provide a clear understanding of why customers leave or which customer groups require attention.

The key problems addressed by this project are:

- Difficulty identifying customer groups with higher churn rates.
- Limited visibility into the relationship between churn, contract type, tenure, payment method, and services.
- Challenges in combining and preparing customer data for consistent analysis.
- Lack of a centralized, interactive dashboard for monitoring important business metrics.
- Difficulty identifying newly joined customers who may be at risk of future churn.

The project addresses these challenges by developing a structured ETL pipeline, an interactive Power BI reporting solution, and a machine learning model for churn prediction.

## 4. Project Objectives

The primary objectives of this project are:

1. **Data extraction and transformation:** Import raw telecom customer data into SQL Server and prepare it for analysis.
2. **Data quality management:** Examine missing values, distinct categories, and data consistency before loading the cleaned records into the production table.
3. **Customer segmentation:** Analyze churn across demographic, geographic, account, payment, and service-related dimensions.
4. **KPI development:** Calculate total customers, new joiners, total churn, and churn rate.
5. **Interactive visualization:** Develop Power BI dashboards that communicate customer behavior and churn patterns clearly.
6. **Predictive analytics:** Train a Random Forest model to classify customers as likely to stay or churn.
7. **Business decision support:** Identify actionable opportunities for customer retention and targeted marketing campaigns.

## 5. Tools and Technologies

| Technology | Purpose |
|---|---|
| Microsoft SQL Server | Database creation, data exploration, ETL, cleaning, and transformation |
| SQL | Queries, conditional logic, aggregations, null handling, and views |
| Power BI Desktop | Interactive dashboards, data modeling, visualizations, and DAX measures |
| Power Query | Data transformation, conditional columns, grouping, and unpivoting |
| DAX | KPI calculations and analytical measures |
| Python | Data preparation, exploratory analysis, and churn prediction |
| Pandas and NumPy | Data manipulation and numerical operations |
| Scikit-learn | Data encoding, train-test splitting, Random Forest training, and evaluation |
| Matplotlib and Seaborn | Data visualization and feature-importance analysis |
| Jupyter Notebook | Developing and testing the machine learning workflow |
| Excel/CSV | Data exchange between the database, Python, and Power BI |

## 6. Project Architecture

The project follows an end-to-end analytics architecture that separates data preparation, reporting, and predictive modeling.

```text
             Raw Telecom Customer Dataset
                         |
                         v
                Microsoft SQL Server
                         |
                         v
                 Staging Table
                   stg_Churn
                         |
                         v
             Data Cleaning and ETL
                         |
                         v
                 Production Table
                   prod_Churn
                         |
                +--------+--------+
                |                 |
                v                 v
          SQL Data Views      Power BI Data
        vw_ChurnData         Transformation
        vw_JoinData                |
                |                  v
                v           Interactive Reports
          Python / ML        and KPI Dashboards
                |
                v
        Random Forest Model
                |
                v
        Predicted Churners
                |
                v
       Online Deployment 
```

### Architecture Explanation

- **Source layer:** Contains the original telecom customer dataset.
- **Staging layer:** Stores the imported data before production transformation.
- **Transformation layer:** Handles null values, standardizes categorical values, and prepares the production table.
- **Analytical layer:** SQL views provide filtered datasets for historical churn analysis and newly joined customers.
- **Visualization layer:** Power BI presents KPIs, customer segments, and churn patterns through interactive reports.
- **Prediction layer:** Python trains and evaluates the classification model and generates predictions for new customer records.
- **Reporting layer:** Predicted churn records can be loaded into Power BI for further analysis.

## 7. Dataset Description

The project uses a telecom customer dataset containing information about customer demographics, account characteristics, subscribed services, financial metrics, and customer status.

### Important Dataset Attributes

| Category | Example attributes |
|---|---|
| Customer demographics | Gender, Age, Married |
| Geography | State |
| Customer relationship | Tenure_in_Months, Number_of_Referrals |
| Services | Phone_Service, Internet_Service, Internet_Type |
| Additional services | Online_Security, Online_Backup, Streaming_TV, Streaming_Movies |
| Account information | Contract, Paperless_Billing, Payment_Method |
| Financial information | Monthly_Charge, Total_Charges, Total_Refunds, Total_Revenue |
| Customer outcome | Customer_Status, Churn_Category, Churn_Reason |

### Customer Status

The dataset distinguishes between three important customer statuses:

- **Stayed:** Customers who continued using the company's services.
- **Churned:** Customers who discontinued the company's services.
- **Joined:** Newly acquired customers.

This distinction is important because historical customers provide the labeled records required to train and evaluate the model, while newly joined customers form the target population for prospective churn prediction.

## 8. SQL Server: Data Exploration and ETL

SQL Server forms the foundation of the project's data preparation process. Instead of performing all transformations directly in spreadsheets, the project uses a relational database to organize customer records and create reusable analytical datasets.

### 8.1 Database Creation

The database `db_Churn` is created to store the staging table, production table, and analytical views.

```sql
CREATE DATABASE db_Churn;
```

The raw customer dataset is imported into `stg_Churn` using SQL Server's data import functionality.

### 8.2 Data Exploration

Before cleaning the data, SQL queries are used to understand its structure and identify useful patterns.

The exploration includes:

- Counting customers across different categories.
- Examining distinct values in columns such as Gender, Contract, State, and Customer_Status.
- Calculating category percentages.
- Comparing customer status with total revenue.
- Checking missing values across important customer attributes.

Example:

```sql
SELECT
    Contract,
    COUNT(Contract) AS TotalCount
FROM stg_Churn
GROUP BY Contract;
```

This query summarizes the number of records associated with each contract category and provides an initial understanding of the customer base.

### 8.3 Data Cleaning and Transformation

The raw dataset may contain missing values in optional service and churn-related columns. These values need to be handled consistently before the data is used for reporting.

The project uses SQL functions such as `ISNULL()` to replace missing categorical values with appropriate defaults, including `No`, `None`, and `Others`, depending on the column.

Example:

```sql
SELECT
    Customer_ID,
    ISNULL(Value_Deal, 'None') AS Value_Deal,
    ISNULL(Online_Security, 'No') AS Online_Security
FROM stg_Churn;
```

The transformed records are loaded into the production table `prod_Churn`.

Separating staging and production tables helps preserve the imported source data while providing a standardized dataset for downstream analysis.

### 8.4 Creating Analytical Views

Two SQL views are created to provide different datasets for the analytical workflow.

**`vw_ChurnData`**

Contains customers whose status is either `Stayed` or `Churned`. This view supplies the historical labeled data used for churn analysis and model training.

**`vw_JoinData`**

Contains customers whose status is `Joined`. This view supplies the newly acquired customer records used for churn prediction.

Example:

```sql
CREATE VIEW vw_ChurnData AS
SELECT *
FROM prod_Churn
WHERE Customer_Status IN ('Churned', 'Stayed');
```

Views simplify data access, reduce repeated filtering logic, and provide a consistent interface for Power BI and Python.

## 9. Power BI: Data Transformation and Modeling

Power BI is used to convert the prepared customer dataset into an interactive business intelligence solution.

Power Query handles additional transformations, while DAX is used to calculate the measures required for reporting.

### 9.1 Data Transformation

The Power BI preparation stage includes:

- Creating a numerical churn status column, where churned customers are represented by `1` and other statuses by `0`.
- Grouping monthly charges into ranges to compare customer behavior across pricing segments.
- Creating age groups for demographic analysis.
- Creating tenure groups to study how the length of the customer relationship relates to churn.
- Defining numeric sorting columns to display age and tenure groups in the correct order.
- Unpivoting service-related columns to create a service-level analytical table.

Unpivoting is particularly useful because it converts multiple service columns into a standardized structure containing a service name and its corresponding status. This makes it easier to compare service adoption and churn across different services.

### 9.2 DAX Measures and KPIs

The project includes four key metrics that summarize the customer base and its churn performance.

**Total Customers**

Counts the customer records included in the production dataset.

```dax
Total Customers =
COUNT(prod_Churn[Customer_ID])
```

**New Joiners**

Counts customers whose current status is `Joined`.

```dax
New Joiners =
CALCULATE(
    COUNT(prod_Churn[Customer_ID]),
    prod_Churn[Customer_Status] = "Joined"
)
```

**Total Churn**

Sums the numerical churn status for customers represented in the reporting context.

```dax
Total Churn =
SUM(prod_Churn[Churn Status])
```

**Churn Rate**

Measures the proportion of customers who churned relative to the total customer count.

```dax
Churn Rate =
DIVIDE([Total Churn], [Total Customers])
```

`DIVIDE()` provides safer division behavior when the denominator is zero. The churn rate measure should be formatted as a percentage.

These measures provide a reusable foundation for the dashboard and allow the KPIs to respond to report filters and customer segments.

## 10. Power BI Dashboard Development

The dashboard translates customer records into visual summaries that help users understand the size, composition, and behavior of the customer base.


### 10.1 Executive Summary Dashboard

The summary page provides a high-level overview of customer performance.

**Key Performance Indicators**

- Total Customers
- New Joiners
- Total Churn
- Churn Rate

**Demographic Analysis**

Gender and age-group visuals compare churn behavior across demographic segments.

**Account Analysis**

Contract type, payment method, and tenure groups help examine differences in churn across customer relationships and billing preferences.

**Geographic Analysis**

A state-level view highlights geographical variations in customer churn and helps identify areas that may require further investigation.

**Churn Distribution**

Churn categories summarize the recorded reasons for customer departures, while a tooltip provides additional detail about churn reasons.

**Service Analysis**

Internet type and individual service usage are analyzed to understand how churn is distributed among customers with different service combinations.

### 10.2 Churn Reason Tooltip

The churn reason tooltip provides additional information when users interact with relevant churn visuals.

Rather than displaying every reason directly on the main report page, the tooltip presents a more focused breakdown of churn reasons. This keeps the dashboard organized while making supporting details accessible when required.

### 10.3 Churn Prediction Dashboard

The prediction page is designed to analyze customer records classified as potential churners by the Python model.

It includes customer-level information such as:

- Customer ID
- Monthly Charge
- Total Revenue
- Total Refunds
- Number of Referrals

It also supports segmentation by gender, age group, marital status, payment method, contract type, tenure group, and state.

This page connects predictive modeling with business reporting, enabling stakeholders to explore the characteristics of customers identified as potentially at risk.

### 10.4 Dashboard Design

The report uses a consistent color palette to maintain visual clarity and distinguish important analytical elements.

The combination of KPI cards, categorical charts, demographic comparisons, and interactive tooltips supports both high-level reporting and detailed exploration.
<img width="1207" height="740" alt="image" src="https://github.com/user-attachments/assets/dc84797c-004c-4a8d-9c8d-0208bc5343c8" />
<img width="1282" height="736" alt="image" src="https://github.com/user-attachments/assets/994738a3-e45b-4947-9693-886d28666a35" />
<img width="1201" height="732" alt="image" src="https://github.com/user-attachments/assets/05e6ff8a-eda1-4d50-ba90-6bdb02fdbf39" />

## 11. Python: Customer Churn Prediction

While SQL and Power BI explain historical customer behavior, machine learning adds a predictive component to the project.

The objective is to learn patterns from historical customer records and use them to classify newly joined customers according to their potential churn risk.

### 11.1 Why Random Forest?

Random Forest is a supervised ensemble learning algorithm that combines multiple decision trees to produce a classification.

Each tree learns from a sample of the training data and considers a subset of features. The final classification is determined by combining the trees' predictions through majority voting.

Random Forest is suitable for this project because:

- It can model nonlinear relationships between customer characteristics and churn.
- It can capture interactions between multiple customer attributes.
- It supports numerical and encoded categorical features.
- Combining multiple trees can reduce the variance associated with relying on a single decision tree.
- It provides feature-importance scores that help identify influential predictive variables.

However, model performance depends on data quality, preprocessing, class distribution, and appropriate evaluation. Random Forest does not guarantee accurate predictions simply because it uses multiple trees.

### 11.2 Data Preparation

The historical dataset is loaded from the `vw_ChurnData` sheet exported from SQL Server.

The preprocessing workflow includes:

1. Removing the customer identifier and churn explanation columns from the model features.
2. Encoding categorical variables into numerical representations using `LabelEncoder`.
3. Converting the target variable into binary labels: `Stayed = 0` and `Churned = 1`.
4. Separating the independent variables (`X`) from the target variable (`y`).
5. Dividing the labeled data into training and testing sets.

The model uses the training set to learn patterns, while the testing set provides an independent evaluation of its predictions.

### 11.3 Model Training

The project uses `RandomForestClassifier` from Scikit-learn.

```python
from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)
```

Here, `n_estimators=100` specifies 100 decision trees, and `random_state=42` makes the randomized training procedure reproducible under the same data and environment.

### 11.4 Model Evaluation

The model generates predictions for the held-out testing data. Its performance is examined using a confusion matrix and a classification report.

The evaluation considers:

- **Precision:** The proportion of customers predicted to churn who actually churned.
- **Recall:** The proportion of actual churners correctly identified by the model.
- **F1-score:** The harmonic mean of precision and recall.
- **Confusion matrix:** The number of correct and incorrect predictions for each class.

Recall is particularly important in churn analysis because failing to identify a customer who will leave may mean losing an opportunity for timely retention action. Precision also matters because contacting too many customers who would otherwise stay can increase campaign costs.

The model's actual performance should be assessed from the evaluation results rather than assumed in advance.

### 11.5 Feature Importance

Random Forest provides feature-importance scores that indicate how much individual features contribute to the model's tree-based splits.

These scores can help prioritize further analysis of variables related to customer behavior, account characteristics, pricing, and service usage.

Feature importance indicates predictive usefulness, not causation. It should not be interpreted as proof that a particular attribute causes a customer to churn.

### 11.6 Predicting Newly Joined Customers

After training, the model is applied to records imported from the `vw_JoinData` sheet.

The workflow retains the original customer information, prepares the features using the fitted encoders, and generates predictions.

Customers predicted as churners are filtered and exported to a CSV file for further reporting.

This enables the project to move beyond describing past churn and toward identifying customers who may benefit from proactive retention campaigns.

## 12. Dashboard Deployment

## 12. Model Deployment Using Streamlit

The trained Random Forest model is deployed as an interactive web application using **Streamlit**. The model is saved using `joblib` and loaded through `app.py`, allowing users to predict customer churn without running the training process each time.

### 12.1 Deployment Architecture

```text
Customer Dataset
       |
       v
Data Preprocessing
       |
       v
Random Forest Model
  train_model.py
       |
       v
churn_model.joblib
       |
       v
Streamlit App (app.py)
       |
       +-------------------+
       |                   |
       v                   v
Single Prediction    Batch Prediction
       |                   |
       +---------+---------+
                 |
                 v
    Churn Probability & Risk Level
                 |
                 v
    Retention Suggestions & Results
```

### 12.2 Application Features

| Feature | Description |
|---|---|
| Single Customer | Enter customer details to obtain churn probability, risk level, and a suggested retention action. |
| Batch Prediction | Upload CSV or Excel files, rank customers by predicted churn risk, and download results. |
| About the Model | View accuracy, precision, recall, and feature importance. |

### 12.3 Churn Risk Classification

| Risk Level | Churn Probability |
|---|---|
| High | 60% or above |
| Medium | 30% to below 60% |
| Low | Below 30% |

These thresholds help translate model probabilities into actionable customer segments.

### 12.4 Revenue Calculation

The application calculates `Total_Revenue` automatically:

```text
Total Revenue = Total Charges - Refunds
              + Extra Data Charges
              + Long Distance Charges
```

### 12.5 Deployment Steps

1. Train the model using `python train_model.py` to generate `churn_model.joblib`.
2. Push `app.py`, `churn_model.joblib`, `requirements.txt`, and `train_model.py` to GitHub.
3. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
4. Create an app, select the repository and `main` branch, and specify `app.py` as the main file.
5. Click **Deploy** and test the application.
6. Add the live application link near the top of this README after deployment.

Ensure that the Scikit-learn versions used for training and deployment are compatible and that the same preprocessing steps are applied during prediction.

## 13. Power BI Reporting and Business Intelligence

Power BI provides interactive dashboards for analyzing historical churn, customer demographics, account information, service usage, and predicted churn records.

While Power BI supports aggregated analysis and business reporting, Streamlit provides an interface for individual and batch churn predictions. Together, they connect customer insights with predictive analytics and retention planning.


## 13. Key Findings and Analytical Insights

The project is designed to uncover customer segments and behavioral patterns associated with churn. The following are the principal areas of analysis:
Overall, 1,732 of 6,418 customers churned, a 27% churn rate, and there are 411 new joiners.
Contract type is the strongest driver: month-to-month churn is 47%, one-year 11% and two-year 3%.
Competitors are the top churn reason: 761 of 1,732 churners (about 44%) left for a competitor.
Fiber Optic customers churn most (41%), and customers paying by Mailed Check (38%) or Bank Withdrawal (34%) churn far more than Credit Card customers (15%).
Model result: 84% accuracy, 78% precision and 65% recall on churners.
Prediction: the model flagged 378 of 411 new joiners, 355 of them on month-to-month contracts.

I would be upfront that the 378 flagged is unusually high. New customers naturally have low total charges and revenue, which the model associates with churners, so the next step is to use only signup-time features and rank customers by churn probability rather than a yes/no label.


- **Demographic patterns:** Comparing churn rates across age groups and gender can reveal differences between customer segments.
- **Contract and tenure patterns:** Examining contract types and customer tenure helps identify groups that may require stronger retention support.
- **Payment behavior:** Comparing payment methods and billing preferences can reveal useful associations with churn.
- **Service adoption:** Analyzing internet types and additional services can help identify differences in churn across service combinations.
- **Geographic distribution:** State-level comparisons help locate areas where churn is relatively concentrated.
- **Recorded churn reasons:** Analyzing churn categories and reasons helps organize customer feedback into actionable themes.
- **Predictive identification:** The Random Forest model produces a list of newly joined customers classified as potential churners for further review.

These analyses help organize large volumes of customer data into interpretable business questions. Specific conclusions about the strongest churn drivers should be supported by the actual dashboard results and model evaluation.

## 14. Business Recommendations

Based on the types of insights produced by the project, the following strategies can be considered by a telecom business.

### 14.1 Targeted Retention Campaigns

Use customer segmentation and predicted churn classifications to prioritize retention outreach. Campaigns should focus on relevant customer needs rather than treating every customer identically.

### 14.2 Contract-Based Offers

Review churn rates across contract categories. If particular contract groups show consistently higher churn, evaluate suitable renewal incentives or longer-term plans.

### 14.3 Early Customer Engagement

Monitor newly joined customers and consider proactive onboarding, service guidance, and customer support during the early stages of their relationship with the company.

### 14.4 Service Quality Improvements

Investigate recorded churn reasons and service-related patterns to identify areas where connectivity, reliability, support, or service bundles may require improvement.

### 14.5 Personalized Pricing and Bundling

Use monthly charges, subscribed services, and customer behavior to evaluate whether alternative service packages or pricing options could improve customer satisfaction.

### 14.6 Data-Driven Decision-Making

Use Power BI KPIs to monitor churn trends and evaluate the results of retention campaigns over time. Campaign effectiveness should be measured rather than assumed.

### 14.7 Responsible Use of Predictions

Treat model predictions as indicators for further investigation, not as certain outcomes. Retention teams should consider prediction confidence, campaign costs, and the potential benefit of contacting each customer.

## 15. Project Limitations

Although the project demonstrates an end-to-end analytics workflow, several limitations should be considered.

- **Dataset limitations:** Results depend on the coverage, quality, and representativeness of the available customer dataset.
- **Missing-value treatment:** Replacing null values with defaults may simplify analysis but can hide distinctions between missing, unknown, and genuinely negative responses.
- **Categorical encoding:** Label encoding assigns numerical identifiers to categories. These identifiers do not necessarily represent a meaningful ranking, and unseen categories require careful handling.
- **Class imbalance:** If churners and non-churners are represented unequally, accuracy alone may provide a misleading picture of model performance.
- **Prediction uncertainty:** The model identifies patterns in historical data, but actual future customer behavior can differ.
- **Model validation:** Performance on a held-out test set does not establish performance on future customers. Additional validation and monitoring are required.
- **Feature importance:** Feature-importance scores show predictive associations and do not establish causal relationships.
- **Operational deployment:** The prediction workflow depends on exporting, preparing, and loading new customer data. Automated production scoring requires additional integration.
- **Data freshness:** Dashboard results depend on when the underlying data was last refreshed.
- **Business impact:** Retention strategies should be tested and measured before concluding that they reduce churn or improve profitability.

## 16. Repository Structure

The repository contains the project documentation and the implementation files used for the SQL, Power BI, and Python components.

A typical structure for this project may look like the following. The filenames should match the actual files in the repository.

```text
Telecom-Customer-Churn-Analysis-and-Prediction/
│
├── README.md
│
├── SQL/
│   └── SQL queries and ETL scripts
│
├── PowerBI/
│   └── Power BI report (.pbix)
│
├── Python/
│   └── Churn prediction notebook or scripts
│
├── Dataset/
│   └── Source data or dataset instructions
│
└── Predictions/
    └── Predicted churn output, if included
    └── Online Deploymwnt

```

The directory names above are illustrative. They should be adjusted to match the repository's actual layout rather than creating duplicate files or folders unnecessarily.

## 17. Acknowledgement

This project was developed as a practical learning exercise in end-to-end data analytics, business intelligence, and machine learning.

The project workflow and learning reference were informed by the *End-End Churn Analysis Portfolio Project* developed by Arpit Kumar. The reference provides guidance on telecom churn analysis, SQL Server ETL, Power BI dashboards, and Random Forest prediction.

The project combines these concepts with the implementation, analysis, and reporting developed for this repository. The dataset and supporting resources should be credited to their original source where applicable.

## 18. Conclusion

The Telecom Customer Churn Analysis and Prediction project demonstrates how SQL Server, Power BI, and Python can be integrated into a single analytical workflow.

SQL Server provides structured data preparation and reusable views. Power BI transforms the prepared records into interactive dashboards for customer segmentation and churn monitoring. Python and Random Forest extend the solution by classifying newly joined customers according to their potential churn risk.

Together, these components demonstrate the practical application of data engineering, descriptive analytics, business intelligence, and predictive modeling to a real-world business problem.

The project also highlights an important principle of analytics: **the value of data lies not only in understanding what happened, but also in using those insights to make better-informed decisions about what to do next.**

---

*Developed as a Data Analytics and Machine Learning portfolio project.*
