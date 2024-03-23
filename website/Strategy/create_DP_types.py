import csv
from collections import defaultdict

# Initialize a dictionary to store the combined text for each unique value in the first column
combined_data = defaultdict(str)

# Read the original CSV file
with open('../source_files/masterGOF_junk.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        # Remove "ï»¿" from the beginning of each column if present
        row = [col.lstrip('ï»¿') for col in row]
        category = row[0].strip()
        text = row[2].strip()
        combined_data[category] += text + ' '

# Write the new CSV file
with open('../source_files/DP_cat.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for category, text in combined_data.items():
        writer.writerow([category, text.strip()])

print('New CSV file has been created.')

    