from website.Strategy.CoR.preprocessor_sc import Preprocessor
from nltk.corpus import wordnet

class Synonymize(Preprocessor):

    def preprocess(self, data):
        # Synonymize words
        words = data.split()
        synonyms = []
        for word in words:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonyms.append(lemma.name())
        text = ' '.join(synonyms)

        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text
