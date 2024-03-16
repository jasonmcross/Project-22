class Vectorizer:
    def __init__(self, some_common_parameter=None):
        self.some_common_parameter = some_common_parameter
        
    def vectorize(self, data):
        raise NotImplementedError("Subclass must implement abstract method")