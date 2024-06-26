#Download-from-OpenAlex.py

import requests
import json
import csv

# The URL of the OpenAlex API endpoint
url = 'https://api.openalex.org/authors/https://orcid.org/0000-0001-5048-1859'

# Send a GET request to the URL
response = requests.get(url)

# Parse the JSON response
data = response.json()

# Now you can access the fields in the data
print(f"ID: {data['id']}")
print(f"ORCID: {data['orcid']}")
print(f"Display Name: {data['display_name']}")
print(f"Works Count: {data['works_count']}")

