from website.Strategy.CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from website.Strategy import kmeans, mbkmeans
from website.Strategy import defaultVectorizer
from pathlib import Path
import pandas as pd

from website.Strategy.predictorClass import Predictor

def main(collection, model):
    # Instantiate the preprocessors
    preprocessors = [lower_punc.LowerPunc(), remove_stop.RemoveStop(), remove_junk.RemoveJunk(), stem.Stem(), tokenize.Tokenize(), lemmatize.Lemmatize()]
    
    # Get what collection csv to use
    path = "source_files/MasterSource.csv"
    filepath = Path(__file__).parent / path
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])   
          
    v = defaultVectorizer.defaultVectorizer()        

    # Instantiate the selected clusterer
    if model == "1":
        c = kmeans.KMeansClusterer(3)
    elif model == "2":
        c = mbkmeans.MBKMeansClusterer(3)
    
    predictor = Predictor(preprocessors, v, c)

    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(predictor.preprocess_data)
    features = predictor.vectorize_data(df, collection)
    predictor.cluster_data(features, collection)
