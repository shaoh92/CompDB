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
                # Remove lines that start with "S" followed by digits (likely page numbers)
                page_text = re.sub(r'^S\d+.*$', '', page_text, flags=re.MULTILINE)
                text += page_text
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
                        body = []
                        k = j + 2
                        while len(body) < X:
                            line = lines[k].strip()
                            # Check if the line is a valid coordinate (contains exactly 4 elements)
                            if len(line.split()) == 4:
                                body.append(line)
                            k += 1
                        # Write the X, unique label and the body to the CSV file
                        writer.writerow([X, label] + body)
        # Close the PDF file
        doc.close()
print("step 1 done. Coordinates extracted from PDF files and saved as *-coord.csv.")

# Import necessary modules
import os
import csv
import re

# Define the directory where the CSV files are located
csv_directory = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates'

# Get a list of all CSV files in the directory that end with "-coord.csv"
invalid_files_count = 0
csv_files = [f for f in os.listdir(csv_directory) if f.endswith("-coord.csv")]

# Loop through each CSV file in the list
for csv_filename in csv_files:
    # Open the current CSV file for reading
    with open(os.path.join(csv_directory, csv_filename), 'r', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        # Loop through each row in the CSV file
        for i, row in enumerate(reader):
            # Initialize filename to None
            filename = None
            # Loop through each column in the row
            for column in row:
                # Check if the column contains "TS"
                if 'TS' in column:
                    # If filename is not already set, find the first digit/word in this column as the filename
                    if not filename and column.strip():  # if the column is not blank
                        filename = re.search(r'\b\w+\b', column).group(0)
            # If "TS" was found and a filename was set
            if filename:
                # Create a new directory named after the CSV file (without the extension)
                new_dir = os.path.join(csv_directory, os.path.splitext(csv_filename)[0])
                # Create the new directory if it doesn't already exist
                os.makedirs(new_dir, exist_ok=True)
                # Construct the name of the new .xyz file
                new_filename = os.path.join(new_dir, filename + '.xyz')
                # Open the new .xyz file for writing
                with open(new_filename, 'w', newline='') as new_file:
                    # Write the row to the new .xyz file, with each column in a new row
                    for item in row:
                        # Only write the item to the file if it's not blank
                        if item.strip():
                            new_file.write("%s\n" % item)
                # Open the new .xyz file for reading
                with open(new_filename, 'r') as check_file:
                    # Read all lines in the file
                    lines = check_file.readlines()
                    # Get the value of "X" from the first line
                    X = int(lines[0].strip())
                    # Count the number of non-blank lines in the file
                    non_blank_lines = sum(1 for line in lines if line.strip())
                    # If the count does not match "X" plus 2, print the name of the .xyz file
                    if non_blank_lines != X + 2:
                        invalid_files_count += 1
                        print(f"Invalid file: {new_filename}")
print(f"Number of invalid files: {invalid_files_count}")             

print("step 2 done. We printed xyz coordinates in the new directory named after the CSV file (without the extension).")

import os
import subprocess
import shutil
from rdkit import Chem

# Replace 'your_directory_path' with the path to your directory containing .xyz files
directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\cs0c00111_si_001-coord'

# Replace 'path_to_obabel' with the full path to your obabel executable
path_to_obabel = 'C:\\Program Files\\OpenBabel-3.1.1\\obabel.exe'

# Open a null file for redirecting stderr
with open(os.devnull, 'w') as null:
    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        # If the file is a .xyz file
        if filename.endswith(".xyz"):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)
            # Construct the path for the .mol file
            mol_file_path = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}.mol")
            # Use Open Babel to convert the .xyz file to a .mol file, redirecting stderr to null
            subprocess.run([path_to_obabel, file_path, '-O', mol_file_path], stderr=null)

print("step 3 done. .xyz files are converted to .mol files with openbabel")