import pickle
import numpy as np 
import pandas as pd
import predicttestcopy as pt
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
#import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path
  
def trainIt():
    filepath = Path(__file__).parent / "combined_GOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    #print(df.head())

    vec = TfidfVectorizer(stop_words="english")
    vec.fit(df.Description.values)
    features = vec.transform(df.Description.values)

    cls = MiniBatchKMeans(n_clusters=3, random_state = 0)
    cls.fit(features)

    #pca = PCA(n_components=2, random_state = 0)
    #reduced_features = pca.fit_transform(features.toarray())
    #reduced_cluster_centers = pca.transform(cls.cluster_centers_)

    """ plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.title("Pattern Clusters")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show() """

    # Save model
    filepath = Path(__file__).parent / "clustering_model.pkl"
    with open(filepath, 'wb') as model_file:
        pickle.dump(cls, model_file)

    # Save vectorizer
    filepath = Path(__file__).parent / "vectorizer.pkl"
    with open(filepath, 'wb') as vec_file:
        pickle.dump(vec, vec_file)

    design_problems = [
        "Design a drawing editor. A design is composed of the graphics (lines, rectangles and roses), positioned at precise positions. Each graphic form must be modeled by a class that provides a method draw(): void. A rose is a complex graphic designed by a black-box class component. This component performs this drawing in memory, and provides access through a method getRose(): int that returns the address of the drawing. It is probable that the system evolves in order to draw circles",
        "Design a DVD market place work. The DVD marketplace provides DVD to its clients with three categories: children, normal and new. A DVD is new during some weeks, and after change category. The DVD price depends on the category. It is probable that the system evolves in order to take into account the horror category",
        "Many distinct and unrelated operations need to be performed on node objects in a heterogeneous aggregate structure. You want to avoid 'polluting00' the node classes with these operations. And, you do not want to have to query the type of each node and cast the pointer to the appropriate type before performing the desired operation"
    ]

    for problem in design_problems:
        print(pt.predictIt(problem))    

trainIt()
