import pickle
from clusterer_sc import Clusterer
import pandas as pd
import matplotlib.pyplot as plt 
from fcmeans import FCM
from sklearn.decomposition import PCA
from pathlib import Path
#import numpy as np
from scipy.sparse import spmatrix

class FuzzyCMeansClusterer(Clusterer):
    def __init__(self, num_clusters):
        super().__init__(num_clusters=num_clusters)
    
    def cluster(self, features):
        fcm = FCM(n_clusters=3)
        fcm.fit(features.toarray())
        pca = PCA(n_components=2, random_state = 0)
        reduced_features = pca.fit_transform(features.toarray())
        reduced_cluster_centers = pca.transform(fcm.centers)
        
        #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=fcm.predict(features))
        #plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
        #plt.legend()
        #plt.title("Fuzzy CMeans")
        #plt.xlabel("PCA Feature 1")
        #plt.ylabel("PCA Feature 2")
        ##plt.show()

        filepath = Path(__file__).parent.parent / "models/fuzzycmeans_model.pkl"
        with open(filepath, 'wb') as model_file:
            pickle.dump(fcm, model_file)
        pass