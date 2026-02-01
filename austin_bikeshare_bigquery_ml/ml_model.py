from google.cloud import bigquery
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT = os.getenv('PROJECT')

# Initialize Client
client = bigquery.Client(project=PROJECT)

# Fetch data
query = """
SELECT
    start_time,
    start_station_name,
    end_station_name,
    subscriber_type,
    duration_minutes
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
WHERE duration_minutes > 0 AND duration_minutes < 120
LIMIT 100000
"""

print("Fetching data from BigQuery...")
df = client.query(query).to_dataframe()

# Feature Engineering
print("Engineering features...")

# Extract time-based features
df['start_time'] = pd.to_datetime(df['start_time'])
df['hour'] = df['start_time'].dt.hour
df['dayofweek'] = df['start_time'].dt.dayofweek
df['month'] = df['start_time'].dt.month

# Drop the original timestamp
df = df.drop('start_time', axis=1)

# Encode categorical variables
#le_station = LabelEncoder()
#le_subscriber = LabelEncoder()

# Target encoding for start_station_name
station_means = df.groupby('start_station_name')['duration_minutes'].mean()
df['start_station_encoded'] = df['start_station_name'].map(station_means)
df = df.drop('start_station_name', axis=1)

# Clean subscriber types
def clean_sub_type(st):
    st = str(st).lower().strip()
    if 'annual' in st or 'local365' in st:
        return 'annual_member'
    if 'walk up' in st or 'single trip' in st:
        return 'casual_rider'
    if 'student' in st:
        return 'student'
    return 'other'

df['subscriber_type_clean'] = df['subscriber_type'].apply(clean_sub_type)

# One-Hot encoding for subscriber_type
df = pd.get_dummies(df, columns=['subscriber_type_clean'], prefix='sub')
df = df.drop('subscriber_type', axis=1)

print(f"New columns created: {df.columns.tolist()}")

#df['start_station_name'] = le_station.fit_transform(df['start_station_name'])
#df['subscriber_type'] = le_subscriber.fit_transform(df['subscriber_type'])

print(df.head())

# Prepare for training
print("Splitting data...")
X = df.drop(['duration_minutes', 'end_station_name'], axis=1)
y = df['duration_minutes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
print("Training model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=1)
model.fit(X_train, y_train)

# Model evaluation
print("Evaluating model...")
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model performance:")
print(f"Mean Absolute Error: {mae:.2f} minutes")
print(f"R2 Score: {r2:.2f}")

# Check feature importance
importances = pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_})

print("Feature importance:")
print(importances.sort_values(by='importance', ascending=False))

# Visualization: actual vs predicted
plt.figure(figsize=(10,6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.3)
plt.plot([0,120], [0,120], color='red', linestyle='--')
plt.title('Actual vs Predicted Trip Duration')
plt.xlabel('Actual Duration (min)')
plt.ylabel('Predicted Duration (min)')
plt.show()

# Visualization: error distribution
plt.figure(figsize=(10,6))
error = y_test - y_pred
sns.histplot(error, bins=30, kde=True)
plt.title('Distribution of Prediction Errors')
plt.xlabel('Error (Actual - Predicted) in Minutes')
plt.show()