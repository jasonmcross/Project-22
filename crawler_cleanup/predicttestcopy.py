from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import clusteringcopy as clu
import pandas as pd
import numpy as np
import pickle
from pathlib import Path

def predictIt(input):
    # Load model
    filepath = Path(__file__).parent / "clustering_model.pkl"
    with open(filepath, 'rb') as model_file:
        loaded_cls = pickle.load(model_file)

    # Load vectorizer
    filepath = Path(__file__).parent / "vectorizer.pkl"
    with open(filepath, 'rb') as vec_file:
        loaded_vec = pickle.load(vec_file)
        
    filepath = Path(__file__).parent / "combinedGOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    # Vectorize input
    user_input_vectorized = loaded_vec.transform([input])

    #########################################
    #                                       #
    #           MiniBatchKMeans             #
    #                                       #
    #########################################

    ## Predict cluster
    #cluster = loaded_cls.predict(user_input_vectorized)[0]

    #########################################
    #                                       #
    #        AgglomerativeClustering        #
    #                                       #
    #########################################

    # Get centroids
    centroids = clu.get_centroids()

    # Find patterns in cluster
    distances = euclidean_distances(user_input_vectorized, centroids)
    cluster = np.argmin(distances, axis=1)[0]

    #########################################
    #                                       #
    #               DBSCAN                  #
    #                                       #
    #########################################


    #########################################
    #                                       #
    #          SpectralClustering           #
    #                                       #
    #########################################


    #########################################
    #                                       #
    #               MeanShift               #
    #                                       #
    #########################################


    #########################################
    #                                       #
    #           GaussianMixture             #
    #                                       #
    #########################################






    # Find patterns in cluster
    patterns = df[loaded_cls.labels_ == cluster]

    # Find similarity between input and patterns
    similarities = cosine_similarity(user_input_vectorized, loaded_vec.transform(patterns['Description'].values))

    # Find most similar pattern
    similar_index = np.argmax(similarities)
    similar_pattern = patterns.iloc[similar_index]

    # Return pattern
    return similar_pattern['Category'], similar_pattern['Pattern']
