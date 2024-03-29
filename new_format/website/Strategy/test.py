from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
import defaultVectorizer, ngramVectorizer
from pathlib import Path
import pandas as pd
import pickle

from predictorClass import Predictor


def main():
    preprocess = ["1", "1", "1", "1", "1", "1", "None", "None"]
    vector = "1"
    clusterer = "2"
    problems = ['''Design a DVD market place work. The DVD
                marketplace provides DVD to its clients with three categories:
                children, normal and new. A DVD is new during some weeks, and
                after change category. The DVD price depends on the category. It is
                probable that the system evolves in order to take into account the
                horror category.''',
               '''Design a drawing editor. A design is composed of the graphics (lines, rectangles and roses), positioned at precise
                positions. Each graphic form must be modeled by a class that
                provides a method draw(): void. A rose is a complex graphic designed by a black-box class component. This component performs
                this drawing in memory, and provides access through a method
                getRose(): int that returns the address of the drawing. It is probable
                that the system evolves in order to draw circles''',
                '''Many distinct and unrelated operations need
                to be performed on node objects in a heterogeneous aggregate
                structure. You want to avoid polluting the node classes with these
                operations. And, you do not want to have to query the type of
                each node and cast the pointer to the appropriate type before
                performing the desired operation.'''
                ]
    # Instantiate the selected preprocessors
    preprocessors = [remove_junk.RemoveJunk(), stem.Stem(), tokenize.Tokenize(), lemmatize.Lemmatize(), extract_nouns.ExtractNouns(), 
                     extract_verbs.ExtractVerbs(), extract_adjectives.ExtractAdjectives(), synonymize.Synonymize()]
    pp_user = [lower_punc.LowerPunc(), remove_stop.RemoveStop()]
    
    # Load data
    filepath = Path(__file__).parent / "source_files/MasterGOF.csv"
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

    predictor = Predictor(pp_user, v, c)

    

    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(predictor.preprocess_data)
    
    features = predictor.vectorize_data(df)
    predictor.cluster_data(features)

    for i, problem in enumerate(problems):
        problem = predictor.preprocess_data(problem)
        results = predictor.predict(problem, df, loaded_cls, loaded_vec)
        print(i)
        for result in results:
            print(result)
    

if __name__ == "__main__":
    main()
