from CoR.preprocessor_sc import Preprocessor
import string

class LowerPunc(Preprocessor):
    def preprocess(self, data):
        # Lower case
        text = data.lower()
        # Remove punctuation
        text = ''.join([c for c in text if c not in string.punctuation])
        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text
