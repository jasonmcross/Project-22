import pickle
import numpy as np 
import pandas as pd
import predicttestcopy as pt
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
from sklearn.cluster import MiniBatchKMeans
#import appendGOF_lemm
#import os
#import nltk
#from nltk.corpus import wordnet, stopwords
#from nltk.stem import WordNetLemmatizer
#import string
#from nltk.tokenize import word_tokenize
#from nltk.tag import pos_tag
#
#df1 = pd.read_csv(os.path.abspath(os.path.join('..', 'crawler', 'data', 'refactoringGOF.csv')), header = None)
#df2 = pd.read_csv(os.path.abspath(os.path.join('..', 'crawler', 'data', 'sourcemakingGOF.csv')), header = None)
#
#nltk.download('wordnet')
#nltk.download('stopwords')
#nltk.download('punkt')
#stop_words = set(stopwords.words('english'))
#nltk.download('averaged_perceptron_tagger')  # For part-of-speech tagging
#
#lemmatizer = WordNetLemmatizer()
#
#def get_wordnet_pos(word):
#    """Map POS tag to first character lemmatize() accepts"""
#    tag = nltk.pos_tag([word])[0][1][0].upper()
#    tag_dict = {"J": wordnet.ADJ,
#                "N": wordnet.NOUN,
#                "V": wordnet.VERB,
#                "R": wordnet.ADV}
#    
#    return wordnet.VERB if tag == "V" else None
#
#def extract_verbs(text):
#    tokens = nltk.word_tokenize(text)
#    tagged_tokens = nltk.pos_tag(tokens)
#    verbs = [token for token, pos in tagged_tokens if pos.startswith('VB')]
#    return ' '.join(verbs)
#
#def preprocessText(texts):
#    texts = texts.lower()
#    texts = ''.join([char for char in texts if char not in string.punctuation])
#    lemmatizer = WordNetLemmatizer()
#    
#    processed_texts = []
#    for text in texts:
#        tokens = word_tokenize(text)
#        tagged_tokens = pos_tag(tokens)
#        verbs = [lemmatizer.lemmatize(token, pos='v') for token, pos in tagged_tokens if pos.startswith('VB')]
#        processed_texts.append(' '.join(verbs))
#    return processed_texts
#    #words = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text) if w not in stop_words]
#    #return ' '.join(words)
#
## Apply preprocessing to 3rd column of files
#df1.iloc[:, 2] = df1.iloc[:,2].astype(str).apply(preprocessText)
#df2.iloc[:, 2] = df2.iloc[:,2].astype(str).apply(preprocessText)
#
## Concatenate dataframes
#df_combined = pd.concat([df1, df2], ignore_index=True)

def trainIt():
    df = pd.read_csv('combinedGOF_lemm.csv', encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    #print(#df.head())
                   

    vec = TfidfVectorizer(stop_words="english")
    #vec.fit(df.Description.values)
    #features = vec.transform(df.Description.values)
    tfidf_matrix = vec.fit_transform(df.Description.values)

    cls = KMeans(n_clusters=3, random_state = 0)
    cls.fit(tfidf_matrix)

    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(tfidf_matrix.toarray())
    reduced_cluster_centers = pca.transform(cls.cluster_centers_)

    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.labels_)
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.title("Pattern Clusters")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show() 

    # Save model
    with open('clustering_model.pkl', 'wb') as model_file:
        pickle.dump(cls, model_file)

    # Save vectorizer
    with open('vectorizer.pkl', 'wb') as vec_file:
        pickle.dump(vec, vec_file)

    design_problems = [
        "Design a drawing editor. A design is composed of te graphics (lines, rectangles and roses), positioned at precise positions. Each graphic form must be modeled by a class that provides a method draw(): void. A rose is a complex graphic designed by a black-box class component. This component performs this drawing in memory, and provides access through a method getRose(): int that returns the address of the drawing. It is probable that the system evolves in order to draw circles",
        "Design a DVD market place work. The DVD marketplace provides DVD to its clients with three categories: children, normal and new. A DVD is new during some weeks, and after change category. The DVD price depends on the category. It is probable that the system evolves in order to take into account the horror category",
        "Many distinct and unrelated operations need to be performed on node objects in a heterogeneous aggregate structure. You want to avoid 'polluting00' the node classes with these operations. And, you do not want to have to query the type of each node and cast the pointer to the appropriate type before performing the desired operation"
    ]

    for problem in design_problems:
        print(pt.predictIt(problem))    

trainIt()