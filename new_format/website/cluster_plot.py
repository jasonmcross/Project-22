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


#########################################
#                                       #
#                KMeans                 #
#                                       #
#########################################
def kmeans(features, df: pd.DataFrame):
    km = KMeans(n_clusters=3, random_state = 0, algorithm='elkan')
    km.fit(features)
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())
    reduced_cluster_centers = pca.transform(km.cluster_centers_)

    for cluster_label in range(3):
        cluster_points = reduced_features[km.labels_ == cluster_label]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster_label}')
    
    #plt.scatter(reduced_features[:,0], reduced_features[:,1], c=km.labels_)
    #plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    #plt.legend()
    #plt.title("KMeans")
    #plt.xlabel("PCA Feature 1")
    #plt.ylabel("PCA Feature 2")
    #plt.show()

    df['cluster'] = km.labels_
    df.to_csv('masterGOF_junk.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/kmeans_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(km, model_file)


#########################################
#                                       #
#           MiniBatchKMeans             #
#                                       #
#########################################
def mbkmeans(features, df: pd.DataFrame):
    mbkm = MiniBatchKMeans(n_clusters=3, random_state = 0)
    mbkm.fit(features)
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())
    reduced_cluster_centers = pca.transform(mbkm.cluster_centers_)
    
    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=mbkm.labels_)
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.title("MiniBatchKMeans")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

    df['cluster'] = mbkm.labels_
    df.to_csv('mbkmeans.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/mbkmeans_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(mbkm, model_file)

#########################################
#                                       #
#        AgglomerativeClustering        #
#                                       #
#########################################
def agglomerative(features, df: pd.DataFrame):
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
    plt.show()

    df['cluster'] = ac.labels_
    df.to_csv('agglomerative.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/agglomerative_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(ac, model_file)

#########################################
#                                       #
#               DBSCAN                  #
#                                       #
#########################################
def dbscan(features, df: pd.DataFrame):
    dbs = DBSCAN(eps=0.5, min_samples=5)
    dbs.fit(features.toarray())
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())

    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=dbs.labels_)
    plt.title("DBSCAN")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

    df['cluster'] = dbs.labels_
    df.to_csv('dbscan.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/dbscan_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(dbs, model_file)

#########################################
#                                       #
#          SpectralClustering           #
#                                       #
#########################################
def spectral(features, df: pd.DataFrame):
    sc = SpectralClustering(n_clusters=3)
    sc.fit(features.toarray())
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())

    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=sc.labels_)
    plt.title("SpectralClustering")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

    df['cluster'] = sc.labels_
    df.to_csv('spectral.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/spectral_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(sc, model_file)

#########################################
#                                       #
#               MeanShift               #
#                                       #
#########################################
def mean_shift(features, df: pd.DataFrame):
    bandwidth = estimate_bandwidth(features.toarray(), quantile=0.2, n_samples=500)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(features.toarray())
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())

    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=ms.labels_)
    plt.title("MeanShift")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

    df['cluster'] = ms.labels_
    df.to_csv('mean_shift.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/mean_shift_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(ms, model_file)

#########################################
#                                       #
#           GaussianMixture             #
#                                       #
#########################################
def gaussian_mixture(features, df: pd.DataFrame):
    gm = GaussianMixture(n_components=3, random_state=0)
    gm.fit(features.toarray())
    labels = gm.predict(features.toarray())
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())

    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=labels, cmap='viridis')
    plt.title("GaussianMixture")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.colorbar(label='Cluster Label')
    plt.show()

    df['cluster'] = labels
    df.to_csv('gaussian_mixture.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/gaussian_mixture_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(gm, model_file)

#########################################
#                                       #
#            Fuzzy C-Mean               #
#                                       #
#########################################
def fuzzy_cmean(features, df: pd.DataFrame):
    fcm = FCM(n_clusters=3)
    fcm.fit(features.toarray())
    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(features.toarray())

    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=fcm.u.argmax(axis=1))
    plt.title("Fuzzy C-Mean")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

    df['cluster'] = fcm.u.argmax(axis=1)
    df.to_csv('fuzzy_cmean.csv', index=False, header=False, mode='w', encoding='utf-8')

    filepath = Path(__file__).parent / "models/fuzzy_cmean_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(fcm, model_file)