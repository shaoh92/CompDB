import csv
import os
import re
import collections

# Specify the directory path and the file name
directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\OpenAlex'
file_name = 'OAlex-PL-KNH-CJC-doi.csv'

# Join the directory_path and the file_name to create the full file path
file_path = os.path.join(directory_path, file_name)

# Create a Counter object
counter = collections.Counter()

# Create a dictionary to store the rows by type
rows_by_type = collections.defaultdict(list)

# Open the CSV file with the 'utf-8' encoding
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    # Iterate over the rows in the CSV file
    for row in reader:
        for cell in row:
            match = re.search(r'https://doi\.org/10\.1021/([^0-9]*)', cell)
            if match:
                # Extract the type from the DOI
                type = match.group(1)

                # Add the row to the list of rows for this type
                rows_by_type[type].append(row)

# Filter the rows_by_type dictionary to keep only the types with 10 or more rows
rows_by_type = {type: rows for type, rows in rows_by_type.items() if len(rows) >= 10}

# Create a counter for the filtered types
filtered_counter = collections.Counter({type: len(rows) for type, rows in rows_by_type.items()})

# Get the types and their counts in descending order of the counts
ranking = filtered_counter.most_common()

# Print the ranking
for type, count in ranking:
    print(f'Type: {type}, Count: {count}')

# Get the types and their counts in descending order of the counts
ranking = filtered_counter.most_common()

# Iterate over the types in the ranking
for type, count in ranking:

    # Create the full file path for the new CSV file
    new_file_path = os.path.join(directory_path, f'{type}.csv')

    # Open a new CSV file in write mode for each type
    with open(new_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write the rows for this type to the CSV file
        for row in rows_by_type[type]:
            writer.writerow(row)