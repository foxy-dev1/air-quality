import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import numpy as np
from prophet import Prophet
import os


filtered_df = pd.read_csv('data/filtered_df.csv')
test_df = pd.read_csv('air_quality_data.csv')
test_df.drop(columns=['PM10','O3','NO2','SO2','CO'],inplace=True)
test_df.rename(columns={'Timestamp':'index','PM2.5':'pm25'},inplace=True)
test_df['index'] = pd.to_datetime(test_df['index']).dt.date

combined_df = pd.concat([filtered_df, test_df], ignore_index=True)
combined_df.rename(columns={'index': 'ds', 'pm25': 'y'}, inplace=True)

model = Prophet(interval_width=0.80, yearly_seasonality=True)
model.fit(combined_df)

future = model.make_future_dataframe(periods=15)
forecast_future = model.predict(future)

csv_filepath = '/home/runner/work/air-quality/air-quality/future_forecast.csv'

forecast_future.to_csv(csv_filepath,index=False)
