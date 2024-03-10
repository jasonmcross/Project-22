from vectorizer_sc import Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class defaultVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()
        self.vectorizer = TfidfVectorizer()
        
    def vectorize(self, data):
        return self.vectorizer.fit_transform(data)