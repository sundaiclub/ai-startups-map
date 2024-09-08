import openai
from web_search import search_web
from scraper import scrape_text_from_url

openai_client = openai.OpenAI()


def get_query(location):
    prompt = '''
    Based on the given location write a google query to search for food/restaurants in that location.

    location: {location}
    Just output the query.
    query:
    '''
    prompt = prompt.format(location=location)

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content


def get_web_search_results(query):
    results = search_web([query])
    urls = []
    for k, v in results.items():
        for url_info in v:
            urls.append(url_info['url'])
    parsed_data = ''
    for url in urls:
        try:
            parsed_data += scrape_text_from_url(url)['scraped_text']
        except:
            pass
    return parsed_data


def get_food_recommendations_data(location):
    food_recommendation_prompt = '''
    Based on the given location and results from top google searches, write a point wise restaurant recommendation based on the scraped info.
    mention the restaurant name, cuisine it is famous for, address(if available), and rating.
    location: {location}
    scraped_data: {scraped_data}
    
    Just output the recommendation in markdown.
    recommendations:
    '''
    scraped_data = get_web_search_results(get_query(location))
    food_recommendation_prompt = food_recommendation_prompt.format(location=location, scraped_data=scraped_data)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{'role': 'user', 'content': food_recommendation_prompt}]
    )
    return response.choices[0].message.content