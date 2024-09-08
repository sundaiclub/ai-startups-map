import json
from typing import Dict, List


def json_to_markdown(data: Dict[str, List[Dict[str, str]]]) -> str:
    markdown = "# Travel Itinerary\n\n"

    for day, activities in data.items():
        markdown += f"## {day.capitalize()}\n\n"

        for activity in activities:
            markdown += f"### {activity['location']}\n\n"
            markdown += f"**Type:** {activity['type_of_place']}\n\n"
            markdown += f"**Description:** {activity['description']}\n\n"
            markdown += f"**Duration:** {activity['approximate_duration']}\n\n"
            markdown += "---\n\n"

    return markdown.strip()
