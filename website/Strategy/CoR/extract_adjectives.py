from CoR.preprocessor_sc import Preprocessor
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

class ExtractAdjectives(Preprocessor):
    
    def preprocess(self, data):
        tokens = word_tokenize(data)
        tagged = pos_tag(tokens)
        adjs = [word for word, pos in tagged if (pos.startswith('J'))]

        text = ' '.join(adjs)
        
        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text
