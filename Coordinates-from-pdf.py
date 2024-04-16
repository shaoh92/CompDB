import os
import fitz
import csv
import re
import pandas as pd

directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates'

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    # If the file is a PDF
    if filename.endswith(".pdf"):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        # Open the PDF file with fitz
        doc = fitz.open(file_path)
        # Create a new CSV file for each PDF, named after the PDF with '-coord' appended
        csv_filename = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}-coord.csv")
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(['X', 'Label'] + [f'Coordinate {i+1}' for i in range(16)])
            # Get the entire text of the PDF as a single string
            text = ""
            for page in doc:
                page_text = page.get_text()
                # Replace lines that start with "S" followed by digits (likely page numbers) with "TOBEREMOVED"
                page_text = re.sub(r'^S\d+', 'TOBEREMOVED', page_text, flags=re.MULTILINE)
                text += page_text
            # Remove the "TOBEREMOVED" anchors
            text = text.replace('TOBEREMOVED', '')
            # Split the text into lines
            lines = text.splitlines()
            # Loop through each line
            for j, line in enumerate(lines):
                # If the line contains a number and nothing else
                if line.strip().isdigit():
                    # Get the number of atoms (X)
                    X = int(line)
                    # Check if X is larger than or equal to 16
                    if X >= 16:
                        # Check if j + 1 is within the range of lines
                        if j + 1 < len(lines):
                            # Get the unique label
                            label = lines[j + 1].strip()
                            # Get the body of the "Cartesian coordinates"
                            body = [coord.strip() for coord in lines[j + 2 : j + 2 + X]]
                            # Write the X, unique label and the body to the CSV file
                            writer.writerow([X, label] + body)
        # Close the PDF file
        doc.close()

print("step 1 done. Coordinates extracted from PDF files and saved as *-coord.csv. Note: Some empty units may be present in the CSV files. Need to remove them later")

import csv
import os

# Specify the directory where the CSV files are
csv_directory = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates'

# Get the list of CSV files in the directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith("-coord.csv")]

# Loop through each CSV file
for csv_filename in csv_files:
    # Construct the name of the new CSV file
    new_csv_filename = os.path.splitext(csv_filename)[0] + "-TS.csv"

    # Open the original CSV file for reading and the new CSV file for writing
    with open(os.path.join(csv_directory, csv_filename), 'r', newline='') as csvfile, open(os.path.join(csv_directory, new_csv_filename), 'w', newline='') as new_csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(new_csvfile)
        # Loop through each row in the original CSV file
        for row in reader:
            # Convert the row to a string to check for "TS"
            row_str = ' '.join(row)
            # If "TS" is in the row
            if 'TS' in row_str:
                # Write the row to the new CSV file
                writer.writerow(row)

print("step 2 done. All coordinates with TS label are filterd out to a new file as *-coord-TS.csv. Note: Some empty units may be present in the CSV files. Need to remove them later")