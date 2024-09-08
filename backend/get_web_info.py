import os
import openai
import sys
from bs4 import BeautifulSoup
import requests

import time

from query_generator import get_queries
from scraper import scrape_text_from_url
from web_search import search_web

subscription_key = os.environ["BING_SEARCH_API_KEY"]


def get_itinerary_info(
    location, date, traveling_with, preferences, additional_preferences
):
    print("  Generating queries for itinerary ...")

    queries = get_queries(
        location, date, traveling_with, preferences, additional_preferences
    )

    web_search_results = search_web(queries, count=2)

    urls = []
    for k, v in web_search_results.items():
        for url_info in v:
            urls.append(url_info["url"])
    parsed_data = ""
    for url in urls:
        print("  Scraping url:", url)
        try:
            parsed_data += scrape_text_from_url(url)["scraped_text"] + "\n\n"
        except:
            pass
    return parsed_data
