from website.Strategy.CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from website.Strategy import kmeans, mbkmeans
from website.Strategy import defaultVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
from pathlib import Path

class Predictor:
    
    def __init__(self, preprocessors=None, vectorizer=None, clusterer=None):
        # A list of preprocessor instances
        self.preprocessors = preprocessors if preprocessors is not None else []
        # An instance of a Vectorizer
        self.vectorizer = vectorizer
        # An instance of a Clusterer
        self.clusterer = clusterer

    def preprocess_data(self, data):
        # Apply the chain of preprocessing steps to the data
        for preprocessor in self.preprocessors:
            data = preprocessor.preprocess(data)
        return data

    def vectorize_data(self, data, collection):
        # Vectorize the preprocessed data
        if self.vectorizer is not None:
            return self.vectorizer.vectorize(data, collection)
        else:
            raise NotImplementedError("Vectorizer has not been set.")

    def cluster_data(self, data, collection):
        # Apply the clustering algorithm to the vectorized data
        if self.clusterer is not None:
            self.clusterer.cluster(data, collection)
        else:
            raise NotImplementedError("Clusterer has not been set.")

    def predict(self, problem, data, loaded_cls, loaded_vec):
        # The main method to process and predict based on the input data
        # Vectorize input
        problem = self.clusterer.vectorize(problem, loaded_vec)# loaded_vec.transform([problem])
        # Predict cluster
        cluster = self.clusterer.predict(problem, loaded_cls)# loaded_cls.predict(problem)[0]
    
        # Find patterns in cluster
        #print(loaded_cls.labels_, cluster, data)
        patterns = data[loaded_cls.labels_ == cluster]

        # Find similarity between input and patterns
        similarities = cosine_similarity(problem, loaded_vec.transform(patterns['Description'].values))

        # Find most similar patterns
       #index = -2
       #similar_index = np.argmax(similarities)
       #similar_index1 = np.argsort(np.max(similarities, axis=0))[index]
       #similar_pattern = patterns.iloc[similar_index]
       #similar_pattern1 = patterns.iloc[similar_index1]
       #while similar_pattern['Pattern'] == similar_pattern1['Pattern']:
       #    index -= 1
       #    print(similar_pattern1['Pattern'])
       #    similar_index1 = np.argsort(np.max(similarities, axis=0))[index]
       #similar_index2 = np.argsort(np.max(similarities, axis=0))[index-1]
       #similar_pattern2 = patterns.iloc[similar_index2]

        # Find most similar patterns
        similar_index = np.argmax(similarities)
        similar_index1 = np.argsort(np.max(similarities, axis=0))[-2]
        similar_index2 = np.argsort(np.max(similarities, axis=0))[-3]

        # Get similar patterns
        similar_pattern = patterns.iloc[similar_index]
        similar_pattern1 = patterns.iloc[similar_index1]
        similar_pattern2 = patterns.iloc[similar_index2]

        # Get similarity score
        similarity_score = similarities[0][similar_index]
        similarity_score1 = similarities[0][similar_index1]
        similarity_score2 = similarities[0][similar_index2]

        # Format output for html display including similarity scores
        output = f"{similar_pattern['Pattern']} Category: {similar_pattern['Category']} Similarity: {similarity_score}"
        output1 = f"{similar_pattern1['Pattern']} Category: {similar_pattern1['Category']} Similarity: {similarity_score1}"
        output2 = f"{similar_pattern2['Pattern']} Category: {similar_pattern2['Category']} Similarity: {similarity_score2}"
        
        # Return patterns
        return output, output1, output2
    
    def predictTest(self, problem, data, loaded_cls, loaded_vec):
        # The main method to process and predict based on the input data
        # Vectorize input
        problem = self.clusterer.vectorize(problem, loaded_vec)# loaded_vec.transform([problem])
        # Predict cluster
        cluster = self.clusterer.predict(problem, loaded_cls)# loaded_cls.predict(problem)[0]
    
        # Find patterns in cluster
        #print(loaded_cls.labels_, cluster, data)
        patterns = data[loaded_cls.labels_ == cluster]

        # Find similarity between input and patterns
        similarities = cosine_similarity(problem, loaded_vec.transform(patterns['Description'].values))

        # Find most similar patterns
        similar_index = np.argmax(similarities)
        similar_index1 = np.argsort(np.max(similarities, axis=0))[-2]
        similar_index2 = np.argsort(np.max(similarities, axis=0))[-3]

        # Get similar patterns
        similar_pattern = patterns.iloc[similar_index]
        similar_pattern1 = patterns.iloc[similar_index1]
        similar_pattern2 = patterns.iloc[similar_index2]
        
        # Return patterns
        return similar_pattern['Pattern'], similar_pattern1['Pattern'], similar_pattern2['Pattern']
