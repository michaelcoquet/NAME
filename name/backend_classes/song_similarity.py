class SongSimilarity:

    def __init__(self, songs, features):
        """ Instantiation function. 
        songs: a list of songs for which similarity must be calculated
        features: a list of features for which similarity should be
        calculated (e.g. tempo) feature_mappings: a dictionary that
        maps specific feature names to the method that will compute
        the similarity score calculation for that particular feature
        """
        self.songs = songs
        self.features = features
        self.feature_mappings = {"duration_ms": self.calculate_duration_ms_similarity,
                                 "key": self.calculate_key_similarity,
                                 "tempo": self.calculate_tempo_similarity,
                                 "danceability": self.calculate_danceability_similarity,
                                 "energy": self.calculate_energy_similarity,
                                 "loudness": self.calculate_loudness_similarity,
                                 "mode": self.calculate_mode_similarity,
                                 "speechiness": self.calculate_speechiness_similarity,
                                 "acousticness": self.calculate_acousticness_similarity,
                                 "instrumentalness": self.calculate_instrumentalness_similarity,
                                 "liveness": self.calculate_liveness_similarity,
                                 "valence": self.calculate_valence_similarity,
                                 "time_signature": self.calculate_time_signature_similarity} # add the rest

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
        similarity = (0.1 * scores["danceability"]
                     + 0.1 * scores["energy"]
                     + 0.1 * scores["loudness"]
                     + 0.1 * scores["speechiness"]
                     + 0.1 * scores["acousticness"]
                     + 0.1 * scores["instrumentalness"]
                     + 0.1 * scores["liveness"]
                     + 0.1 * scores["valence"]
                     + 0.02 * scores["duration_ms"]
                     + 0.02 * scores["key"]
                     + 0.02 * scores["tempo"]
                     + 0.02 * scores["mode"]
                     + 0.02 * scores["time_signature"]) 

        return str(similarity * 100) + " %"

    def calculate_duration_ms_similarity(self):
        """ Calculates the similarity score for the duration_ms
        feature.
        """
        return 0

    def calculate_key_similarity(self):
        """ Calculates the similarity score for the key feature. """
        return 0

    def calculate_tempo_similarity(self):
        """ Calculates the similarity score for the tempo feature. """ 
        return 0

    def calculate_danceability_similarity(self):
        """ Calculates the similarity score for the danceability feature. """ 
        danceability_scores = []
        for song in songs:
            danceability_scores.append(song.features.danceability)

        if (max(danceability_scores)-min(danceability_scores)) * 3 > 1:
            return 0

        return 1-max(danceability_scores)-min(danceability_scores)

    def calculate_energy_similarity(self):
        """ Calculates the similarity score for the energy feature. """ 
        energy_scores = []
        for song in songs:
            energy_scores.append(song.features.energy)

        if (max(energy_scores)-min(energy_scores)) * 2 > 1:
            return 0

        return 1-max(energy_scores)-min(energy_scores)

    def calculate_loudness_similarity(self):
        """ Calculates the similarity score for the loudness feature. """ 
        loudness_scores = []
        for song in songs:
            loudness_scores.append(song.features.loudness)

        if abs(max(loudness_scores)-min(loudness_scores)) * 4 > 1:
            return 0

        return 1-abs(max(loudness_scores)-min(loudness_scores))

    def calculate_mode_similarity(self):
        """ Calculates the similarity score for the mode feature. """ 
        mode_scores = []
        for song in songs:
            mode_scores.append(song.features.mode)

        return abs(sum(mode_scores)/len(mode_scores)-0.5) / 0.5

    def calculate_speechiness_similarity(self):
        """ Calculates the similarity score for the speechiness feature. """ 
        speechiness_scores = []
        for song in songs:
            speechiness_scores.append(song.features.speechiness)
        
        if (max(speechiness_scores)-min(speechiness_scores)) * 6 > 1:
            return 0
        
        return 1-max(speechiness_scores)-min(speechiness_scores)

    def calculate_acousticness_similarity(self):
        """ Calculates the similarity score for the acoustincness feature. """ 
        acousticness_scores = []
        for song in songs:
            acousticness_scores.append(song.features.acousticness)

        if (max(acousticness_scores)-min(acousticness_scores)) * 5 > 1:
            return 0

        return 1-max(acousticness_scores)-min(acousticness_scores)

    def calculate_instrumentalness_similarity(self):
        """ Calculates the similarity score for the instrumentalness feature. """ 
        instrumentalness_scores = []
        for song in songs:
            instrumentalness_scores.append(song.features.instrumentalness)

        if (max(instrumentalness_scores)-min(instrumentalness_scores)) * 6 > 1:
            return 0

        return 1-max(instrumentalness_scores)-min(instrumentalness_scores) 

    def calculate_liveness_similarity(self):
        """ Calculates the similarity score for the liveness feature. """ 
        liveness_scores = []
        for song in songs:
            liveness_scores.append(song.features.liveness)

        if (max(liveness_scores)-min(liveness_scores)) * 4 > 1:
            return 0

        return 1-max(liveness_scores)-min(liveness_scores)

    def calculate_valence_similarity(self):
        """ Calculates the similarity score for the valence feature. """ 
        valence_scores = []
        for song in songs:
            valence_scores.append(song.features.valence)

        return 1-max(valence_scores)-min(valence_scores) 

    def calculate_time_signature_similarity(self):
        """ Calculates the similarity score for the time_signature feature. """ 
        return 0