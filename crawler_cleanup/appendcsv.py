import pandas as pd
import glob
import csv

# List of CSV files to combine
path = 'G:/Project-22/crawler/data/'
csv_files = glob.glob(path + '/*GOF.csv')

dfs = []

# Read each CSV file and append to dataframe
for csv_file in csv_files:
    df = pd.read_csv(csv_file, index_col = None, header = 0)
    dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dfs, axis = 0, ignore_index = True)

# Write to CSV
combined_df.to_csv('crawler/data/combined_patternsGOF.csv', index = False)
