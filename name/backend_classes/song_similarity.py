class SongSimilarity:

    def __init__(self, songs, features):
        """ Instantiation function. 
        songs: a list of songs for which similarity must be calculated
        features: a list of features for which similarity should be calculated (e.g. tempo)
        feature_mappings: a dictionary that maps specific feature names to the method that will compute
        the similarity score calculation for that particular feature
        """
        self.songs = songs
        self.features = features
        self.feature_mappings = {"duration_ms": self.calculate_duration_ms_similarity,
                                 "key": self.calculate_key_similarity} # add the rest

    def compare_all(self):
        """ Compares all songs in the songlist, returning similarity
        scores for all the given features
        """
        features = self.features
        feature_mappings = self.feature_mappings
        songs = self.songs
        scores = {}

        # Calculate similarity separately for each feature in the features list
        for feature in features: 
            scores[feature] = feature_mappings[feature]()
        
        # We might want to weight the results for each feature score, but for now
        # just return the mean value
        similarity = sum(scores.values())/len(scores.values())

        return similarity

    def calculate_duration_ms_similarity(self):
        """
        Calculates the similarity score for the duration_ms feature.
        """
        return 0

    def calculate_key_similarity(self):
        """
        Calculates the similarity score for the key feature. 
        """
        return 0