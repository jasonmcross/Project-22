import pandas as pd
import os
import csv
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Project main directory#os.path.abspath(os.path.join(__file__, '..', '..'))

def extract_nouns_verbs(data):
    tokens = word_tokenize(data)
    tagged = pos_tag(tokens)
    nouns_verbs = [word for word, pos in tagged if pos.startswith('N') or pos.startswith('V')]
    return(nouns_verbs)

def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word, pos='v') for word in words]
    return(lemmas)

def expand_keywords(words):
    synonyms = set()
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
    return(list(synonyms))

def main():
    PATH = join_path(__file__, '..', '..')
    data = []
    file_dir = join_path(PATH, 'crawler', 'data')
    for file in os.listdir(file_dir):
        with open(join_path(file_dir, file), 'r', encoding='utf-8') as crawl_data:
            csv_reader = csv.reader(crawl_data)
            for row in csv_reader:
                description = row[2].lower()
                data.append(description)

    df_dict = {}
    df_dict['desc'] = data
    df = pd.DataFrame(df_dict)
    df['tokens'] = df['desc'].apply(word_tokenize)
    df['nouns_verbs'] = df['desc'].apply(extract_nouns_verbs)
    df['lemmas'] = df['nouns_verbs'].apply(lemmatize_words)
    df['keywords'] = df['lemmas'].apply(expand_keywords)
    keywords = set(keyword for sublist in df['keywords'] for keyword in sublist)
    vocab = {word: ind for ind, word in enumerate(keywords)}
    tfidf_vect = TfidfVectorizer(vocabulary=vocab)
    tfidf_mtrx = tfidf_vect.fit_transform(df['desc'].apply(' '.join))
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(tfidf_mtrx)
    df['cluster'] = kmeans.labels_
    print(df['cluster'])
    #print(tfidf_mtrx)
    #dense = tfidf_mtrx.toarray()
    #np.save('matrix.npy', dense)
    df.to_csv('out.csv', index=False, header=False, mode='w')

def join_path(*args):
    return(os.path.abspath(os.path.join(*args)))

if __name__ == "__main__":
    main()