from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from Strategy import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
from Strategy import defaultVectorizer, ngramVectorizer
from pathlib import Path
import pandas as pd

from website.Strategy.predictorClass import Predictor


def main(collection, vector, clusterer, preprocess):
    # Instantiate the selected preprocessors
    preprocessors = [remove_junk(), stem(), tokenize(), lemmatize(), extract_nouns(), extract_verbs(), extract_adjectives(), synonymize()]
    pp_user = [lower_punc(), remove_stop()]
    
    # Load data
    if collection == "1" or collection == "2":
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
    
    predictor = Predictor(preprocessors, v, c)

    df = predictor.preprocess_data(df)
    features = predictor.vectorize_data(df)
    predictor.cluster_data(features)

if __name__ == "__main__":
    main()
