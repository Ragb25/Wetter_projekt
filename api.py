import requests
import json
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime
from flask import jsonify

"""
Diese Methode ermöglich mit der Name einer Stadt Informationen wie Longitude und Latitude zu kriegen.
Somit können wie die Daten einfach mit openmeteo-API hochladen.
"""
def getInfo(stadt):
    if not stadt:
        return None
    lat, lon = None, None
    header = {
        "User-Agent": "Mein erstes Projekt mit einer API Nutzung (ragb25@tu-clausthal.de)",
    }

    params = {
        "q": f"{stadt}",
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    
    
    url = f"https://nominatim.openstreetmap.org/search"

    try:
        responses = requests.get(url, params=params, headers=header)
        data = responses.json()
        lon = data[0]["lon"]
        lat = data[0]["lat"]
        address = data[0]["address"]
        #print(adress)
    except requests.exceptions.HTTPError as HTTPError:
        print(f"Nicht möglich: {HTTPError}")
    except requests.exceptions.Timeout as timeout:
        print(f"nicht möglich: {timeout}")
    except requests.ConnectionError as connectionError:
        print(f"nicht möglich: {connectionError}")
    return lon, lat, address

"""
Diese Funktion nutzt die Latitude und Longitude, um die Wetterdaten der entsprechenden Stadt mittels openmeteo-API zu bestimmen. 
"""
def wetter_daten(lon, lat):
    if not lon or not lat:
         return None
    try:
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
    
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "wind_speed_10m", "relative_humidity_2m"],
        }
        responses = openmeteo.weather_api(url, params = params)
    
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        # Process current data. The order of variables needs to be the same as requested.
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_wind_speed_10m = current.Variables(1).Value()
        current_relative_humidity_2m = current.Variables(2).Value()
    
        a = current.Time()
        b = current_temperature_2m
        c = current_wind_speed_10m
        d = current_relative_humidity_2m
        return a, b, c, d
    except requests.exceptions.HTTPError as HTTPError:
            print(f"Nicht möglich: {HTTPError}")
    except requests.exceptions.Timeout as timeout:
        print(f"nicht möglich: {timeout}")
    except requests.ConnectionError as connectionError:
        print(f"nicht möglich: {connectionError}")

"""
Hier wird die Wetterdaten von 7 Tagen gezeigt.
"""
def vorhersage(lon, lat):
    if not lon or not lat:
         return None
    try:
    # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
    
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "temperature_2m_min"],
        }
        responses = openmeteo.weather_api(url, params = params)
    
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    
        daily_data = {
            "date": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
                end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            )
        }
    
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min
    
        daily_dataframe = pd.DataFrame(data = daily_data)
        return f"\nDaily data\n", daily_dataframe
    except requests.exceptions.HTTPError as HTTPError:
                print(f"Nicht möglich: {HTTPError}")
    except requests.exceptions.Timeout as timeout:
        print(f"nicht möglich: {timeout}")
    except requests.ConnectionError as connectionError:
        print(f"nicht möglich: {connectionError}")

"""
Diese Funktion dienst dazu, alle Daten so zu organisieren, dass sie direkt von der
app benutzt werden können.
"""
def daten_organisation(lon, lat):
    timestamp, current_temperature, current_wind_speed, current_relative_humidity = wetter_daten(lon, lat)

    date = datetime.fromtimestamp(timestamp)

    wetter_vorhersage = vorhersage(lon, lat)
    
    return  date, float("{:.3f}".format(current_temperature)), float("{:.3f}".format(current_wind_speed)), current_relative_humidity, wetter_vorhersage[1]

    
     








while True:
    lon, lat, adress = getInfo("Hannover")
    if not lon or not lat:
        print(f"Fehler: {stadt} ist keine gültige Stadt")
        continue
    else:
       
        tag = wetter_daten(lon, lat)
        print(int(tag[1]))
            
        
        break

