from website.Strategy.CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from website.Strategy import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
from website.Strategy import defaultVectorizer, ngramVectorizer
from pathlib import Path
import pandas as pd

from website.Strategy.predictorClass import Predictor


def main(collection, clusterer):
    # Instantiate the preprocessors
    preprocessors = [lower_punc.LowerPunc(), remove_stop.RemoveStop(), remove_junk.RemoveJunk(), stem.Stem(), tokenize.Tokenize(), lemmatize.Lemmatize()]
    
    # Load data
    if collection == "1" or collection == "2":
        filepath = Path(__file__).parent / "source_files/rawGOF.csv"
        df = pd.read_csv(filepath, encoding='ISO-8859-1',
                       header=None, names=['Category', 'Pattern', 'Description'])    
          
    v = defaultVectorizer.defaultVectorizer()        

    # Instantiate the selected clusterer
    if clusterer == "1":
        c = kmeans.KMeansClusterer(3)
    elif clusterer == "2":
        c = mbkmeans.MBKMeansClusterer(3)
    elif clusterer == "3":
        c = agglomerative.AgglomerativeClusterer(3)
    elif clusterer == "4":
        c = dbscan.DBSCAN(3)
    elif clusterer == "5":
        c = spectral.SpectralClusterer(3)
    elif clusterer == "6":
        c = meanShift.MeanShiftClusterer(3)
    elif clusterer == "7":
        c = gaussianMixture.GaussianMixtureClusterer(3)
    elif clusterer == "8":
        c = fuzzyCmean.FuzzyCMeansClusterer(3)
    
    predictor = Predictor(preprocessors, v, c)

    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(predictor.preprocess_data)
    features = predictor.vectorize_data(df)
    predictor.cluster_data(features)
