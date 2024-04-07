from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
import defaultVectorizer, ngramVectorizer
from pathlib import Path
import pandas as pd
import pickle

from predictorClass import Predictor


def main():
    preprocess = ["1", "1", "1", "1", "none", "none", "none", "none"]
    vector = "1"
    clusterer = "1"
    
    filepath = Path(__file__).parent / "dpTest.csv"
    problems = pd.read_csv(filepath, encoding='ISO-8859-1', header=None, names=['#', 'source', 'Descripition', 'Expected Answer', 'cat', 'results', 'score'])
    total_questions = len(problems)
    
    # Instantiate the selected preprocessors
    preprocessors = [remove_junk.RemoveJunk(), stem.Stem(), tokenize.Tokenize(), lemmatize.Lemmatize(), extract_nouns.ExtractNouns(), 
                     extract_verbs.ExtractVerbs(), extract_adjectives.ExtractAdjectives(), synonymize.Synonymize()]
    pp_user = [lower_punc.LowerPunc(), remove_stop.RemoveStop()]
    
    # Load data
    filepath = Path(__file__).parent / "source_files/masterGOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])    
    
    

    # Collect user input for selected preprocessors
    for i, value in enumerate(preprocess):
        if value == "1":
            pp_user.append(preprocessors[i])       

    # Instantiate the selected vectorizer
    if vector == "1":
        v = defaultVectorizer.defaultVectorizer()
    elif vector == "2":
        v = ngramVectorizer.ngramVectorizer()        

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

    predictor = Predictor(pp_user, v, c)

    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(predictor.preprocess_data)

    features = predictor.vectorize_data(df)
    predictor.cluster_data(features)

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

    total = 0
    for i in range(1, total_questions):
        problem = predictor.preprocess_data(problems['Descripition'][i])
        results = predictor.predict(problem, df, loaded_cls, loaded_vec)
        
        print(problems['Expected Answer'][i], " to ", results)
        if problems['Expected Answer'][i] == results:
            total += 1
    
    print(total, "/", total_questions)

if __name__ == "__main__":
    main()

