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
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.legend()
    plt.title("KMeans")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

    df['cluster'] = km.labels_
    df.to_csv('masterGOF_junk.csv', index=False, header=False, mode='w', encoding='utf-8')


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