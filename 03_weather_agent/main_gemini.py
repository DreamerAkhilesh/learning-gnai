import os
import json
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_weather(location):
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
    ).json()

    if not geo.get("results"):
        return {"error": "Location not found"}

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,wind_speed_10m"
    ).json()

    return weather["current"]

def run_weather_agent(user_query):
    # Simple approach - ask the model to extract location and then get weather
    location_prompt = f"Extract the city/location name from this query: '{user_query}'. Return only the location name, nothing else."
    
    try:
        location_response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=location_prompt
        )
        location = location_response.text.strip()
        
        # Get weather data
        weather_data = get_weather(location)
        
        if "error" in weather_data:
            return f"Sorry, I couldn't find weather data for {location}"
        
        # Generate final response
        weather_prompt = f"""
        The user asked: {user_query}
        
        Weather data for {location}:
        Temperature: {weather_data['temperature_2m']}°C
        Wind Speed: {weather_data['wind_speed_10m']} km/h
        
        Please provide a natural, helpful response about the weather.
        """
        
        final_response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=weather_prompt
        )
        return final_response.text
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print(run_weather_agent(input(">> Ask >> ")))