from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
from Strategy import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
from Strategy import defaultVectorizer, ngramVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
from new_format.website.Strategy.CoR import remove_junk
from website import preprocessing as pp
from website import vectorizer as vec
from website import cluster_plot as cp
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

    def vectorize_data(self, data):
        # Vectorize the preprocessed data
        if self.vectorizer is not None:
            return self.vectorizer.vectorize(data)
        else:
            raise NotImplementedError("Vectorizer has not been set.")

    def cluster_data(self, data):
        # Apply the clustering algorithm to the vectorized data
        if self.clusterer is not None:
            self.clusterer.cluster(data)
        else:
            raise NotImplementedError("Clusterer has not been set.")

    def predict(self, problem, data, loaded_cls, loaded_vec):
        # The main method to process and predict based on the input data
        # Predict cluster
        cluster = loaded_cls.predict(problem)[0]
    
        # Find patterns in cluster
        patterns = data[loaded_cls.labels_ == cluster]

        # Find similarity between input and patterns
        similarities = cosine_similarity(problem, loaded_vec.transform(patterns['Description'].values))

        # Find most similar patterns
        similar_index = np.argmax(similarities)
        similar_index1 = similar_index + 1
        similar_index2 = similar_index + 2

        # Get similarity score
        similarity_score = similarities[0][similar_index]
        similarity_score1 = similarities[0][similar_index1]
        similarity_score2 = similarities[0][similar_index2]

        # Get similar patterns
        similar_pattern = patterns.iloc[similar_index]
        similar_pattern1 = patterns.iloc[similar_index1]
        similar_pattern2 = patterns.iloc[similar_index2]

        # Format output for html display including similarity scores
        output = f"{similar_pattern['Pattern']}    Category: {similar_pattern['Category']}    Similarity: {similarity_score:.2f}"
        output1 = f"{similar_pattern1['Pattern']}    Category: {similar_pattern1['Category']}    Similarity: {similarity_score1:.2f}"
        output2 = f"{similar_pattern2['Pattern']}    Category: {similar_pattern2['Category']}    Similarity: {similarity_score2:.2f}"

        # Return patterns
        return output, output1, output2  
