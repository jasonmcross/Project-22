import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

def vectorize_default(df: pd.DataFrame):    
    vec = TfidfVectorizer()
    vec.fit(df.Description.values)
    features = vec.transform(df.Description.values)

    # Save vectorizer
    filepath = Path(__file__).parent / "vectorizer_default.pkl"
    with open(filepath, 'wb') as vec_file:
        pickle.dump(vec, vec_file)

    return features

def vectorize_ngram(df: pd.DataFrame):
    vec = TfidfVectorizer(ngram_range=(2, 3))
    vec.fit(df.Description.values)
    features = vec.transform(df.Description.values)

    # Save vectorizer
    filepath = Path(__file__).parent / "vectorizer_ngram.pkl"
    with open(filepath, 'wb') as vec_file:
        pickle.dump(vec, vec_file)

    return features