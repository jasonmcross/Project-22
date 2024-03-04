from preprocessor_sc import Preprocessor
from nltk.corpus import stopwords
import nltk

class RemoveStop(Preprocessor):    
    
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    def preprocess(self, data):
        # Remove stop words
        words = [word for word in data.split() if word not in self.stop_words]
        text = ' '.join(words)

        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text