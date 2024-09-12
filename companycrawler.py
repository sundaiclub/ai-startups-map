# -*- coding: utf-8 -*-
"""companycrawler.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z-B9OfHkXc81JgseRp1skqd_mb7IYdIe
"""

import requests
import pandas as pd

def get_first_link(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['items'][0]['link']
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Read the Excel file, starting from A1 in Sheet5
excel_file = '2023-02-27-yc-companies.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet5', header=0)

# Extract links from column F and format them
links = df.iloc[:, 5].dropna().tolist()  # Column F is index 5 (0-based indexing)
formatted_links = [f'"{link}"' for link in links]

# Join the formatted links with commas
links_string = ','.join(formatted_links)

# Create the list of URLs (in this case, it's just the links from the Excel file)
urls = links[100:]

# Process all URLs and collect the results
results = [get_first_link(url) for url in urls]

# Add the results to the DataFrame in column G
df['f_link'] = pd.Series(results)

# Save the updated DataFrame back to the original Excel file
with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
    # Remove the existing Sheet5 if it exists
    if 'Sheet5' in writer.book.sheetnames:
        idx = writer.book.sheetnames.index('Sheet5')
        writer.book.remove(writer.book.worksheets[idx])

    # Write the updated DataFrame to Sheet5
    df.to_excel(writer, sheet_name='Sheet5', index=False)

print("Results have been added to column G (f_link) in the original Excel file.")

# Optionally, you can still save the results to a separate Excel file
result_df = pd.DataFrame({'Original Link': links, 'Search Result': results})
result_df.to_excel('search_results.xlsx', index=False)



!pip install openpyxl requests beautifulsoup4 Pillow

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64
import os

# Function to get the logo URL from a website
def get_logo_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for common logo elements
        logo = soup.find('link', rel='shortcut icon') or \
               soup.find('link', rel='icon') or \
               soup.find('meta', property='og:image')

        if logo:
            logo_url = logo.get('href') or logo.get('content')
            if logo_url and not logo_url.startswith('http'):
                return f"{url.rstrip('/')}/{logo_url.lstrip('/')}"
            return logo_url
    except:
        pass
    return None

# Function to convert image to base64
def image_to_base64(image_url):
    try:
        response = requests.get(image_url, timeout=5)
        img = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return None

# Load the Excel file
file_path = '2023-02-27-yc-companies.xlsx'
df = pd.read_excel(file_path, sheet_name='2023-02-27-yc-companies.csv')

# Add a new column for logos
df['logo'] = ''

# Process each website
for index, row in df.iterrows():
    website = row['website']
    if pd.notna(website):
        logo_url = get_logo_url(website)
        if logo_url:
            base64_image = image_to_base64(logo_url)
            if base64_image:
                df.at[index, 'logo'] = f'=IMAGE("data:image/png;base64,{base64_image}")'

    # Print progress
    if index % 10 == 0:
        print(f"Processed {index} websites")

# Save the updated Excel file
output_path = '2023-02-27-yc-companies_with_logos.xlsx'
df.to_excel(output_path, index=False, engine='openpyxl')

print(f"Completed. File saved as {output_path}")

import pandas as pd
import re

# Read the Excel file
# Adjust the path to where your file is located
df = pd.read_excel('2023-02-27-yc-companies_with_logos.xlsx', sheet_name='Sheet1', dtype=str)

# Function to extract base64 string from the IMAGE formula
def extract_base64(formula):
    if not isinstance(formula, str):
        return None
    match = re.search(r'base64,([^"]+)', formula)
    if match:
        return match.group(1)
    return None

# Apply the function to create a new column
df['base64_logo'] = df['logo'].apply(extract_base64)

# Display the first few rows to verify
print(df[['logo', 'base64_logo']].head())

# Save the updated DataFrame back to Excel
df.to_excel('updated_yc_companies_with_logos.xlsx', index=False)

print("Updated Excel file saved with new 'base64_logo' column.")