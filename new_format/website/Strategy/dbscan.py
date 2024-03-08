import pickle
from clusterer_sc import Clusterer
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from pathlib import Path

class DBSCAN(Clusterer):
    def __init__(self, num_clusters):
        super().__init__(num_clusters=num_clusters)
        
    def cluster(self, features):
        dbs = DBSCAN(eps=0.5, min_samples=5)
        dbs.fit(features.toarray())
        pca = PCA(n_components=2, random_state = 0)
        reduced_features = pca.fit_transform(features.toarray())

        plt.scatter(reduced_features[:,0], reduced_features[:,1], c=dbs.labels_)
        plt.title("DBSCAN")
        plt.xlabel("PCA Feature 1")
        plt.ylabel("PCA Feature 2")
        plt.show()

        filepath = Path(__file__).parent / "models/dbscan_model.pkl"
        with open(filepath, 'wb') as model_file:
            pickle.dump(dbs, model_file)

        pass