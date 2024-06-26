#This file will transform the doi into the SI link. change line 25 for different journal formats
import csv

# Specify the input and output file paths
input_file_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\OpenAlex\\jacs..csv'
output_file_path = 'C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\SI-w-DFT-coordinates\\OpenAlex\\jacs-doi-SI-link.csv'

# Open the input file in read mode and the output file in write mode
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
    # Create a CSV reader for the input file and a CSV writer for the output file
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate over the rows in the input file
    for row in reader:
        # Extract the DOI part from the URL
        doi_part = row[0].split('/')[-1]
        #print(doi_part) # debug

        # Extract the string after the "." as doi_label
        doi_label = doi_part.split('.')[-1]
        #print(doi_label) # debug

        # Replace the base URL in the first column of the row
        row[0] = 'https://pubs.acs.org/doi/suppl/10.1021/' + doi_part + '/suppl_file/ja' + doi_label + '_si_001.pdf'

        # Write the modified row to the output file
        writer.writerow(row)