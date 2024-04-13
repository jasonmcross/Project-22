class Clusterer:
    def __init__(self, num_clusters=None):
        self.num_clusters = num_clusters        
        
    def cluster(self, features):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def vectorize(self, problem):
        raise NotImplementedError("Subclass must implement abstract method")

    def predict(self, features, cls):
        raise NotImplementedError("Subclass must implement abstract method")