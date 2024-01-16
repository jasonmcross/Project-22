import csv
import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
  
# Dataset link:  
# https://github.com/PawanKrGunjan/Natural-Language-Processing/blob/main/Sarcasm%20Detection/sarcasm.json 
df = pd.read_csv('sourcemaking.csv', encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

random_state = 0 

print(df.head())

vec = TfidfVectorizer(stop_words="english")
vec.fit(df.Pattern.values)
features = vec.transform(df.Pattern.values)

cls = MiniBatchKMeans(n_clusters=3, random_state=random_state)
cls.fit(features)

cls.predict(features)

cls.labels_

pca = PCA(n_components=2, random_state=random_state)
reduced_features = pca.fit_transform(features.toarray())

reduced_cluster_centers = pca.transform(cls.cluster_centers_)

plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(features))
plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
plt.show()