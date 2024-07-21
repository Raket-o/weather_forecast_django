from typing import Any

import requests

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def get_geo_location_by_name_city(name_city: str) -> list | str:
    response = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={name_city}&count=10&language=ru&format=json")
    response = response.json()
    return response.get("results")


def get_forecast_weather(lat: float, lon: float) -> dict[Any, Any]:
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "forecast_days": 1,
        "hourly": "temperature_2m",
        "timezone": "Europe/Moscow",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m

    result = []
    result_dict = dict()
    for elem in zip(hourly_data.get("date"), hourly_data.get("temperature_2m")):
        date, hour = str(elem[0]).split(" ")
        hour = hour[:5]
        temperature = int(elem[1])
        result.append({"date": date, "hour": hour, "temperature": temperature})

    for elem in result:
        result_dict.setdefault(elem["date"], [])
        result_dict[elem["date"]].append({"hour": elem["hour"], "temperature": elem["temperature"]})

    return result_dict
