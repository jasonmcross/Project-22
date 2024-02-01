import pickle
import numpy as np 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MeanShift
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path

centroids = None

def trainIt():
    global centroids
    filepath = Path(__file__).parent / "combinedGOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    print("Running clustering...")

    #vec = TfidfVectorizer(ngram_range=(1, 2))
    vec = TfidfVectorizer()
    vec.fit(df.Description.values)
    features = vec.transform(df.Description.values)

#########################################
#                                       #
#           MiniBatchKMeans             #
#                                       #
#########################################
    #cls = MiniBatchKMeans(n_clusters=3, random_state = 0)
    #cls.fit(features)
    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #reduced_cluster_centers = pca.transform(cls.cluster_centers_)
    #
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    #plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    #plt.title("MiniBatchKMeans")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()

#########################################
#                                       #
#                KMeans                 #
#                                       #
#########################################
    #cls = KMeans(n_clusters=3, random_state = 0)
    #cls.fit(features)
    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #reduced_cluster_centers = pca.transform(cls.cluster_centers_)
    #
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    #plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    #plt.title("KMeans")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()

#########################################
#                                       #
#        AgglomerativeClustering        #
#                                       #
#########################################
    cls = AgglomerativeClustering(n_clusters=3)
    cls.fit(features.toarray())
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())

    # Calculate centroids
    centroids = np.zeros((cls.n_clusters_, features.shape[1]))
    for cluster in range(cls.n_clusters_):
        cluster_indices = np.where(cls.labels_ == cluster)[0]
        cluster_points = features[cluster_indices]
        centroids[cluster] = cluster_points.mean(axis=0)

    # Make centroids available for import
    def get_centroids():
        return centroids
        
    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    plt.title("AgglomerativeClustering")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

#########################################
#                                       #
#               DBSCAN                  #
#                                       #
#########################################
    #cls = DBSCAN(eps=0.5, min_samples=5)
    #cls.fit(features)

    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #    
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    #plt.title("DBSCAN")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()

#########################################
#                                       #
#          SpectralClustering           #
#                                       #
#########################################
    #cls = SpectralClustering(n_clusters=3, affinity='nearest_neighbors')
    #cls.fit(features)
#
    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #    
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    #plt.title("SpectralClustering")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()

#########################################
#                                       #
#               MeanShift               #
#                                       #
#########################################
    #cls = MeanShift()
    #cls.fit(features)

    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #reduced_cluster_centers = pca.transform(cls.cluster_centers_)
    #    
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    #plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    #plt.title("MeanShift")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()

#########################################
#                                       #
#           GaussianMixture             #
#                                       #
#########################################
    #cls = GaussianMixture(n_components=3, random_state=0)
    #cls.fit(features.toarray())

    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #    
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    #plt.title("GaussianMixture")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()



    # Save model
    filepath = Path(__file__).parent / "clustering_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(cls, model_file)

    # Save vectorizer
    filepath = Path(__file__).parent / "vectorizer.pkl"
    with open(filepath, 'wb') as vec_file:
        pickle.dump(vec, vec_file)        

# Make centroids available for import
def get_centroids():
    #print(centroids)
    return centroids