from vectorizer_sc import Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class ngramVectorizer(Vectorizer):
    def __init__(self, range=(1, 3)):
        super().__init__()
        self.range = range
        self.vectorizer = TfidfVectorizer(ngram_range=range)
        
    def vectorize(self, data):
        return self.vectorizer.fit_transform(data)