from preprocessor_sc import Preprocessor
from nltk.tokenize import word_tokenize

class Tokenize(Preprocessor):
    
    def preprocess(self, data):
        # Tokenize words
        tok = word_tokenize(data)
        text = ' '.join(tok)
        processed_data = super().preprocess(text)

        return processed_data