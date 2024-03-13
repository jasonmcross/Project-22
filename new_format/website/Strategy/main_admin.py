from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from Strategy import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
from Strategy import defaultVectorizer, ngramVectorizer
from pathlib import Path
import pandas as pd


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
    
    for i, value in enumerate(preprocess):        
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp_user[i])        

    # Instantiate the selected vectorizer
    if vector == "1":
        features = defaultVectorizer()
    elif vector == "2":
        features = ngramVectorizer()        

    # Instantiate the selected clusterer
    if clusterer == "1":
        kmeans(features)
    elif clusterer == "2":
        mbkmeans(features)
    elif clusterer == "3":
        agglomerative(features)
    elif clusterer == "4":
        dbscan(features)
    elif clusterer == "5":
        spectral(features)
    elif clusterer == "6":
        meanShift(features)
    elif clusterer == "7":
        gaussianMixture(features)
    elif clusterer == "8":
        fuzzyCmean(features)
    

if __name__ == "__main__":
    main()