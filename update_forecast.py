import streamlit as st
import pandas as pd
import altair as alt
from datetime import date,timedelta
import numpy as np
from prophet import Prophet
import os
from github import Github


filtered_df = pd.read_csv('data/filtered_df.csv')

test_df = pd.read_csv('data/test_df.csv')

combined_df = pd.concat([filtered_df,test_df],ignore_index=True)

combined_df.rename(columns={'index':'ds','pm25':'y'},inplace=True)


model = Prophet(interval_width=0.80,yearly_seasonality=True)

model.fit(combined_df)

future = model.make_future_dataframe(periods=7)
forecast_future = model.predict(future)

forecast_csv = forecast_future.to_csv(index=False)

token = os.getenv('TOKEN_GITHUB')
repo_name = 'foxy-dev1/air-quality'
file_path = '/home/runner/work/air-quality/air-quality/forecast.csv'
commit_message = 'update forecast data'

g = Github(token)
repo = g.get_repo(repo_name)


contents = repo.get_contents(file_path)

repo.update_file(contents.path, commit_message, forecast_csv, contents.sha)
