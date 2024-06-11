import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
import numpy as np
from prophet import Prophet
import os
from github import Github

# Load data
filtered_df = pd.read_csv('data/filtered_df.csv')
test_df = pd.read_csv('data/test_df.csv')
combined_df = pd.concat([filtered_df, test_df], ignore_index=True)
combined_df.rename(columns={'index': 'ds', 'pm25': 'y'}, inplace=True)

# Train the Prophet model
model = Prophet(interval_width=0.80, yearly_seasonality=True)
model.fit(combined_df)

# Make future predictions
future = model.make_future_dataframe(periods=7)
forecast_future = model.predict(future)

# Get the last 10 lines of the forecast
forecast_last_10 = forecast_future.tail(10)

# Convert the last 10 lines of the forecast to CSV
forecast_csv = forecast_last_10.to_csv(index=False)

# Authenticate to GitHub
token = os.getenv('TOKEN_GITHUB')
g = Github(token)

# Check the rate limit
rate_limit = g.get_rate_limit().core
print(f"Remaining API requests: {rate_limit.remaining}")
print(f"Rate limit resets at: {rate_limit.reset}")

# If rate limit is exceeded, exit early
if rate_limit.remaining == 0:
    reset_time = (rate_limit.reset - datetime.datetime.utcnow()).total_seconds()
    print(f"Rate limit exceeded. Waiting for {reset_time} seconds until reset.")
    exit(1)

# Define repository details
repo_name = 'foxy-dev1/air-quality'
file_path = 'forecast.csv'  # Adjust to the correct path in your repo
commit_message = 'update forecast data'

# Get the repository
repo = g.get_repo(repo_name)

# Function to get file contents with rate limit handling
def get_file_contents(repo, file_path):
    try:
        contents = repo.get_contents(file_path)
        print("File contents retrieved successfully.")
        return contents
    except Exception as e:
        raise e

# Get the file contents
contents = get_file_contents(repo, file_path)

# Update the file in the repository
try:
    repo.update_file(contents.path, commit_message, forecast_csv, contents.sha)
    print("File updated successfully.")
except Exception as e:
    print(f"Error updating file: {e}")
