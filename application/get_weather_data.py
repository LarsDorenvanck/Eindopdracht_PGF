import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather_and_wind(latitude, longitude):
    """
    Fetch weather and wind data for a given latitude and longitude.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        tuple: A tuple containing the weather description and wind speed.
               If an error occurs, returns an error message string.
    """
    # OpenWeatherMap API endpoint and parameters
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY
    }
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return f"Error fetching weather data: Status code {response.status_code}"
        data = response.json()

        # Extract relevant information
        weather_description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        # Format and return the results
        return weather_description, wind_speed

    except requests.RequestException as e:
        return f"Error fetching weather data: {e}"

def calculate_fallout_radius_and_risk(wind_speed, blast_radius, weather_description):
    """
    Calculate the fallout radius and risk percentage based on wind speed, blast radius, and weather conditions.

    Args:
        wind_speed (float): The wind speed in m/s.
        blast_radius (float): The initial blast radius in km.
        weather_description (str): A description of the weather conditions.

    Returns:
        tuple: A tuple containing the calculated fallout radius and risk percentage.
    """
    #some estimation of what a reasonable spread factor is.
    spread_factor = wind_speed / 10
    fallout_radius = blast_radius * (1 + spread_factor)

    #Map weather to risk percentage. If weather is not mapped, use 67%
    weather_factor = {
        "rain": 1.0,
        "thunderstorm": 1.0,
        "clear": 0.53,
        "snow": 0.8
    }.get(weather_description.lower(), 0.67)
    
    risk_percentage = weather_factor * 100
    
    return fallout_radius, risk_percentage


if __name__ == "__main__":
    lat = 52.370216 #latitude amsterdam
    long = 4.895168 #longitude amsterdam
    get_weather_and_wind(lat, long)

