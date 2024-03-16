import pandas as pd
import pickle
from vectorizer_sc import Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

class ngramVectorizer(Vectorizer):
    def __init__(self, range=(1, 3)):
        super().__init__()
        self.range = range
        self.vectorizer = TfidfVectorizer(ngram_range=range)
        
    def vectorize(self, df: pd.DataFrame):
        vec = TfidfVectorizer(ngram_range=(2, 3))
        vec.fit(df.Description.values)
        features = vec.transform(df.Description.values)
    
        # Save vectorizer
        filepath = Path(__file__).parent / "vectorizers/vectorizer_ngram.pkl"
        with open(filepath, 'wb') as vec_file:
            pickle.dump(vec, vec_file)
    
        return features