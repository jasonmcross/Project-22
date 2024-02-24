import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import glob
import os



# List of CSV files to combine
#path = 'C:/VSCodeProject-22/crawler/data/'
#csv_files = glob.glob(path + '/*GOF.csv')

df1 = pd.read_csv('C:/VSCode/Project-22/crawler/data/refactoringGOF.csv', header = None)
df2 = pd.read_csv('C:/VSCode/Project-22/crawler/data/sourcemakingGOF.csv', header = None)

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocessText(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Split, remove stopwords and stem
    words = [ps.stem(word) for word in text.split() if word not in stop_words]
    # Remove duplicate words
    words = list(set(words))
    # Join words back together
    text = ' '.join(words)

    return text

# Apply preprocessing to 3rd column of files
df1.iloc[:, 2] = df1.iloc[:,2].astype(str).apply(preprocessText)
df2.iloc[:, 2] = df2.iloc[:,2].astype(str).apply(preprocessText)

# Concatenate dataframes
df_combined = pd.concat([df1, df2], ignore_index=True)

# Write to CSV
df_combined.to_csv('C:/VSCode/Project-22/crawler_cleanup/combined_GOFNew.csv', index=False, header = False)


# Combine files into one file
#with open('combined_GOF.csv', 'w', encoding = 'ISO-8859-1') as outfile:
#    for i, fname in enumerate(csv_files):
#        with open(fname) as infile:
#            if i == 0:
#                outfile.write(infile.read())
#            else:
#                next(infile)
#                outfile.write(infile.read())
