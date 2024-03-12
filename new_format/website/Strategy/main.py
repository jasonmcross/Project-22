from predictorClass import Predictor
from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from Strategy import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
from Strategy import defaultVectorizer, ngramVectorizer
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle

def main(problem, collection, source, vector, clusterer, preprocess):
    # Instantiate the selected preprocessors
    preprocessors = [remove_junk(), stem(), tokenize(), lemmatize(), extract_nouns(), extract_verbs(), extract_adjectives(), synonymize()]
    pp_user = [lower_punc(), remove_stop()]
    
    # Load data
    if collection == "1" or collection == "2":
        filepath = Path(__file__).parent / "source_files/masterGOF.csv"
        df = pd.read_csv(filepath, encoding='ISO-8859-1',
                       header=None, names=['Category', 'Pattern', 'Description'])    
    
    
    # Collect user input or read configuration    
    for i, value in enumerate(preprocess):
        if value == "1":
            pp_user.append(preprocessors[i])

    # Preprocess data
    for preprocessor in pp_user:
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(preprocessor)
        user_input = preprocessor(problem)    

    # Instantiate the selected vectorizer
    if vector == "1":
        vectorizer = defaultVectorizer()
    elif vector == "2":
        vectorizer = ngramVectorizer()

    # Load vectorizer
    if vector == "1":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_default.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    elif vector == "2":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_ngram.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)

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

    # Create the Predictor instance with the selected strategies
    predictor = Predictor(preprocessors=preprocessors, vectorizer=vectorizer, clusterer=clusterer)

    # Vectorize input
    user_input_vectorized = loaded_vec.transform([user_input])

    # Predict cluster
    cluster = loaded_cls.predict(user_input_vectorized)[0]
    
    # Find patterns in cluster
    patterns = df[loaded_cls.labels_ == cluster]

    # Find similarity between input and patterns
    similarities = cosine_similarity(user_input_vectorized, loaded_vec.transform(patterns['Description'].values))

    # Find most similar patterns
    similar_index = np.argmax(similarities)
    similar_index1 = similar_index + 1
    similar_index2 = similar_index + 2

    # Get similarity score
    similarity_score = similarities[0][similar_index]
    similarity_score1 = similarities[0][similar_index1]
    similarity_score2 = similarities[0][similar_index2]

    # Get similar patterns
    similar_pattern = patterns.iloc[similar_index]
    similar_pattern1 = patterns.iloc[similar_index1]
    similar_pattern2 = patterns.iloc[similar_index2]

    # Format output for html display including similarity scores
    output = f"{similar_pattern['Pattern']}    Category: {similar_pattern['Category']}    Similarity: {similarity_score:.2f}"
    output1 = f"{similar_pattern1['Pattern']}    Category: {similar_pattern1['Category']}    Similarity: {similarity_score1:.2f}"
    output2 = f"{similar_pattern2['Pattern']}    Category: {similar_pattern2['Category']}    Similarity: {similarity_score2:.2f}"

    # Return patterns
    return output, output1, output2

if __name__ == "__main__":
    main()