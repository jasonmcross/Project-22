import pickle
import numpy as np 
import pandas as pd
import predicttest as pt
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
  

df = pd.read_csv('sourcemaking.csv', encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

print(df.head())

vec = TfidfVectorizer(stop_words="english")
vec.fit(df.Description.values)
features = vec.transform(df.Description.values)

cls = MiniBatchKMeans(n_clusters=3, random_state = 0)
cls.fit(features)

pca = PCA(n_components=2, random_state = 0)
reduced_features = pca.fit_transform(features.toarray())
reduced_cluster_centers = pca.transform(cls.cluster_centers_)

""" plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
plt.title("Pattern Clusters")
plt.xlabel("PCA Feature 1")
plt.ylabel("PCA Feature 2")
plt.show() """

# Save model
with open('clustering_model.pkl', 'wb') as model_file:
    pickle.dump(cls, model_file)

# Save vectorizer
with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vec, vec_file)

print(pt.predictIt('I want to create a new object', df))