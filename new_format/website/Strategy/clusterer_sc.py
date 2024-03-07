class Clusterer:
    def __init__(self, num_clusters=None):
        self.num_clusters = num_clusters        
        
    def cluster(self, data, features):
        raise NotImplementedError("Subclass must implement abstract method")