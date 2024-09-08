from get_web_info import get_itinerary_info
from get_food_recommendations import get_food_recommendations_data
from tiktok_generator import generate_tiktok
import openai
from openai import OpenAI
import json
from stored_strings import standard_output, itinerary_system_prompt
import ast
import os
import uuid
from get_preferences_from_questionnaire import get_preferences
import pandas as pd
import pydeck as pdk

from geopy.geocoders import Nominatim

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    print("Error: OPENAI_API_KEY is not set.")
else:
    print("API Key retrieved successfully.")

preferences = travel_keywords = [
    "Historical landmarks & museums",
    "City tours & sightseeing",
    "Local cuisine & food tours",
    "Beaches & relaxation",
    "Hiking & nature trails",
    "Botanical gardens & parks",
    "Nightlife & entertainment",
    "Shopping & local markets",
    "Art galleries & exhibitions",
    "Cultural festivals & events",
    "Boat rides & water activities",
    "National parks & natural reserves",
    "Theme parks & attractions",
    "Adventure sports & outdoor activities",
    "Religious & spiritual sites",
    "Cooking classes & culinary experiences",
    "Wine, brewery & beverage tastings",
    "Zoos, aquariums & wildlife",
    "Theater, concerts & live performances",
]

traveling_options = ["Friend", "Family", "Couple", "Solo", "Group"]


def get_itinerary(
    location, date, traveling_with, preferences, additional_preferences, outsourced=None
) -> dict:
    """
    :param location: str
    :param date: list
    :param traveling_with: str
    :param preferences: str
    :param additional_preferences: str
    :return: itinerary: dict
    """
    print("Getting information from web ...")
    outsourced = get_itinerary_info(
        location, date, traveling_with, preferences, additional_preferences
    )
    print("Generating itinerary ... ")
    for _ in range(3):
        json_string = raw_itinerary(
            location,
            date,
            traveling_with,
            preferences,
            additional_preferences,
            outsourced=outsourced,
        )
        print("Raw Itinerary")
        print(json_string)
        try:
            ast.literal_eval(json_string)
            return json.loads(json_string)
        except:
            pass
    return "Failed"


def generate_video(itinerary, city) -> str:
    """
    Takes in an itinerary dict and generates a video and saves it to a file
    :param itinerary: dict
    :return: filepath: str
    """
    print("Generating Video ...")
    save_dir = f"data/{uuid.uuid4()}"
    filepath = generate_tiktok(itinerary, city, save_dir)
    print("Video saved at:", filepath)
    return filepath


def raw_itinerary(
    location, date, traveling_with, preferences, additional_preferences, outsourced=None
):
    itinerary_user_prompt = f"""
  Location: {location}.
  Date: {date}.
  Who I am traveling with: {traveling_with}.
  Preferences on activites: {preferences}.
  Additional preferences: {additional_preferences}.
  Data/recommendations from some prominent webpages: {outsourced}.
  """
    print("Calling GPT-4o mini ...")
    generate_itinerary_client = OpenAI(api_key=OPENAI_API_KEY)
    itinerary_response = generate_itinerary_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": itinerary_system_prompt},
            {"role": "user", "content": itinerary_user_prompt},
        ],
    )
    raw_itinerary = itinerary_response.choices[0].message.content
    return raw_itinerary


import pandas as pd
import pydeck as pdk

from geopy.geocoders import Nominatim


def get_lat_long(place_name):
    geolocator = Nominatim(user_agent="travel_buddy_application")
    location = geolocator.geocode(place_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None


def get_map(plan, city):
    print("Generating map ...")
    city_loc = get_lat_long(city)
    if city_loc is None:
        print("Couldn't get location of the city")
        return None

    locations = []
    for v in plan.values():
        for x in v:
            locations.append(x["location"])

    lat_lon = [x for x in map(get_lat_long, locations) if x]
    chart_data = pd.DataFrame(
        data=dict(
            lat=[x[0] for x in lat_lon],
            lon=[x[1] for x in lat_lon],
        )
    )
    # st.dataframe(chart_data)
    # chart_data.columns = ["lat", "lon"]
    layers = pdk.Layer(
        "HexagonLayer",
        data=chart_data,
        get_position=["lon", "lat"],
        radius=200,
        elevation_scale=4,
        elevation_range=[0, 3000],
        pickable=True,
        extruded=True,
    )
    map_ = pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=city_loc[0],
            longitude=city_loc[1],
            zoom=11,
            pitch=50,
        ),
        layers=[layers],
    )
    return map_


def get_food_recommendations_(city_name):
    print("Generating food recommendations ...")
    return get_food_recommendations_data(city_name)


def get_dynamic_preferences(questionnaire):
    print("Getting dynamic preferences ...")
    return get_preferences(questionnaire)
