from preprocessor_sc import Preprocessor

class RemoveJunk(Preprocessor):
    junk_words = ["imagine", "pattern", "design", "patterns", "also", "like", "code", "let", "used", "use", "app", "fun", "may", "problem", "client", "often", "later", "however", "got", 
              "given",  "need", "object", "objects", "class", "classes"]
    
    def preprocess(self, data):
        # Remove junk words
        text = ' '.join([word for word in data.split() if word not in self.junk_words])

        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(text)
        else:
            return text