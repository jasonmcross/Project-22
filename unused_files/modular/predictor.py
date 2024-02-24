from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
import preprocessing as pp
import vectorizer as vec
import cluster_plot as cp
from pathlib import Path

def predictIt(problem, collection, source, vector, clusterer, preprocess):
    # Array of preprocessing functions
    preprocess_functions = [pp.remove_junk, pp.stem, pp.tokenize, pp.lemma, pp.extract_nouns, pp.extract_verbs, pp.extract_adj, pp.synonymize]
    
    # Load data
    if collection == "1" or collection == "2":
        filepath = Path(__file__).parent / "source_files/masterGOF.csv"
        df = pd.read_csv(filepath, encoding='ISO-8859-1',
                       header=None, names=['Category', 'Pattern', 'Description'])
    
    # Preprocess data
    for i, value in enumerate(preprocess):
        if value == "1":
            df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(preprocess_functions[i])
    
    # Vectorize data
    if vector == "1":
        features = vec.vectorize_default(df)
    elif vector == "2":
        features = vec.vectorize_ngram(df)

    # Cluster data
    if clusterer == "1":
        cp.kmeans(features, df)
    elif clusterer == "2":
        cp.mbkmeans(features, df)
    elif clusterer == "3":
        cp.agglomerative(features, df)
    elif clusterer == "4":
        cp.dbscan(features, df)
    elif clusterer == "5":
        cp.spectral(features, df)
    elif clusterer == "6":
        cp.mean_shift(features, df)
    elif clusterer == "7":
        cp.gaussion_mixture(features, df)
    elif clusterer == "8":
        cp.fuzzy_cmean(features, df)
    
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

    # Load vectorizer
    if vector == "1":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_default.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    elif vector == "2":
        filepath = Path(__file__).parent / "vectorizers/vectorizer_ngram.pkl"
        with open(filepath, 'rb') as vec_file:
            loaded_vec = pickle.load(vec_file)
    
    # Vectorize input
    user_input_vectorized = loaded_vec.transform([problem])

    # Predict cluster
    cluster = loaded_cls.predict(user_input_vectorized)[0]
    
    # Find patterns in cluster
    patterns = df[loaded_cls.labels_ == cluster]

    # Find similarity between input and patterns
    similarities = cosine_similarity(user_input_vectorized, loaded_vec.transform(patterns['Description'].values))

    # Find most similar patterns
    similar_index = np.argmax(similarities)
    similar_index1 = similar_index-1
    similar_index2 = similar_index-2
    similar_pattern = patterns.iloc[similar_index]
    similar_pattern1 = patterns.iloc[similar_index1]
    similar_pattern2 = patterns.iloc[similar_index2]

    # Format output for html display
    output = similar_pattern['Pattern'] + "    Category: " + similar_pattern['Category']
    output1 = similar_pattern1['Pattern'] + "    Category: " + similar_pattern1['Category']
    output2 = similar_pattern2['Pattern'] + "    Category: " + similar_pattern2['Category']    

    # Return patterns
    return output, output1, output2

