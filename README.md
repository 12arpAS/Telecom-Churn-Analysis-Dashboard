# Telecom-Customer-Churn-Analysis-Dashboard
End-to-end data analytics project analyzing customer churn using SQL, Power BI dashboards, and Python machine learning models to predict customers likely to leave.

**#📊 Customer Churn Analysis & Prediction Project**

**##1. Introduction to Churn Analysis**

In today’s highly competitive business environment, customer retention has become one of the most important factors for long-term success. Companies invest significant resources in acquiring new customers, but losing existing customers can lead to revenue loss and reduced growth.
Customer churn refers to the percentage of customers who stop using a company’s product or service during a given time period. Understanding why customers leave and identifying early warning signs are essential for developing effective retention strategies.
Churn analysis uses data analytics, business intelligence tools, and machine learning techniques to examine customer behavior, detect churn patterns, and predict which customers are likely to leave in the future. By identifying these customers early, businesses can take proactive actions such as personalized offers, improved services, or targeted marketing campaigns.
This project focuses on analyzing telecom customer data to understand churn behavior and build a system that helps businesses visualize churn trends and predict potential churners.

**##2. Target Audience**

Although this project analyzes churn in a telecom company, the methodology and techniques used can be applied across many industries, including:

1. Telecommunications
2. Banking and financial services
3. Retail and e-commerce
4. ubscription services
5. Healthcare platforms
Any organization that relies on customer loyalty and long-term relationships can benefit from churn analysis. The insights derived from this project help organizations improve customer satisfaction and reduce customer attrition.

**##3. Project Objectives**

The primary goal of this project is to build a complete end-to-end data analytics solution for analyzing and predicting customer churn.

**Key objectives include:**

Build a complete ETL pipeline using SQL Server
Clean and transform raw customer data
Perform data exploration and validation
Create interactive dashboards using Power BI
Analyze churn based on:
Demographic information
Geographic location
Payment and account details
Services used by customers
Identify patterns that characterize customers who churn
Provide business insights to design targeted marketing campaigns
Develop a machine learning model using Python to predict future churners

**##4. Why I Chose This Project**

While exploring real-world business problems in data analytics, I realized that one of the biggest challenges companies face today is customer churn. Many businesses, especially in industries like telecom, banking, and subscription services, lose customers every day. When customers leave, companies not only lose revenue but also the opportunity to build long-term relationships.
This made me curious about an important question: Can data help businesses predict which customers are likely to leave before it actually happens?

To explore this question, I decided to work on a Customer Churn Analysis and Prediction project. My goal was to analyze customer behavior, identify patterns that lead to churn, and build a machine learning model capable of predicting future churners.

This project was also a great opportunity for me to apply multiple data analytics skills together. I used SQL for data extraction and transformation, Power BI for interactive dashboards, and Python with machine learning algorithms to build predictive models.

**##5. Tools and Technologies Used**

1. SQL Server	Data storage and ETL pipeline
2. SQL Server Management Studio	Database management and queries
3. Power BI	Data visualization and dashboard creation
4. Python	Machine learning model for churn prediction
5. CSV Dataset	Source data for analysis

**##6. Key Metrics Analyzed**

The project focuses on several important business metrics that help understand customer churn:

Total Customers – Total number of customers in the dataset
Total Churn – Number of customers who have left the service
Churn Rate – Percentage of customers who churned
New Joiners – Number of new customers who joined the service

These metrics provide a high-level view of customer growth and retention performance.

**##7. Project Architecture**

The project follows a structured data analytics workflow:

**Raw CSV Dataset
       ↓
SQL Server ETL Pipeline
       ↓
Data Cleaning & Transformation
       ↓
Power BI Dashboard Analysis
       ↓
Python Machine Learning Model
       ↓
Prediction of Future Churners**

This architecture ensures data reliability, scalability, and efficient analysis.

**#8. Step 1 – ETL Process in SQL Server**

The first step of the project involves building an ETL (Extract, Transform, Load) pipeline in SQL Server.

**##Data Import**

The dataset was imported from a CSV file into a staging table using the SQL Server Import Wizard.
Important steps included:

Assigning Customer_ID as the primary key
Allowing null values during import to prevent errors
Converting BIT columns to VARCHAR(50) to avoid import issues

**##Data Exploration**

After importing the data, several SQL queries were executed to analyze the dataset.
Examples include:

Customer distribution by Gender

**SELECT Gender, Count(Gender) as TotalCount,
Count(Gender)  1.0 / (Select Count() from stg_Churn)  as Percentage
from stg_Churn
Group by Gender**

Contract type distribution

**SELECT Contract, Count(Contract) as TotalCount,
Count(Contract)  1.0 / (Select Count() from stg_Churn)  as Percentage
from stg_Churn
Group by Contract**

Revenue contribution by Customer Status

**SELECT Customer_Status, Count(Customer_Status) as TotalCount, Sum(Total_Revenue) as TotalRev,
Sum(Total_Revenue) / (Select sum(Total_Revenue) from stg_Churn) * 100  as RevPercentage
from stg_Churn
Group by Customer_Status**

State-wise customer distribution

**SELECT State, Count(State) as TotalCount,
Count(State)  1.0 / (Select Count() from stg_Churn)  as Percentage
from stg_Churn
Group by State
Order by Percentage desc**
These queries help understand the overall structure and patterns in the dataset.

**##Data Quality Check**

A null value analysis was performed to identify missing data across all columns.
The SQL query counted null values for attributes such as:

Age
Gender
Payment Method
Internet Services
Streaming Services
Revenue fields
.................

This SQL query checks the stg_Churn table to find how many NULL (missing) values are present in each column. It uses a CASE statement to mark NULL values as 1 and non-NULL values as 0. Then the SUM() function adds these values to calculate the total missing values for every column. Each column such as Gender, Age, State, and Contract gets its own NULL count. This helps identify missing data so it can be cleaned before further analysis or processing.

**##Data Cleaning**

Null values were handled using the ISNULL() function to replace missing values with default values such as:

"None"
"No"
"Others"
    
**##Creating Views for Power BI**

Two SQL views were created to simplify Power BI analysis.
1. vw_ChurnData
2. vw_JoinData
   
**Create View vw_ChurnData as
select * from prod_Churn where Customer_Status In ('Churned', 'Stayed')**

**Create View vw_JoinData as
select * from prod_Churn where Customer_Status = 'Joined'**
These both views helped in doing the machine learning prediction task and dashboard creating for future churners.


**#8. Step 2 – Data Transformation in Power BI**

After loading data into Power BI, several transformations were performed.

**Calculated Columns**
**1. Churn Status**

**2. Monthly Charge Range**

Customers were grouped based on monthly charges:
< 20
20 – 50
50 – 100
> 100
**3.Age Group Mapping**

Customers were grouped into age categories:
< 20
20 – 35
36 – 50
> 50
This helps analyze churn behavior across different age segments.
> 
**##4.Tenure Group Mapping**

Customer tenure was categorized into groups:
< 6 Months
6 – 12 Months
12 – 18 Months
18 – 24 Months
>= 24 Months

Tenure analysis helps identify new customers who are more likely to churn.

**##5.Services Transformation**

Service-related columns were unpivoted to create a structured table showing:
Service type
Whether the service is active
This simplifies analysis of service adoption patterns.

**#8. Step 3 – Power BI Measures**

Several DAX measures were created to calculate key business metrics.

**Total Customers**

Total Customers = COUNT(prod_Churn[Customer_ID])
**New Joiners**

New Joiners = CALCULATE(COUNT(prod_Churn[Customer_ID]),
prod_Churn[Customer_Status] = "Joined")
**Total Churn**

Total Churn = SUM(prod_Churn[Churn Status])
**Churn Rate**

Churn Rate = [Total Churn] / [Total Customers]

These measures power the KPI cards and charts in the dashboard.

**#9. Power BI Dashboard Analysis**

The Power BI dashboard visualizes churn trends across multiple dimensions.

Main analysis areas include:

**Demographic Analysis**
Age group
Gender
Marital status

**Geographic Analysis**
Customer distribution by state
Regional churn patterns

**Account & Payment Analysis**
Contract type
Payment method
Monthly charges

**Service Usage Analysis**
Internet service type
Streaming services
Security services

These visualizations allow stakeholders to quickly identify churn drivers.

**#10. Machine Learning Prediction**

To enhance the analysis, a machine learning model was built using Python to predict future churners.
The process included:

**Data preprocessing
Feature encoding
Train-test split
Model training
Model evaluation
Churn prediction**
The model helps businesses identify customers at risk before they leave.

For predicting customer churn, we will be using a widely used Machine Learning algorithm called RANDOM FOREST.

**#Importing Libraries & Data Load**

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble
import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

**Read the data from the specified sheet into a pandas DataFrame**
data = pd.read_excel(file_path, sheet_name=sheet_name)

**Display the first few rows of the fetched data**
print(data.head())

**#Data Preprocessing**

**Drop columns that won't be used for prediction**
data = data.drop(['Customer_ID', 'Churn_Category', 'Churn_Reason'], axis=1)

**List of columns to be label encoded**

columns_to_encode = [

    'Gender', 'Married', 'State', 'Value_Deal', 'Phone_Service', 'Multiple_Lines',

    'Internet_Service', 'Internet_Type', 'Online_Security', 'Online_Backup',

    'Device_Protection_Plan', 'Premium_Support', 'Streaming_TV', 'Streaming_Movies',

    'Streaming_Music', 'Unlimited_Data', 'Contract', 'Paperless_Billing',

    'Payment_Method'

]

**Encode categorical variables except the target variable**

label_encoders = {}

for column in columns_to_encode:

    label_encoders[column] = LabelEncoder()

    data[column] = label_encoders[column].fit_transform(data[column])

**Manually encode the target variable 'Customer_Status'**

data['Customer_Status'] = data['Customer_Status'].map({'Stayed': 0, 'Churned': 1})

**Split data into features and target**

X = data.drop('Customer_Status', axis=1)

y = data['Customer_Status']

**Split data into training and testing sets**

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

 Train Random Forest Model

# Initialize the Random Forest Classifier

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

**Feature Selection using Feature Importance**

importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

**Plot the feature importances**

plt.figure(figsize=(15, 6))
sns.barplot(x=importances[indices], y=X.columns[indices])
plt.title('Feature Importances')
plt.xlabel('Relative Importance')
plt.ylabel('Feature Names')
plt.show()

**#Use Model for Prediction on New Data**

**Define the path to the Joiner Data Excel file**

file_path = r"C:\yourpath\Prediction_Data.xlsx"
new_data = pd.read_excel(file_path, sheet_name=sheet_name)
print(new_data.head())
original_data = new_data.copy()
customer_ids = new_data['Customer_ID']

**Drop columns that won't be used for prediction in the encoded DataFrame**

new_data = new_data.drop(['Customer_ID', 'Customer_Status', 'Churn_Category', 'Churn_Reason'], axis=1)

**Encode categorical variables using the saved label encoders**

for column in new_data.select_dtypes(include=['object']).columns:

    new_data[column] = label_encoders[column].transform(new_data[column])

** #Make predictions**

new_predictions = rf_model.predict(new_data)

**Add predictions to the original DataFrame**

original_data['Customer_Status_Predicted'] = new_predictions

**Filter the DataFrame to include only records predicted as "Churned"**

original_data = original_data[original_data['Customer_Status_Predicted'] == 1]

**Save the results**
original_data.to_csv(r"C:\yourpath\Predictions.csv", index=False)


**#11. Key Insights from the Analysis**

The analysis revealed several important patterns:

Customers with month-to-month contracts churn more frequently
Customers with short tenure have higher churn probability
Higher monthly charges increase churn likelihood
Customers using fewer services are more likely to churn

These insights provide valuable guidance for customer retention strategies.

**#12. Business Recommendations**

Based on the findings, businesses can reduce churn by:

Encouraging long-term contracts
Offering discounts or loyalty rewards
Improving customer support services
Providing bundled service packages
Targeting high-risk customers with personalized retention campaigns

**#13. Project Outcomes**

This project successfully demonstrates an end-to-end data analytics workflow, including:

Building a SQL ETL pipeline
Performing data cleaning and transformation
Creating interactive Power BI dashboards
Applying machine learning for churn prediction
Generating actionable business insights















