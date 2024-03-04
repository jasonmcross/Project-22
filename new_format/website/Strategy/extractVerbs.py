from preprocessor_sc import Preprocessor
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

class ExtractVerbs(Preprocessor):
    
    def preprocess(self, data):
        tokens = word_tokenize(data)
        tagged = pos_tag(tokens)
        verbs = [word for word, pos in tagged if (pos.startswith('V'))]

        text = ' '.join(verbs)
        
        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text