import pyalex
import json
from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders
import os

pyalex.config.email = "huiling.shao1992@gmail.com"

directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\OpenAlex'

# Test of the OpenAlex API - Make a request to the OpenAlex API for an author
author_data = Authors()["https://orcid.org/0000-0001-8007-6408"]

# Join the directory_path and the filename to create the full file path
file_path = os.path.join(directory_path, 'HS-pub.txt')

# Open the file in write mode ('w')
with open(file_path, 'w') as f:
    # Use json.dump to write the author_data to the file
    json.dump(author_data, f, indent=4)
# Completed. Test of the OpenAlex API - Make a request to the OpenAlex API for an author

