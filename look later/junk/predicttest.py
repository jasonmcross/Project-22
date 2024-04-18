from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
from pathlib import Path

def predictIt(input, collection):
    # Load model
    filepath = Path(__file__).parent / "crawler_cleanup/clustering_model.pkl"
    with open(filepath, 'rb') as model_file:
        loaded_cls = pickle.load(model_file)

    # Load vectorizer
    filepath = Path(__file__).parent / "crawler_cleanup/vectorizer.pkl"
    with open(filepath, 'rb') as vec_file:
        loaded_vec = pickle.load(vec_file)

    # User selected Gang of Four collection
    if collection == 2:
        filepath = Path(__file__).parent / "crawler_cleanup/combined_GOF.csv"
    # User selected All collections
    else:
        filepath = Path(__file__).parent / "crawler_cleanup/combined_GOF.csv"
    
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    # Vectorize input
    user_input_vectorized = loaded_vec.transform([input])

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

    # Return three most similar patterns
    return output, output1, output2
