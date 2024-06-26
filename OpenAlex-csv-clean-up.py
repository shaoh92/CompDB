#OpenAlex-csv-clean-up.py

import os
import pandas as pd


# Directory containing the CSV files
directory = "C:\\Users\\huili\\OneDrive\\Documents\\UCLA\\Reserach\\CompDB\\HS-PL-CJC-KNH-2014to2024"

# # Get a list of all CSV files in the directory
# csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# # Read each CSV file and append it to a list
# dfs = [pd.read_csv(os.path.join(directory, f)) for f in csv_files]

# # Concatenate all dataframes in the list
# combined_df = pd.concat(dfs, ignore_index=True)

# # Remove duplicate rows
# combined_df.drop_duplicates(inplace=True)

# # Write the combined dataframe to a new CSV file
# combined_df.to_csv(os.path.join(directory, 'combined.csv'), index=False)

# Read the combined CSV file with 'latin1' encoding
df = pd.read_csv(os.path.join(directory, 'combined.csv'), encoding='latin1')

# Remove rows where primary_location_display_name contains "Review"
df = df[~df['primary_location_display_name'].str.contains('Review', case=False, na=False)]

# Remove rows where doi is blank
df = df.dropna(subset=['doi'])

# Remove duplicate 'doi' values
df = df.drop_duplicates(subset='doi', keep='first')

# Remove rows where 'cited_by_count' is 0
df = df[df['cited_by_count'] != 0]

# Sort the dataframe by publication_date
df.sort_values('publication_date', inplace=True)

# Print the total number of lines
print(f"Total number of lines: {len(df)}")

# Write the sorted dataframe back to the CSV file
df.to_csv(os.path.join(directory, 'combined.csv'), index=False)

# Create a new DataFrame that only includes the 'doi' column
doi_df = df[['doi']]

# Write the 'doi' DataFrame to a new CSV file
doi_df.to_csv(os.path.join(directory, 'doi.csv'), index=False)