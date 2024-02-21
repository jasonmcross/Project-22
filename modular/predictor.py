from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
import preprocessing as pp
import vectorizer as vec
import cluster_plot as cp
from pathlib import Path

def predictIt(input, data: pd.DataFrame):
    # Load model
    filepath = Path(__file__).parent / "clustering_model_master.pkl"
    with open(filepath, 'rb') as model_file:
        loaded_cls = pickle.load(model_file)

    # Load vectorizer
    filepath = Path(__file__).parent / "vectorizer_master.pkl"
    with open(filepath, 'rb') as vec_file:
        loaded_vec = pickle.load(vec_file)

    # Load data
    df = data
    
    # Vectorize input
    user_input_vectorized = loaded_vec.transform([input])

    # Predict cluster
    cluster = loaded_cls.predict(user_input_vectorized)[0]
    
    # Find patterns in cluster
    patterns = df[loaded_cls.labels_ == cluster]

    # Find similarity between input and patterns
    similarities = cosine_similarity(user_input_vectorized, loaded_vec.transform(patterns['Description'].values))

    # Find most similar pattern
    similar_index = np.argmax(similarities)
    similar_pattern = patterns.iloc[similar_index]
    

    # Return pattern
    return similar_pattern['Category'], similar_pattern['Pattern']

