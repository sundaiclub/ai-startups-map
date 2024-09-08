import openai
import re
import json

openai_client = openai.OpenAI()


def parse_response(response):
    response = re.findall(r"```json(.*?)```", response, re.DOTALL)
    if len(response) == 0:
        return None
    response = response[0].strip()
    return json.loads(response)


def get_preferences(questionnaire):
    prompt = f"""
    Based on the following information, generate a list of types of activities, things to do, kind of places to visit 
    that a person would like to do based on the questionnaire they answered.
    
    Generate 10-12 preferences.

    {questionnaire}
    
    the output should be a json object with the following format:
    {{'preferences': [p_1, p_2, p_3, p_4, p_5, ...]}}

    output:
    """

    preferences = None
    max_tries = 3
    while preferences is None:
        response = (
            openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            .choices[0]
            .message.content
        )
        preferences = parse_response(response)
        max_tries -= 1
        if max_tries == 0:
            break
    if preferences is None:
        return [
            "Historical landmarks & museums",
            "City tours & sightseeing",
            "Local cuisine & food tours",
            "Beaches & relaxation",
            "Hiking & nature trails",
            "Botanical gardens & parks",
            "Nightlife & entertainment",
        ]
    return preferences["preferences"]
