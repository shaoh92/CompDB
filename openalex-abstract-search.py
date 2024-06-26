import pyalex
import json
from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders

import pyalex
pyalex.config.email = "huiling.shao1992@gmail.com"

pyalex.config.email = "your_email@example.com"

# Make a request to the OpenAlex API for an author
author_data = Authors()["https://orcid.org/0000-0001-8007-6408"]

# Open the file in write mode ('w')
with open('OpenAlex-test.txt', 'w') as f:
    # Use json.dump to write the author_data to the file
    json.dump(author_data, f, indent=4)