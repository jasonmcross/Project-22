from CoR import extract_adjectives, extract_nouns, extract_verbs, lemmatize, lower_punc, remove_junk, remove_stop, stem, synonymize, tokenize
import agglomerative, dbscan, fuzzyCmean, gaussianMixture, kmeans, mbkmeans, meanShift, spectral
import defaultVectorizer, ngramVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
from CoR import remove_junk
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

    def predict(self, problem, data: pd.DataFrame, loaded_cls, loaded_vec):
        # The main method to process and predict based on the input data
        # Vectorize input
        problem = loaded_vec.transform([problem])
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

        # Convert similarity score to 2 decimal places
        similarity_score = round(similarity_score, 2)
        similarity_score1 = round(similarity_score1, 2)
        similarity_score2 = round(similarity_score2, 2)

        # Get similar patterns
        similar_pattern = patterns.iloc[similar_index]
        similar_pattern1 = patterns.iloc[similar_index1]
        similar_pattern2 = patterns.iloc[similar_index2]

        # Format output for html display including similarity scores
        output = "Pattern: " + similar_pattern['Pattern'] + "   " + "Category: " + similar_pattern['Category'] + "   " + "Similarity: " + similarity_score.astype(str)
        output1 = "Pattern: " + similar_pattern1['Pattern'] + "   " + "Category: " + similar_pattern1['Category'] + "   " + "Similarity: " + similarity_score1.astype(str)
        output2 = "Pattern: " + similar_pattern2['Pattern'] + "   " + "Category: " + similar_pattern2['Category'] + "   " + "Similarity: " + similarity_score2.astype(str)
        
        # Return patterns
        return output, output1, output2  
