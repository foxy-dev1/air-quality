import requests
import pandas as pd
from datetime import datetime
import csv,os

def get_data():
    
    api_key = os.environ.get('AIR_QUALITY_API')

    latitude = 19.0336118
    longitude = 73.0181395749251

    aqicn_base_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}'

    aqicn_url = f'{aqicn_base_url}&appid={api_key}'

    response = requests.get(aqicn_url)

    if response.status_code == 200:
        data = response.json()  
        print("Air Quality Data fetched successfully:", data)
        return data
    else:
        print("Failed to fetch Air Quality Data. Status code:", response.status_code)
        return None


def update_csv(data, csv_filename= '/home/runner/work/air-quality/air-quality/air_quality_data.csv'):
    header = ['Timestamp', 'PM2.5', 'PM10','O3','NO2','SO2', 'CO']
    params = [[d['components']['pm2_5'],d['components']['pm10'],d['components']['o3'],d['components']['no2'],d['components']['so2'],d['components']['co']] for d in data['list']]

    row = [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        params[0][0],
        params[0][1],
        params[0][2],
        params[0][3],
        params[0][4],
        params[0][5],

    ]

    try:
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

        file_exists = os.path.isfile(csv_filename) and os.path.getsize(csv_filename) >0

        with open(csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            if not file_exists:
                csv_writer.writerow(header)
            csv_writer.writerow(row)
        print("Data successfully added to CSV.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


if __name__ == "__main__":
    print("Current Working Directory:", os.getcwd())  # Print the current working directory

    air_quality_data = get_data()

    if air_quality_data:
        update_csv(air_quality_data)
