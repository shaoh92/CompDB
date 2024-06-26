# This script will use the doi-url to find SI of the pdf of interest
import requests
from bs4 import BeautifulSoup
import sys
import os
import random

# Create a new directory for error files if it doesn't exist
err_dir = 'err'
os.makedirs(err_dir, exist_ok=True)

# Redirect standard error output to a file
sys.stderr = open(os.path.join(err_dir, 'error.err'), 'w')

# The URL you want to scrape
url = 'https://pubs.acs.org/doi/10.1021/acs.orglett.5b03171'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

try:
    # Choose a random user agent
    user_agent = random.choice(user_agents)

    # Send a GET request to the URL with the user agent
    response = requests.get(url, headers={'User-Agent': user_agent})
    print(response)

    # Parse the content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup.prettify())
    # Now you can use the `soup` object to find tags, navigate the parse tree, etc.
    # For example, to find all <a> tags:
    a_tags = soup.find_all('a')

    # Initialize a counter for the number of files found
    files_found = 0

    for tag in a_tags:
        print(tag.get('href'))
        href = tag.get('href')
        if href and (href.endswith('.pdf') or href.endswith('.xyz') or href.endswith('.txt')):
            print(os.path.basename(href))
            files_found += 1

    # If no files were found, print a message
    if files_found == 0:
        print("No files found.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}", file=sys.stderr)