import pandas as pd
import pickle
from vectorizer_sc import Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

class defaultVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()
        self.vectorizer = TfidfVectorizer()
        
    def vectorize(self, df: pd.DataFrame):
        vec = TfidfVectorizer()
        vec.fit(df.Description.values)
        features = vec.transform(df.Description.values)
    
        # Save vectorizer
        filepath = Path(__file__).parent / "vectorizers/vectorizer_default.pkl"
        with open(filepath, 'wb') as vec_file:
            pickle.dump(vec, vec_file)
    
        return features