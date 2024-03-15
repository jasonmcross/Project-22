from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
import defaultVectorizer, ngramVectorizer
from pathlib import Path
import pandas as pd
import pickle

from predictorClass import Predictor


def main():
    preprocess = ["1", "1", "1", "1", "1", "1", "1", "1"]
    vector = "1"
    clusterer = "1"
    problem = "Test problem for creating a website."

    # Instantiate the selected preprocessors
    preprocessors = [remove_junk(), stem(), tokenize(), lemmatize(), extract_nouns(), extract_verbs(), extract_adjectives(), synonymize()]
    pp_user = [lower_punc(), remove_stop()]
    
    # Load data
    filepath = Path(__file__).parent / "source_files/rawGOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])    
    
    # Collect user input for selected preprocessors
    for i, value in enumerate(preprocess):
        if value == "1":
            pp_user.append(preprocessors[i])       

    # Instantiate the selected vectorizer
    if vector == "1":
        v = defaultVectorizer()
    elif vector == "2":
        v = ngramVectorizer()        

    # Instantiate the selected clusterer
    if clusterer == "1":
        c = kmeans()
    elif clusterer == "2":
        c = mbkmeans()
    elif clusterer == "3":
        c = agglomerative()
    elif clusterer == "4":
        c = dbscan()
    elif clusterer == "5":
        c = spectral()
    elif clusterer == "6":
        c = meanShift()
    elif clusterer == "7":
        c = gaussianMixture()
    elif clusterer == "8":
        c = fuzzyCmean()
    
    # Load vectorizer
    if vector == "1":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_default.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    elif vector == "2":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_ngram.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    
    # Load model
    if clusterer == "1":
        filepath = Path(__file__).parent / "models/kmeans_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == "2":
        filepath = Path(__file__).parent / "models/mbkmeans_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == "3":
        filepath = Path(__file__).parent / "models/agglomerative_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == "4":
        filepath = Path(__file__).parent / "models/dbscan_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == "5":
        filepath = Path(__file__).parent / "models/spectral_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == "6":
        filepath = Path(__file__).parent / "models/mean_shift_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == "7":
        filepath = Path(__file__).parent / "models/gaussion_mixture_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == "8":
        filepath = Path(__file__).parent / "models/fuzzy_cmean_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)

    predictor = Predictor(preprocessors, v, c)

    df = predictor.preprocess_data(df)
    features = predictor.vectorize_data(df)
    predictor.cluster_data(features)


    problem = predictor.preprocess_data(problem)
    problem = predictor.vectorize_data(problem)
  
    results = predictor.predict(problem, df, loaded_cls, loaded_vec)
    
    print(results)
