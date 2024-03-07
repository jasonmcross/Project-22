from clusterer_sc import Clusterer
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

class KMeansClusterer(Clusterer):
    def __init__(self, num_clusters):
        super().__init__(num_clusters=num_clusters)
    
    def cluster(self, df: pd.DataFrame, features):
        km = KMeans(n_clusters=3, random_state = 0, algorithm='elkan')
        km.fit(features)
        pca = PCA(n_components=2, random_state = 0)
        reduced_features = pca.fit_transform(features.toarray())
        pass
