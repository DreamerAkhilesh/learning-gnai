import os
import json
import requests
import re
from dotenv import load_dotenv

load_dotenv()

def get_weather(location):
    """Get weather data from Open-Meteo API"""
    try:
        # Get coordinates for the location
        geo_response = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        )
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {"error": f"Location '{location}' not found"}

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]
        country = geo_data["results"][0].get("country", "")

        # Get weather data
        weather_response = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min"
            f"&timezone=auto"
        )
        weather_data = weather_response.json()

        current = weather_data["current"]
        daily = weather_data["daily"]

        # Weather code descriptions (simplified)
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }

        weather_desc = weather_codes.get(current["weather_code"], "Unknown")

        return {
            "location": f"{city_name}, {country}",
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "condition": weather_desc,
            "max_temp": daily["temperature_2m_max"][0],
            "min_temp": daily["temperature_2m_min"][0]
        }

    except Exception as e:
        return {"error": f"Failed to get weather data: {str(e)}"}

def extract_location_from_query(query):
    """Simple location extraction from user query"""
    query = query.lower()
    
    # Remove common weather-related words
    weather_words = ['weather', 'temperature', 'temp', 'forecast', 'climate', 'how', 'is', 'the', 'in', 'at', 'for', 'what', 'whats', "what's", '?', '!']
    
    words = query.split()
    location_words = [word for word in words if word not in weather_words]
    
    # Join remaining words as location
    location = ' '.join(location_words).strip()
    
    # If no location found, ask user
    if not location:
        return None
    
    return location

def format_weather_response(weather_data):
    """Format weather data into a nice response"""
    if "error" in weather_data:
        return weather_data["error"]
    
    response = f"""
🌤️ Weather for {weather_data['location']}:

🌡️ Current Temperature: {weather_data['temperature']}°C
📊 Condition: {weather_data['condition']}
💧 Humidity: {weather_data['humidity']}%
💨 Wind Speed: {weather_data['wind_speed']} km/h

📈 Today's High: {weather_data['max_temp']}°C
📉 Today's Low: {weather_data['min_temp']}°C
    """.strip()
    
    return response

def run_weather_agent(user_query):
    """Main weather agent function"""
    location = extract_location_from_query(user_query)
    
    if not location:
        return "Please specify a location. For example: 'Delhi weather' or 'What's the weather in New York?'"
    
    weather_data = get_weather(location)
    return format_weather_response(weather_data)

if __name__ == "__main__":
    while True:
        try:
            query = input("\n>> Ask about weather (or 'quit' to exit): ")
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            response = run_weather_agent(query)
            print(response)
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")