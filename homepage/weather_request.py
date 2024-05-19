import numpy as np
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import pandas as pd

power_installation = 2.5
panel_efficiency = 0.2
om = openmeteo_requests.Client()

def request_data(latitude, longitude):
    params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunshine_duration"]
    }

    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(3).ValuesAsNumpy()

    daily_estimated_energy = power_installation * daily_sunshine_duration * panel_efficiency

    daily_data = {
        "Date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
            ).strftime('%d/%m/%Y')
        }

    daily_data["Weather Icon"] = standarize_weather_code(daily_weather_code)
    daily_data["Max. Temperature"] = daily_temperature_2m_max
    daily_data["Min. Temperature"] = daily_temperature_2m_min
    daily_data["Est. Energy"] = daily_estimated_energy

    daily_dataframe = pd.DataFrame(data = daily_data)
    columns_to_round = ["Max. Temperature", "Min. Temperature", "Est. Energy"]
    for col in columns_to_round:
        daily_dataframe[col] = daily_dataframe[col].round(2)
        daily_dataframe[col] = daily_dataframe[col].map('{:.2f}'.format)
    dataframe_dict = daily_dataframe.to_dict(orient="records")
    transposed_data = {key: [day[key] for day in dataframe_dict] for key in dataframe_dict[0]}

    return transposed_data

def standarize_weather_code(daily_weather_code):
    # 0, 1 - clear sky, 2 - partly cloud, 3 - cloud, 45, 48 - fog, 51, 53, 55 - drizzle
    # 56, 57 - freezing drizzle, 61, 63, 65, 80, 81, 82 - rain
    # 66, 67 - freezing rain, 71, 73, 75, 85, 86 - snow	
    # 77 - snow grains,	95 -thunder, 96, 99 thunder with hail
    mapping = {
    0: 0, 1: 0, 2: 1,
    3: 2, 45: 3, 48: 3,
    51: 4, 53:4, 55:4,
    56: 5, 57: 5,
    61: 6, 63: 6, 65: 6, 80: 6, 81: 6, 82: 6,
    66: 7, 67: 7,
    71: 8, 73: 8, 75: 8, 85: 8, 86: 8,
    77: 9, 95: 10, 96: 11, 99: 11
}
    new_column_array = np.where(np.isin(daily_weather_code, list(mapping.keys())), daily_weather_code, -1)
    new_column_array = np.vectorize(mapping.get)(new_column_array)
    return new_column_array