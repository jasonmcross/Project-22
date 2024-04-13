from sklearn.metrics.pairwise import cosine_similarity
import clustering as cl
import pandas as pd
import numpy as np
import pickle

def predictIt(input):
    # Load model
    with open('clustering_model.pkl', 'rb') as model_file:
        loaded_cls = pickle.load(model_file)

    # Load vectorizer
    with open('vectorizer.pkl', 'rb') as vec_file:
        loaded_vec = pickle.load(vec_file)

    df = pd.read_csv('sourcemaking.csv', encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

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