# Austin Bikeshare Data Analysis & Prediction

This project explores the Austin Bikeshare public dataset using Google BigQuery and implements a Machine Learning model to predict trip durations.

**Project Overview**
- Data Source: `bigquery-public-data.austin_bikeshare`
- Goal: Explore trip patterns and build a regression model to predict how long a trip will last (`duration_minutes`) based on starting conditions.

**File Structure**
- `data_exploration.py`: SQL-based exploration of the dataset (Top stations, peak hours, subscriber behavior).
- `ml_model.py`: Machine Learning pipeline including data cleaning, feature engineering, and model training.

**Feature Engineering**

To improve model accuracy, several transformations were applied:
1. Target Encoding: Replaced starting stations with their historical average trip duration.
2. One-Hot Encoding: Categorized subscriber types into standardized groups (Annual, Casual, Student).
3. Temporal Features: Extracted hour, day of the week, and month from trip timestamps.

**Environment Setup**
```bash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt