from website.Strategy.CoR import lemmatize, lower_punc, remove_junk, remove_stop, stem, tokenize
from website.Strategy import kmeans, mbkmeans
from website.Strategy import defaultVectorizer
from pathlib import Path
import pandas as pd
import pickle
from website.Strategy.predictorClass import Predictor

def main(problem, collection):
    # Instantiate the selected preprocessors
    preprocessors = [lower_punc.LowerPunc(), remove_stop.RemoveStop(), remove_junk.RemoveJunk(), stem.Stem(), tokenize.Tokenize(), lemmatize.Lemmatize()]
    
    # Get what clusterer to use
    path1 = f"models/{collection}KMeans.pkl"
    check1 = Path(__file__).parent / path1
    path2 = f"models/{collection}MBKMeans.pkl"
    check2 = Path(__file__).parent / path2
    
    if check1.is_file():
        c = kmeans.KMeansClusterer(3)
        filepath = Path(__file__).parent / path1
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    elif check2.is_file():
        c = mbkmeans.MBKMeansClusterer(3)
        filepath = Path(__file__).parent / path2
        with open(filepath, 'rb') as model_file:
            loaded_cls = pickle.load(model_file)
    
    # Instantiate the vectorizer
    vectorizer = defaultVectorizer.defaultVectorizer()

    # Load vectorizer
    path = f"vectorizers/{collection}.pkl"
    filepath = Path(__file__).parent / path
    with open(filepath, 'rb') as vec_file:
        loaded_vec = pickle.load(vec_file)
    
    # Get what collection csv to use
    path = "source_files/MasterSource.csv"
    filepath = Path(__file__).parent / path
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description']) 

    p = Predictor(preprocessors, vectorizer, c)
    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(p.preprocess_data)
    problem = p.preprocess_data(problem)
    results = p.predict(problem, df, loaded_cls, loaded_vec)
    
    return results
