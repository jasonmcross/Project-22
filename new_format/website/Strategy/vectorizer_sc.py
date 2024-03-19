import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

class Vectorizer:
    def __init__(self, some_common_parameter=None, range=(1, 1)):
        self.some_common_parameter = some_common_parameter
        self.vectorizer = TfidfVectorizer(ngram_range=range)
        
    def vectorize(self, data):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def add_weights(self, features):

        important_words = {
            'Behavioral': ['state', 'design', 'method', 'responsibility', 'command', 'interpreter', 'iterator', 'mediater', 'memmento', 'null', 'observer', 'strategy', 'visitor'],
            'Creational': ['factory', 'algorithm', 'create', 'builder', 'pool', 'prototype', 'singleton'],
            'Structural': ['implementation', 'proxy', 'client', 'adapter', 'bridge', 'composite', 'decorator', 'facade', 'flyweight', 'private']
        }

        for cat, words in important_words.items():
            for word in words:
                word_ind = self.vectorizer.vocabulary_.get(word)
                if word_ind is not None:
                    features[:word_ind] *= 2

    def test_vectorizer(self, description, category):

        x_train, x_test, y_train, y_test = train_test_split(description, category, test_size=0.2, random_state=42)
        model = LogisticRegression()

        x_train_tfidf = self.vectorizer.fit_transform(x_train)
        x_test_tfidf = self.vectorizer.transform(x_test)
        print()
        print(x_test_tfidf)
        print()

        model.fit(x_train_tfidf, y_train)
        print(model.get_params())

        y_pred = model.predict(x_test_tfidf)

        accuracy = accuracy_score(y_test, y_pred)
