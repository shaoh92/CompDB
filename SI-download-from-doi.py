#This file will download the supporting information (pdf) with a given doi
import requests
import os
import csv
import time
import random
from PyPDF2 import PdfReader
import logging

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Specify the directory path and the file name
directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\OpenAlex'
file_name = 'jacs-doi-SI-link.csv'

successful_rows = []

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

keywords = ["density functional theory", "DFT", "cartesian coordinates"]

# Initialize the counter
successful_downloads = 0

print("Starting to process CSV file...") # debug

with open(os.path.join(directory_path, file_name), 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        url = row[0]
        print(f"Processing URL: {url}")
        wait_time = random.randint(300, 500)
        print(f"Waiting for {wait_time} seconds before sending GET request...")
        time.sleep(wait_time)  # Wait for a random amount of time between 0 and 100 seconds
        headers = {
            'User-Agent': random.choice(user_agents)
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # This will raise an HTTPError if the response was an HTTP 4XX or 5XX
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
            if response.status_code == 403:
                logging.error("Received 403 Client Error. Stopping script.")
                raise SystemExit(err)
        except Exception as err:
            logging.error(f"Other error occurred: {err}")
        else:

            # Extract the file name from the URL
            file_name = url.split('/')[-1]

            # Create the full file path
            file_path = os.path.join(directory_path, file_name)

            # Write the content of the response to a new file
            with open(file_path, 'wb') as f:
                f.write(response.content)

            print(f"SI-pdf successfully downloaded from {url}")

            # Open the PDF file in read-binary mode
            with open(file_path, 'rb') as f:
                pdf = PdfReader(f)
                text = " ".join(page.extract_text() for page in pdf.pages)
                print(f"Searching {file_name} for keywords...")

            # Check if any of the keywords are in the text
                contains_keyword = any(keyword in text for keyword in keywords)

            # Close the PDF file before trying to delete it
                f.close()

            if not contains_keyword:
                # If not, delete the file and print a message
                os.remove(file_path)
                print(f"{file_name} does not contain any of the keywords. File deleted.")
            else:
                print(f"{file_name} contains at least one of the keywords.")
                successful_rows.append(row)
                successful_downloads += 1  # Increment the counter

print("Finished processing CSV file.")
print(f"Number of successfully downloaded PDFs: {successful_downloads}")

# Write the successful rows back to the CSV file
#with open(os.path.join(directory_path, file_name), 'w', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerows(successful_rows)