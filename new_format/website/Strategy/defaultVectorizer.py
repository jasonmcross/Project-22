import pandas as pd
import pickle
from vectorizer_sc import Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

class defaultVectorizer(Vectorizer):
    def __init__(self):
        super().__init__()
        
    def vectorize(self, df: pd.DataFrame):
        descriptions = df['Description']

        self.vectorizer.fit(descriptions)
        features = self.vectorizer.transform(descriptions)
        self.add_weights(features)
    
        # Save vectorizer
        filepath = Path(__file__).parent / "vectorizers/vectorizer_default.pkl"
        with open(filepath, 'wb') as vec_file:
            pickle.dump(self.vectorizer, vec_file)
    
        return features