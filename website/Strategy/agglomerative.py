import pickle
from clusterer_sc import Clusterer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.datasets import make_blobs
from pathlib import Path

class AgglomerativeClusterer(Clusterer):
    def __init__(self, num_clusters):
        super().__init__(num_clusters=num_clusters)
    
    def cluster(self, features):
        ac = AgglomerativeClustering(n_clusters=3)
        ac.fit(features.toarray())
        pca = PCA(n_components=2, random_state = 0)
        reduced_features = pca.fit_transform(features.toarray())

        # Calculate centroids
        centroids = np.zeros((ac.n_clusters_, features.shape[1]))
        for cluster in range(ac.n_clusters_):
            cluster_indices = np.where(ac.labels_ == cluster)[0]
            cluster_points = features[cluster_indices]
            centroids[cluster] = cluster_points.mean(axis=0)
        
        plt.scatter(reduced_features[:,0], reduced_features[:,1], c=ac.labels_)
        plt.title("AgglomerativeClustering")
        plt.xlabel("PCA Feature 1")
        plt.ylabel("PCA Feature 2")
        ##plt.show()

        filepath = Path(__file__).parent.parent / "models/agglomerative_model.pkl"
        with open(filepath, 'wb') as model_file:
            pickle.dump(ac, model_file)
        pass

    def vectorize(self, problem, vec):
        return vec.transform([problem])

    def predict(self, features, cls):
        return cls.fit_predict(features.toarray())