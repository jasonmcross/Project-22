import csv
import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
  

df = pd.read_csv('sourcemaking.csv', encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

# Vectorizing the Description column
vec = TfidfVectorizer(stop_words="english")
X = vec.fit_transform(df.Description.values)

# Clustering
n_clusters = 3  # Adjust based on your data
cls = MiniBatchKMeans(n_clusters=n_clusters, random_state=0)
cls.fit(X)

# Top terms per cluster
print("Top terms per cluster:")
order_centroids = cls.cluster_centers_.argsort()[:, ::-1]
terms = vec.get_feature_names_out()

for i in range(n_clusters):
    print(f"Cluster {i}:")
    top_terms = [terms[ind] for ind in order_centroids[i, :10]]  # adjust number as needed
    print(", ".join(top_terms))