import pandas as pd
from collections import Counter
from functools import reduce
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

file1 = pd.read_csv('C:/VSCode/Project-22/crawler/data/refactoringGOF.csv', encoding='latin1', header=None, names=['Category', 'Pattern', 'Description'])
file2 = pd.read_csv('C:/VSCode/Project-22/crawler/data/sourcemakingGOF.csv', encoding='latin1', header=None, names=['Category', 'Pattern', 'Description'])

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# Combine dataframes
merged_df = pd.merge(file1, file2, on=['Category', 'Pattern'], how='inner')

def intersect_descriptions(desc1, desc2):
    words1 = set(desc1.split())
    words2 = set(desc2.split())
    common_words = words1.intersection(words2)
    return ' '.join(common_words)

merged_df['Description'] = merged_df.apply(lambda row: intersect_descriptions(row['Description_x'], row['Description_y']), axis=1)

merged_df = merged_df.drop(columns=['Description_x', 'Description_y'])

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
merged_df.iloc[:, 2] = merged_df.iloc[:,2].astype(str).apply(preprocessText)

# Write to CSV
merged_df.to_csv('C:/VSCode/Project-22/crawler_cleanup/merged_intersected_cleaned.csv', index=False, header = False)