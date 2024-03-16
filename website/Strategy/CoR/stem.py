from CoR.preprocessor_sc import Preprocessor
from nltk.stem import PorterStemmer

class Stem(Preprocessor):    
    
    def preprocess(self, data):
        ps = PorterStemmer()
        # Stem words
        words = [ps.stem(word) for word in data.split()]
        text = ' '.join(words)

        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text
