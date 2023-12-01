import json
import glob
import csv

# List of JSON files to combine
json_files = glob.glob('*.json')

# Open a CSV file for writing
with open('combined_patterns.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Iterate through each JSON file
    for file_name in json_files:
        with open(file_name, 'r') as file:
            data = json.load(file)

            # Write each key-value pair to the CSV
            for key, value in data.items():
                writer.writerow([key, value])