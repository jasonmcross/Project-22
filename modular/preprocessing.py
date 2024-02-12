import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def lower_punc(data):
    # Convert to lowercase
    text = data.lower()
    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])

    return text

def remove_stop(data):
    # Remove stopwords
    text = ' '.join([word for word in data.split() if word not in stop_words])

    return text

def stem(data):
    # Stem words
    words = [ps.stem(word) for word in data.split()]
    text = ' '.join(words)

    return text

def lemma(data):
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word, pos='v') for word in data]
    text = ' '.join(lemmas)

    return text

def tokenize(data):
    # Tokenize words
    text = word_tokenize(data)

    return text

def synonymize(data):
    # Find synonyms
    synonyms = set()
    for word in data:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())

    return list(synonyms)

def extract_nouns_verbs(data):
    tokens = word_tokenize(data)
    tagged = pos_tag(tokens)
    nouns_verbs = [word for word, pos in tagged if (pos.startswith('V') or pos.startswith('N'))]

    return(list(set(nouns_verbs)))