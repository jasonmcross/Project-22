import pickle
import numpy as np 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MeanShift
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import estimate_bandwidth
from sklearn.mixture import GaussianMixture
from fcmeans import FCM
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path

centroids = None

def trainIt():
    global centroids
    filepath = Path(__file__).parent / "masterGOF.csv"
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
    cls = MiniBatchKMeans(n_clusters=3, random_state = 0)
    cls.fit(features)
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())
    reduced_cluster_centers = pca.transform(cls.cluster_centers_)
    
    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.title("MiniBatchKMeans")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

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
    #cls = AgglomerativeClustering(n_clusters=3)
    #cls.fit(features.toarray())
    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
#
    ## Calculate centroids
    #centroids = np.zeros((cls.n_clusters_, features.shape[1]))
    #for cluster in range(cls.n_clusters_):
    #    cluster_indices = np.where(cls.labels_ == cluster)[0]
    #    cluster_points = features[cluster_indices]
    #    centroids[cluster] = cluster_points.mean(axis=0)
    #        
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    #plt.title("AgglomerativeClustering")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()

#########################################
#                                       #
#               DBSCAN                  #
#                                       #
#########################################
    #min_samples = 5
#
    #neighbors = NearestNeighbors(n_neighbors=min_samples)
    #neighbors_fit = neighbors.fit(features)  # 'features' is your dataset
    #distances, indices = neighbors_fit.kneighbors(features)
#
    ## Sort distance values
    #distances = np.sort(distances[:, min_samples-1], axis=0)
#
    #plt.figure(figsize=(10, 5))
    #plt.plot(distances)
    #plt.xlabel('Points')
    #plt.ylabel(f'Distance to {min_samples}th nearest neighbor')
    #plt.title('K-Nearest Neighbors Distance')
    #plt.show()

    #cls = DBSCAN(eps=1.1, min_samples=5)
    #cls.fit(features)
    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #    
    #plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=cls.labels_, cmap='Paired', label='Clustered Points')
    ## Plot noise points in red
    #plt.scatter(reduced_features[cls.labels_ == -1, 0], reduced_features[cls.labels_ == -1, 1], color='red', label='Noise Points')
    #plt.title("DBSCAN")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.legend()
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
    #bandwidth = estimate_bandwidth(features.toarray(), quantile=0.025)
    #cls = MeanShift(bandwidth=bandwidth)
    #cls.fit(features.toarray())
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
    #labels = cls.predict(features.toarray())
    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #    
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=labels, cmap='viridis')
    #plt.title("GaussianMixture")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.colorbar(label='Cluster Label')
    #plt.show()

#########################################
#                                       #
#            Fuzzy C-Mean               #
#                                       #
#########################################
    ## Initialize and fit the FCM model
    #cls = FCM(n_clusters=3)
    #cls.fit(features.toarray()) 
#
    ## Get the predicted cluster memberships for each data point
    #fcm_labels = cls.u.argmax(axis=1)
#
    ## Apply PCA to reduce dimensions for visualization
    #pca = PCA(n_components=2)
    #reduced_features = pca.fit_transform(features.toarray())
#
    ## Cluster centers in the original feature space
    #fcm_centers = cls.centers
#
    ## Transform cluster centers to the reduced feature space
    #reduced_centers = pca.transform(fcm_centers)
#
    ## Plot the clustered data points
    #plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=fcm_labels, alpha=0.5)
#
    ## Plot the cluster centers
    #plt.scatter(reduced_centers[:, 0], reduced_centers[:, 1], marker='x', s=200, c='black')
#
    #plt.title("Fuzzy C-Means")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()



    # Save model
    filepath = Path(__file__).parent / "clustering_model_master.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(cls, model_file)

    # Save vectorizer
    filepath = Path(__file__).parent / "vectorizer_master.pkl"
    with open(filepath, 'wb') as vec_file:
        pickle.dump(vec, vec_file)        

# Make centroids available for import
#def get_centroids():
#    #print(centroids)
#    return centroids