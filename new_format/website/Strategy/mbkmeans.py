import pickle
from clusterer_sc import Clusterer
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from pathlib import Path

class MBKMeansClusterer(Clusterer):
    def __init__(self, num_clusters):
        super().__init__(num_clusters=num_clusters)
    
    def cluster(self, features):
        mbkm = MiniBatchKMeans(n_clusters=3, random_state = 0)
        mbkm.fit(features)
        pca = PCA(n_components=2, random_state = 0)
        reduced_features = pca.fit_transform(features.toarray())
        reduced_cluster_centers = pca.transform(mbkm.cluster_centers_)

        for cluster_label in range(3):
            cluster_points = reduced_features[mbkm.labels_ == cluster_label]
            plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster_label}')
        
        plt.scatter(reduced_features[:,0], reduced_features[:,1], c=mbkm.labels_)
        plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
        plt.legend()
        plt.title("MiniBatchKMeans")
        plt.xlabel("PCA Feature 1")
        plt.ylabel("PCA Feature 2")
        plt.show()

        filepath = Path(__file__).parent / "models/mbkmeans_model.pkl"
        with open(filepath, 'wb') as model_file:
            pickle.dump(mbkm, model_file)
        pass