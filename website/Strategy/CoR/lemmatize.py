from CoR.preprocessor_sc import Preprocessor
from nltk.stem import WordNetLemmatizer

class Lemmatize(Preprocessor):
    
    def preprocess(self, data):
        # Lemmatize words
        lemmatizer = WordNetLemmatizer()
        tok = data.split()
        lem = [lemmatizer.lemmatize(word) for word in tok]
        text = ' '.join(lem)
        
        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text
