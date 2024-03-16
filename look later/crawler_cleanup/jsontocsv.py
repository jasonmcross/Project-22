# importing packages
import pandas as pd
import csv
import glob
import json
from pandas import json_normalize as jn

json_files = glob.glob('*.json')

dfsn = []
dfs = {}

for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            if key in dfs:
                # If the key already exists, append the new value
                dfs[key].append(value)
            else:
                # If the key does not exist, create a new list with the value
                dfs[key] = [value]
        
with open('combined.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in dfs.items():
        combined_values = "; ".join(value)
        writer.writerow([key, combined_values])
#print(dfs)

#df = pd.concat(dfsn, ignore_index=True)
#df.to_csv('springframework.csv', index=False)