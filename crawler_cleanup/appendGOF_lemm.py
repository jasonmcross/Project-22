import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import string
import glob
import os
from sklearn.feature_extraction.text import TfidfVectorizer


# List of CSV files to combine
#path = 'C:/VSCodeProject-22/crawler/data/'
#csv_files = glob.glob(path + '/*GOF.csv')

#print(os.path.abspath('.'))

df1 = pd.read_csv(os.path.abspath(os.path.join('..', 'crawler', 'data', 'refactoringGOF.csv')), header = None)
df2 = pd.read_csv(os.path.abspath(os.path.join('..', 'crawler', 'data', 'sourcemakingGOF.csv')), header = None)


nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
nltk.download('averaged_perceptron_tagger')  # For part-of-speech tagging

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    
    return wordnet.VERB if tag == "V" else None

def preprocessText(text):
    #print(text)
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    text = text.replace('’', '')
    ##words = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text) if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    verbs = [lemmatizer.lemmatize(token, pos='v') for token, pos in tagged_tokens if pos.startswith('VB')]# or pos.startswith('NN')]
    return ''.join(text)

# Apply preprocessing to 3rd column of files
df1.iloc[:, 2] = df1.iloc[:,2].astype(str).apply(preprocessText)
df2.iloc[:, 2] = df2.iloc[:,2].astype(str).apply(preprocessText)

# Concatenate dataframes
df_combined = pd.concat([df1, df2], ignore_index=True)
print(df_combined)

# Write to CSV
df_combined.to_csv(os.path.abspath(os.path.join('.', 'combinedGOF_lemm.csv')), index=False, header = False)


# Combine files into one file
#with open('combinedGOF.csv', 'w', encoding = 'ISO-8859-1') as outfile:
#    for i, fname in enumerate(csv_files):
#        with open(fname) as infile:
#            if i == 0:
#                outfile.write(infile.read())
#            else:
#                next(infile)
#                outfile.write(infile.read())
