import os
import requests

search_url = "https://api.bing.microsoft.com/v7.0/search"


def search_web(queries, count=5):
    results = {}
    for query in queries:
        print("    Searching for query:", query)
        headers = {"Ocp-Apim-Subscription-Key": os.getenv("BING_SEARCH_API_KEY")}
        params = {
            "q": query,
            "textDecorations": True,
            "textFormat": "HTML",
            "count": count,
        }

        # Make the request to Bing API

        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()

        # Extract the search results
        search_results = response.json()

        results[query] = search_results

    final_results = {}
    for key, value in results.items():
        final_results[key] = []
        for res in value["webPages"]["value"]:
            url = res["url"]
            title = res["name"]
            final_results[key].append({"url": url, "title": title})

    return final_results
