import json

import json

# Load JSON data from a file
with open('stackoverflow.json', 'r') as file:
    data = json.load(file)

# Create a new dictionary for modified data
modified_data = {}

# Iterate over each key-value pair in the original data
for key, value in data.items():
    # Split the key and take only the first word
    first_word = key.split()[0]
    # Add to the modified data dictionary
    modified_data[first_word] = value

# Optional: Save the modified data back to a new JSON file
with open('modSO.json', 'w') as file:
    json.dump(modified_data, file, indent=4)