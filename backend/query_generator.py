import openai
import json
import re

openai_client = openai.OpenAI()


def parse_response(response):

    response = re.findall(r"```json(.*?)```", response, re.DOTALL)
    if len(response) == 0:
        return None
    response = response[0].strip()
    return json.loads(response)


def get_response(input_prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant who generates queries to search on google.'},
            {"role": "user", "content": input_prompt}],
    )
    return response.choices[0].message.content


def get_queries(location, date, traveling_with, preferences, additional_preferences):
    prompt = """
    Based on the following information, generate 5 queries to search on google to help plan my next trip.

    location: {location}
    date: {date}
    traveling_with: {traveling_with}
    preferences: {preferences}
    additional_preferences: {additional_preferences}


    the output should be a json object with the following format:
    {{'queries': [q_1, q_2, q_3, q_4, q_5]}}
    output:
    """

    single_query_prompt = """
    Based on the following information, generate a single query to search on google to help plan my next trip.

    location: {location}
    date: {date}
    traveling_with: {traveling_with}
    preferences: {preferences}
    additional_preferences: {additional_preferences}
    
    Output only the query in text format.
    output:
    """

    input_prompt = prompt.format(
        location=location,
        date=date,
        traveling_with=traveling_with,
        preferences=preferences,
        additional_preferences=additional_preferences
    )
    queries = None
    max_tries = 3
    while queries is None:
        queries = parse_response(get_response(input_prompt))
        max_tries -= 1
        if max_tries == 0:
            break

    if queries is None:
        single_query_prompt = single_query_prompt.format(
            location=location,
            date=date,
            traveling_with=traveling_with,
            preferences=preferences,
            additional_preferences=additional_preferences
        )
        return [get_response(single_query_prompt)]
    else:
        return queries['queries']

