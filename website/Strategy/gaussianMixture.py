import pickle
from clusterer_sc import Clusterer
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from pathlib import Path

class GaussianMixtureClusterer(Clusterer):
    def __init__(self, num_clusters):
        super().__init__(num_clusters=num_clusters)
    
    def cluster(self, features):
        gm = GaussianMixture(n_components=3, random_state = 0)
        gm.fit(features)
        pca = PCA(n_components=2, random_state = 0)
        reduced_features = pca.fit_transform(features.toarray())
        reduced_cluster_centers = pca.transform(gm.means_)
        
        plt.scatter(reduced_features[:,0], reduced_features[:,1], c=gm.predict(features))
        plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
        plt.legend()
        plt.title("Gaussian Mixture")
        plt.xlabel("PCA Feature 1")
        plt.ylabel("PCA Feature 2")
        plt.show()

        filepath = Path(__file__).parent / "models/gaussianmixture_model.pkl"
        with open(filepath, 'wb') as model_file:
            pickle.dump(gm, model_file)
        pass