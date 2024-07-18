from typing import List, Dict, Any

import requests

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


# def converting_results(results: dict) -> list:
#     cities_list = []
#     for data in results.get("results"):
#         country = data.get("country")
#         area = data.get("admin1")
#         name = data.get("name")
#         latitude, longitude = data.get("latitude"), data.get("longitude")
#         cities_list.append([country, area, name, latitude, longitude])
#         # print(f"{country}, {area}, {name}, {latitude}, {longitude}")
#     return cities_list


def get_geo_location_by_name_city(name_city: str) -> list | str:
    # name_city = "Саратов"
    # name_city = "Сама"
    # city = "654iunt67imn87"
    response = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={name_city}&count=10&language=ru&format=json")
    response = response.json()
    # print(response)
    # converting_results(response)
    # return response
    # if response.get("results"):
    return response.get("results")
        # return converting_results(response)
    #     for data in response.get("results"):
    #         country = data.get("country")
    #         area = data.get("admin1")
    #         name = data.get("name")
    #         latitude, longitude = data.get("latitude"), data.get("longitude")
    #         print(f"{country}, {area}, {name}, {latitude}, {longitude}")
    # else:
    #     return("Не нашёл такой город")


def get_forecast_weather(lat: float, lon: float) -> list[dict[str, int | Any]]:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "forecast_days": 1,
        "hourly": "temperature_2m",
        "timezone": "Europe/Moscow",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    # print(hourly.Time())
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m

    # print(hourly_data)
    # my_dick_Datetime = hourly_data["date"]
    # my_dick_Datetime = hourly_data.get("date")
    # list_datetime = []
    # for elem in hourly_data["date"]:
    #     date, hour = str(elem).split(" ")
    #     hour = hour[:5]
    #     list_datetime.append((date, hour))
        # print(type(date), date)
        # print(type(temperature), temperature)
        # print()
    # print(list_datetime)
    # print(hourly_data.get("temperature_2m")
    # temperatures = []
    # for elem in hourly_data.get("temperature_2m"):
    #     temperatures.append(int(elem))
    # print(temperatures)
    # for i in zip(list_datetime, temperatures):
    #     print(i)


    result = []
    for elem in zip(hourly_data.get("date"), hourly_data.get("temperature_2m")):
        date, hour = str(elem[0]).split(" ")
        hour = hour[:5]
        temperature = int(elem[1])
        # print(elem[0])
        result.append({"date": date, "hour": hour, "temperature": temperature})

    return result




    # hourly_dataframe = pd.DataFrame(data=hourly_data)
    # print(hourly_dataframe)


# print(get_geo_location_by_name_city("Чапаевск"))
