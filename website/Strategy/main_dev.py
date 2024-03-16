from asyncio.windows_events import NULL
from predictorClass import Predictor
from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from Strategy import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
from Strategy import defaultVectorizer, ngramVectorizer
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle

def main(problem, collection, source, vector, clusterer, preprocess):
    
    # Access database to get what preprocessing was used and what vectorizer was used and model file path
    preprocess = NULL
    vector = NULL
    modelPath = NULL
    # Instantiate the selected preprocessors
    preprocessors = [remove_junk(), stem(), tokenize(), lemmatize(), extract_nouns(), extract_verbs(), extract_adjectives(), synonymize()]
    pp_user = [lower_punc(), remove_stop()]
        
    # Collect user input for selected preprocessors
    for i, value in enumerate(preprocess):
        if value == "1":
            pp_user.append(preprocessors[i])

    filepath = Path(__file__).parent / "models/" + modelPath
    with open(filepath, 'rb') as model_file:
        loaded_cls = pickle.load(model_file)   
    
    # Instantiate the selected vectorizer
    if vector == "1":
        vectorizer = defaultVectorizer()
    elif vector == "2":
        vectorizer = ngramVectorizer()

    # Load vectorizer
    if vector == "1":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_default.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    elif vector == "2":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_ngram.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)

    p = Predictor(preprocess, vector, NULL)
    problem = p.preprocess_data(problem)
    p.vectorize_data(problem)
    results = p.predict(problem, pd.DataFrame, loaded_cls, loaded_vec)
    
    return results
