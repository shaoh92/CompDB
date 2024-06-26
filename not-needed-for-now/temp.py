import csv
import os

# Specify the directory path and the file name
directory_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\OpenAlex'
file_name = 'OAlex-ACS-2020-to-2024-doi.csv'

# Join the directory_path and the file_name to create the full file path
file_path = os.path.join(directory_path, file_name)

# Generate the output file name based on the input file name
base_name, ext = os.path.splitext(file_name)
output_file_name = f'{base_name}-filtered{ext}'

# Specify the output file path
output_file_path = os.path.join(directory_path, output_file_name)

# Open the CSV file with the 'utf-8' encoding
with open(file_path, 'r', encoding='utf-8') as f, open(output_file_path, 'w', newline='', encoding='utf-8') as out_f:
    reader = csv.reader(f)
    writer = csv.writer(out_f)
    for row in reader:
        row_string = ' '.join(row).lower()
        if 'rev' not in row_string and 'account' not in row_string:
            writer.writerow(row)