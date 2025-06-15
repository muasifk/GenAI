import pandas as pd
import requests
import json
from google.genai.types import Tool, FunctionDeclaration, Part
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="weather-app") 
##  https://github.com/philschmid/gemini-samples/blob/main/guides/function-calling.ipynb



# For JSON
def get_weather_forecast(location, date):
    location_obj = geolocator.geocode(location)
    if location_obj:
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={location_obj.latitude}&longitude={location_obj.longitude}&hourly=temperature_2m&start_date={date}&end_date={date}"
            response = requests.get(url)
            data = response.json()
            if "hourly" in data and data["hourly"]:
                result = {time: temp for time, temp in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"])}
                return result
            else:
                return {"error": "No hourly data available"}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Location not found"}
    
# Test the function directly
# result = get_weather_forecast("New York, NY", "2025-06-15")
# print(f"Final result: {result}")


########################  Using Python
def get_weather_forecast2(location: str, date: str) -> str:
    """
    Retrieves the weather using Open-Meteo API for a given location (city) and a date (yyyy-mm-dd). Returns a list dictionary with the time and temperature for each hour."
    
    Args:
        location (str): The city and state, e.g., San Francisco, CA
        date (str): The forecasting date for when to get the weather format (yyyy-mm-dd)
    Returns:
        Dict[str, float]: A dictionary with the time as key and the temperature as value
    """
    location = geolocator.geocode(location)
    if location:
        try:
            response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&hourly=temperature_2m&start_date={date}&end_date={date}")
            data = response.json()
            return {time: temp for time, temp in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"])}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Location not found"}
    

get_weather_forecast_func = {
    "name": "get_weather_forecast",
    "description": "Retrieves the weather using Open-Meteo API for a given location (city) and a date (yyyy-mm-dd). Returns a list dictionary with the time and temperature for each hour.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g., San Francisco, CA"
            },
            "date": {
                "type": "string",
                "description": "the forecasting date for when to get the weather format (yyyy-mm-dd)"
            }
        },
        "required": ["location","date"]
    }
}

# # Function dictionary to map the function name to the function
functions = {
    "get_weather_forecast": get_weather_forecast
    }

# # helper function to bind schema to function
def call_function(function_name, **kwargs):
    return functions[function_name](**kwargs)




