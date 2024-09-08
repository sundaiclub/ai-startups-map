import requests
from bs4 import BeautifulSoup


def scrape_text_from_url(url):
    # Step 1: Send a request to the website
    response = requests.get(url, timeout=5_000, verify=False)
    response.raise_for_status()  # Check that the request was successful

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Step 3: Find and extract all useful text (body, paragraphs, etc.)
    paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])

    scraped_text = []
    for paragraph in paragraphs:
        text = paragraph.get_text().strip()
        if text:  # Only add non-empty text
            scraped_text.append(text)

    # Join the extracted text into a single string
    scraped_text = "\n\n".join(scraped_text)

    # Step 4: Return the URL and the scraped text in a dictionary
    return {"url": url, "scraped_text": scraped_text}
