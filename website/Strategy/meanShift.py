import pickle
from clusterer_sc import Clusterer
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.cluster import MeanShift
from sklearn.decomposition import PCA
from pathlib import Path

class MeanShiftClusterer(Clusterer):
    def __init__(self, num_clusters):
        super().__init__(num_clusters=num_clusters)
    
    def cluster(self, features):
        ms = MeanShift()
        ms.fit(features)
        pca = PCA(n_components=2, random_state = 0)
        reduced_features = pca.fit_transform(features.toarray())
        reduced_cluster_centers = pca.transform(ms.cluster_centers_)
        
        plt.scatter(reduced_features[:,0], reduced_features[:,1], c=ms.labels_)
        plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
        plt.legend()
        plt.title("MeanShift")
        plt.xlabel("PCA Feature 1")
        plt.ylabel("PCA Feature 2")
        plt.show()

        filepath = Path(__file__).parent / "models/meanshift_model.pkl"
        with open(filepath, 'wb') as model_file:
            pickle.dump(ms, model_file)
        pass