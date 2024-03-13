from predictorClass import Predictor
from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from Strategy import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
from Strategy import defaultVectorizer, ngramVectorizer
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle

def main(collection, vector, clusterer, preprocess):
    # Instantiate the selected preprocessors
    preprocessors = [remove_junk(), stem(), tokenize(), lemmatize(), extract_nouns(), extract_verbs(), extract_adjectives(), synonymize()]
    pp_user = [lower_punc(), remove_stop()]
    
    # Load data
    if collection == "1" or collection == "2":
        filepath = Path(__file__).parent / "source_files/masterGOF.csv"
        df = pd.read_csv(filepath, encoding='ISO-8859-1',
                       header=None, names=['Category', 'Pattern', 'Description'])    
    
    # Collect user input for selected preprocessors
    for i, value in enumerate(preprocess):
        if value == "1":
            pp_user.append(preprocessors[i])

    # Preprocess data
    for preprocessor in pp_user:
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(preprocessor)        

    # Instantiate the selected vectorizer
    if vector == "1":
        vectorizer = defaultVectorizer()
    elif vector == "2":
        vectorizer = ngramVectorizer()    

    # Instantiate the selected clusterer
    if clusterer == "1":
        clusterer = kmeans()
    elif clusterer == "2":
        clusterer = mbkmeans()
    elif clusterer == "3":
        clusterer = agglomerative()
    elif clusterer == "4":
        clusterer = dbscan()
    elif clusterer == "5":
        clusterer = spectral()
    elif clusterer == "6":
        clusterer = meanShift()
    elif clusterer == "7":
        clusterer = gaussianMixture()
    elif clusterer == "8":
        clusterer = fuzzyCmean()    

    # Create the Predictor instance with the selected strategies
    predictor = Predictor(preprocessors=preprocessors, vectorizer=vectorizer, clusterer=clusterer)   

    

if __name__ == "__main__":
    main()