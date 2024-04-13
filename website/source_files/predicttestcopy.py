from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import clusteringcopy as clu
import pandas as pd
import numpy as np
import pickle
from pathlib import Path

def predictIt(input):
    # Load model
    filepath = Path(__file__).parent / "clustering_model_master.pkl"
    with open(filepath, 'rb') as model_file:
        loaded_cls = pickle.load(model_file)

    # Load vectorizer
    filepath = Path(__file__).parent / "vectorizer_master.pkl"
    with open(filepath, 'rb') as vec_file:
        loaded_vec = pickle.load(vec_file)
        
    filepath = Path(__file__).parent / "masterGOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    # Vectorize input
    user_input_vectorized = loaded_vec.transform([input])

    #########################################
    #                                       #
    #        MiniBatchKMeans/KMeans         #
    #                                       #
    #########################################

    # Predict cluster
    cluster = loaded_cls.predict(user_input_vectorized)[0]

    #########################################
    #                                       #
    #        AgglomerativeClustering        #
    #                                       #
    #########################################

    ## Get centroids
    #centroids = clu.get_centroids()
#
    ## Find patterns in cluster
    #distances = euclidean_distances(user_input_vectorized, centroids)
    #cluster = np.argmin(distances, axis=1)[0]

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

    #cluster = loaded_cls.predict(user_input_vectorized.toarray())[0]
#
    #all_descriptions_vectorized = loaded_vec.transform(df['Description'].values)
    #similarities = cosine_similarity(user_input_vectorized, all_descriptions_vectorized)
#
    #similar_index = np.argmax(similarities)
    #similar_pattern = df.iloc[similar_index]

    #########################################
    #                                       #
    #            Fuzzy C-Mean               #
    #                                       #
    #########################################

    ## Calculate membership values for the new data point
    #new_data_memberships = loaded_cls.predict(user_input_vectorized.toarray())
#
    ## Determine the most likely cluster (highest membership value)
    ##cluster = np.argmax(new_data_memberships, axis=1)[0]
    #cluster = np.argmax(new_data_memberships)
#
    ## If you need the actual membership values
    ##membership_values = new_data_memberships[0]

    
    
    
    # Find patterns in cluster
    patterns = df[loaded_cls.labels_ == cluster]

    # Find similarity between input and patterns
    similarities = cosine_similarity(user_input_vectorized, loaded_vec.transform(patterns['Description'].values))

    # Find most similar pattern
    similar_index = np.argmax(similarities)
    similar_pattern = patterns.iloc[similar_index]
    

    # Return pattern
    return similar_pattern['Category'], similar_pattern['Pattern']
