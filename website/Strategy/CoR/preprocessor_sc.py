class Preprocessor:
    def __init__(self, next_preprocessor=None):
        self.next_preprocessor = next_preprocessor

    def preprocess(self, data):
        if self.next_preprocessor:
            return self.next_preprocessor.preprocess(data)
        return data