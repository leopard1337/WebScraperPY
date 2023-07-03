import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Make a request to the website with a User-Agent header
url = 'INPUT_URL'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the page title
page_title = soup.title.string.strip() if soup.title else 'Title not found'

# Extract all valid links
validated_links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.startswith('http'):
        validated_links.append(href)

# Extract the titles of linked pages
linked_page_titles = []
for link in validated_links:
    linked_response = requests.get(link)
    linked_soup = BeautifulSoup(linked_response.content, 'html.parser')
    linked_title = linked_soup.title.string.strip() if linked_soup.title else 'Title not found'
    linked_page_titles.append(linked_title)

# Extract header texts
header_texts = [header.text.strip() for header in soup.find_all('h1')]

# Create a dictionary to store the captured data
data = {
    'page_title': page_title,
    'urls': [{'url': normalized_url, 'title': linked_page_title} for normalized_url, linked_page_title in zip(validated_links, linked_page_titles)],
    'headers': header_texts
}

# Save the data to a text file
with open('scraped_data.txt', 'w') as file:
    file.write(str(data))

# Save the data to a CSV file
df = pd.DataFrame(data['urls'])
df.to_csv('scraped_data.csv', index=False)

# Save the data to a JSON file
with open('scraped_data.json', 'w') as json_file:
    json.dump(data, json_file)

# Perform data analysis on captured data
df = pd.DataFrame(data['urls'])
print(df.head())  # Example analysis using Pandas

print("Web scraping completed. Data captured and saved to 'scraped_data.txt', 'scraped_data.csv', and 'scraped_data.json'.")
