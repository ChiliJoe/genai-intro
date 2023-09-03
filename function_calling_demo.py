import requests
import os
from serpapi import GoogleSearch


def do_search(search_term):
    params = {
        "engine": "google",
        "q": search_term,
        "api_key": os.getenv('SERPAPI_API_KEY')
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    result_list = [
        {
            'position': item['position'],
            'title': item['title'],
            'snippet': item['snippet'] if 'snippet' in item else '',
            'languages': item['about_this_result']['languages'][0] if 'about_this_result' in item and 'languages' in item['about_this_result'] else '',
            'regions': item['about_this_result']['regions'][0] if 'about_this_result' in item and 'regions' in item['about_this_result'] else ''
        }
        for item in results["organic_results"]
    ]

    return result_list

def get_current_weather(lat, lon, unit):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={unit}&appid={os.getenv('OWM_API_KEY')}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print("Error:", response.status_code)
        return None


def get_location_data(city, country, state=None):
    if state:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&appid={os.getenv('OWM_API_KEY')}"
    else:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={os.getenv('OWM_API_KEY')}"

    response = requests.get(url)

    if response.status_code == 200:
        location_data = response.json()
        return location_data
    else:
        print("Error:", response.status_code)
        return None


function_list = {
    "do_search":     {
        "function": do_search,
        "description": {
            "name": "do_search",
            "description": "Search google for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The term to search for in the web"
                    },
                },
                "required": ["search_term"],
            },
        }
    },
    "get_current_weather":     {
        "function": get_current_weather,
        "description": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given geo code",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {
                        "type": "number",
                        "description": "latitude",
                    },
                    "lon": {
                        "type": "number",
                        "description": "latitude",
                    },
                    "unit": {
                        "type": "string",
                        "description": "The temperature unit to use. Infer this from the location.",
                        "enum": ["standard", "metric", "imperial"]
                    },
                },
                "required": ["lat", "lon", "unit"],
            },
        }
    },
    "get_location_data": {
        "function": get_location_data,
        "description": {
            "name": "get_location_data",
            "description": "Get the geographic data by location name",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "name of the city",
                    },
                    "state": {
                        "type": "string",
                        "description": "name of the state - only for the US",
                    },
                    "country": {
                        "type": "string",
                        "description": "ISO 3166 country code",
                    },
                },
                "required": ["city", "country"],
            },
        }
    },
}

if __name__ == "__main__":
    function_descriptions = [f["description"] for f in function_list.values()]
    print(function_descriptions)
