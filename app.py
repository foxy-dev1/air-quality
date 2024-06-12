import streamlit as st
import pandas as pd
import altair as alt
from datetime import date,timedelta
import numpy as np



forecast_future = pd.read_csv('future_forecast.csv')

today = date.today()
weekday_name = today.strftime('%A')

Day = []
aqi_values = []

for x in (range(7)):
    date = today + timedelta(x)
    weekday_name = date.strftime('%A')
    aqi = np.floor(forecast_future.loc[forecast_future['ds']==pd.Timestamp(date),'yhat'].values[0])

    Day.append(weekday_name)
    aqi_values.append(aqi)
    

dict = {'Day':Day,'AQI':aqi_values}

df = pd.DataFrame(dict)


def aqi_color(aqi):
    if 0 <= aqi <= 50:
        return 'green'
    elif 51 <= aqi <= 100:
        return 'yellow'
    elif 101 <= aqi <= 150:
        return 'orange'
    elif 151 <= aqi <= 200:
        return 'red'
    elif 201 <= aqi <= 300:
        return 'purple'
    elif 301 <= aqi <= 500:
        return 'maroon'
    else:
        return 'gray'

df['Color'] = df['AQI'].apply(aqi_color)

df['Day'] = pd.Categorical(df['Day'], categories=Day, ordered=True)

st.title('Weekly Air Quality Index (AQI)')
st.write('This app shows the AQI values for each day of the week.')


st.subheader('AQI Bar Chart')
bars = alt.Chart(df).mark_bar().encode(
    x=alt.X('Day'),
    y='AQI',
    color=alt.Color('Color:N', scale=None)
).properties(
    width=600,
    height=400
)


text = bars.mark_text(
    align='center',
    baseline='bottom',
    dy=-10 
).encode(
    text='AQI'
)


chart = bars + text

st.altair_chart(chart, use_container_width=True)
