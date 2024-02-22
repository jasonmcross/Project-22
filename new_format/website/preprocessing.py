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
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

junk_words = ["imagine", "pattern", "design", "patterns", "also", "like", "code", "let", "used", "use", "app", "fun", "may", "problem", "client", "often", "later", "however", "got", 
              "given",  "need", "object", "objects", "class", "classes"]

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

def remove_junk(data):
    # Remove junk words
    text = ' '.join([word for word in data.split() if word not in junk_words])

    return text

def lemma(data):
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word, pos='v') for word in data]
    text = ''.join(lemmas)

    return text

def tokenize(data):
    # Tokenize words
    tok = word_tokenize(data)
    text = ' '.join(tok)

    return text

def synonymize(data):
    # Find synonyms
    synonyms = set()
    for word in data:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
    text = ' '.join(synonyms)
    text = data + ' ' + text

    return text

def extract_nouns(data):
    tokens = word_tokenize(data)
    tagged = pos_tag(tokens)
    nouns = [word for word, pos in tagged if (pos.startswith('N'))]

    text = ' '.join(nouns)
    text = data + ' ' + text

    return text

def extract_verbs(data):
    tokens = word_tokenize(data)
    tagged = pos_tag(tokens)
    verbs = [word for word, pos in tagged if (pos.startswith('V'))]

    text = ' '.join(verbs)
    text = data + ' ' + text

    return text

def extract_adj(data):
    tokens = word_tokenize(data)
    tagged = pos_tag(tokens)
    adjs = [word for word, pos in tagged if (pos.startswith('J'))]

    text = ' '.join(adjs)
    text = data + ' ' + text

    return text