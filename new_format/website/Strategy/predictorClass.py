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
            return self.clusterer.cluster(data)
        else:
            raise NotImplementedError("Clusterer has not been set.")

    def predict(self, data):
        # The main method to process and predict based on the input data
        preprocessed_data = self.preprocess_data(data)
        vectorized_data = self.vectorize_data(preprocessed_data)
        result = self.cluster_data(vectorized_data)
        return result    
