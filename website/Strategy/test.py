from website.Strategy.CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from website.Strategy import fuzzyCmean, kmeans, mbkmeans
from website.Strategy import defaultVectorizer
from pathlib import Path
import pandas as pd
import pickle

from website.Strategy.predictorClass import Predictor


def run_test(preprocess=["1", "1", "1", "1", "none", "none", "none", "none"], vector=1, clusterer=1, problem="This is a test problem."):
    
    # Instantiate the selected preprocessors
    preprocessors = [remove_junk.RemoveJunk(), stem.Stem(), tokenize.Tokenize(), lemmatize.Lemmatize(), extract_nouns.ExtractNouns(), 
                     extract_verbs.ExtractVerbs(), extract_adjectives.ExtractAdjectives(), synonymize.Synonymize()]
    pp_user = [lower_punc.LowerPunc(), remove_stop.RemoveStop()]
    
    # Load data
    filepath = Path(__file__).parent.parent / "source_files/masterGOF.csv" # .parent.parent = ./website
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])    
    
    

    # Collect user input for selected preprocessors
    for i, value in enumerate(preprocess):
        if value == 1:
            pp_user.append(preprocessors[i])       

    # Instantiate the selected vectorizer
    if vector == 1:
        v = defaultVectorizer.defaultVectorizer()      

    # Instantiate the selected clusterer
    if clusterer == 1:
        c = kmeans.KMeansClusterer(3)
    elif clusterer == 2:
        c = mbkmeans.MBKMeansClusterer(3)
    elif clusterer == 3:
        c = fuzzyCmean.FuzzyCMeansClusterer(3)

    predictor = Predictor(pp_user, v, c)

    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(predictor.preprocess_data)

    features = predictor.vectorize_data(df)
    predictor.cluster_data(features)

    # Load vectorizer
    if vector == 1:
        filepath = Path(__file__).parent / "../vectorizers/vectorizer_default.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    elif vector == 2:
        filepath = Path(__file__).parent / "../vectorizers/vectorizer_ngram.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    
    # Load model
    if clusterer == 1:
        filepath = Path(__file__).parent / "../models/kmeans_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == 2:
        filepath = Path(__file__).parent / "../models/mbkmeans_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif clusterer == 3:
        filepath = Path(__file__).parent / "../models/fuzzycmeans_model.pkl"
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)

    
    problem = predictor.preprocess_data(problem)
    results = predictor.predictTest(problem, df, loaded_cls, loaded_vec)
    
    return(results)
