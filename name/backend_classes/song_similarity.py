import numpy as np

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
                                 "time_signature": self.calculate_time_signature_similarity}
        self.weights =          {"duration_ms": 0.02,
                                 "key": 0.02,
                                 "tempo": 0.02,
                                 "danceability": 0.1,
                                 "energy": 0.1,
                                 "loudness": 0.1,
                                 "mode": 0.02,
                                 "speechiness": 0.1,
                                 "acousticness": 0.1,
                                 "instrumentalness": 0.1,
                                 "liveness": 0.1,
                                 "valence": 0.1,
                                 "time_signature": 0.02}

    def compare_all(self):
        """ Compares all songs in the songlist, returning similarity
        scores for all the given features
        """
        features = self.features
        feature_mappings = self.feature_mappings
        weights = self.weights
        scores = 0
        weight = 0

        # Calculate similarity separately for each feature in the features list
        for feature in features:
            weight += weights[feature]
            scores += feature_mappings[feature]() * weights[feature]
        
        similarity = scores / weight

        return str(similarity * 100) + " %"

    def calculate_duration_ms_similarity(self):
        """ Calculates the similarity score for the duration_ms
        feature.
        """
        duration_values = []
        for song in self.songs:
            duration_values.append(song.features.duration)

        normalized_values = ((duration_values - np.min(duration_values))
                                    /np.ptp(duration_values))

        if len(normalized_values) <= 2:
             
            return 1-np.max(normalized_values)-np.min(normalized_values)

        else:
            return 1-np.std(normalized_values)

    def calculate_key_similarity(self):
        """ Calculates the similarity score for the key feature. """
        return 0

    def calculate_tempo_similarity(self):
        """ Calculates the similarity score for the tempo feature. """ 
        tempo_values = []
        for song in self.songs:
            tempo_values.append(song.features.tempo)

        normalized_values = ((tempo_values - np.min(tempo_values))
                                    /np.ptp(tempo_values))

        if len(normalized_values) <= 2:
             
            return 1-np.max(normalized_values)-np.min(normalized_values)

        else:
            return 1-np.std(normalized_values)
        
    def calculate_danceability_similarity(self):
        """ Calculates the similarity score for the danceability feature. """ 
        danceability_scaling_factor = 3
        danceability_scores = []
        for song in self.songs:
            danceability_scores.append(song.features.danceability)

        if len(danceability_scores) <= 2:

            if ((max(danceability_scores)-min(danceability_scores)) * 
                                    danceability_scaling_factor) > 1:
                return 0

            danceability_similarity = (1-((max(danceability_scores)-min(danceability_scores)) 
                                                            * danceability_scaling_factor))

            return danceability_similarity

        else:
            return 1-np.std(danceability_scores)

    def calculate_energy_similarity(self):
        """ Calculates the similarity score for the energy feature. """
        energy_scaling_factor = 2 
        energy_scores = []
        for song in self.songs:
            energy_scores.append(song.features.energy)

        if len(energy_scores) <= 2:

            if ((max(energy_scores)-min(energy_scores)) * 
                            energy_scaling_factor) > 1:
                return 0

            energy_similarity = (1-(max(energy_scores)-min(energy_scores) * 
                                                    energy_scaling_factor))

            return energy_similarity

        else:
            return 1-np.std(energy_scores)

    def calculate_loudness_similarity(self):
        """ Calculates the similarity score for the loudness feature. """
        loudness_scaling_factor = 4 
        loudness_scores = []
        for song in self.songs:
            loudness_scores.append(song.features.loudness)

        normalized_scores = ((loudness_scores - np.min(loudness_scores))
                                        /np.ptp(loudness_scores))

        if len(normalized_scores) <= 2:

            if (abs(max(normalized_scores)-min(normalized_scores)) * 
                                    loudness_scaling_factor) > 1:
                return 0

            loudness_similarity = (1-abs(max(normalized_scores)-min(normalized_scores)) * 
                                                            loudness_scaling_factor)

            return loudness_similarity

        else:
            return 1-np.std(normalized_scores)

    def calculate_mode_similarity(self):
        """ Calculates the similarity score for the mode feature. """ 
        mode_scores = []
        for song in self.songs:
            mode_scores.append(song.features.mode)

        return abs(sum(mode_scores)/len(mode_scores)-0.5) / 0.5

    def calculate_speechiness_similarity(self):
        """ Calculates the similarity score for the speechiness feature. """
        speechiness_scaling_factor = 6 
        speechiness_scores = []
        for song in self.songs:
            speechiness_scores.append(song.features.speechiness)

        if len(speechiness_scores) <= 2:
        
            if ((max(speechiness_scores)-min(speechiness_scores)) * 
                                    speechiness_scaling_factor) > 1:
                return 0
            
            speechiness_similarity = (1-(max(speechiness_scores)-min(speechiness_scores) *  
                                                            speechiness_scaling_factor))

            return speechiness_similarity
        
        else:
            return 1-np.std(speechiness_scores)

    def calculate_acousticness_similarity(self):
        """ Calculates the similarity score for the acoustincness feature. """
        acousticness_scaling_factor = 5
        acousticness_scores = []
        for song in self.songs:
            acousticness_scores.append(song.features.acousticness)

        if ((max(acousticness_scores)-min(acousticness_scores)) * 
                                acousticness_scaling_factor) > 1:
            return 0

        acousticness_similarity = (1-(max(acousticness_scores)-min(acousticness_scores) * 
                                    acousticness_scaling_factor))

        return acousticness_similarity

    def calculate_instrumentalness_similarity(self):
        """ Calculates the similarity score for the instrumentalness feature. """
        instrumentalness_scaling_factor = 6
        instrumentalness_scores = []
        for song in self.songs:
            instrumentalness_scores.append(song.features.instrumentalness)

        if len(instrumentalness_scores) <= 2:

            if ((max(instrumentalness_scores)-min(instrumentalness_scores)) * 
                                        instrumentalness_scaling_factor) > 1:
                return 0

            instrumentalness_similarity = (1-((max(instrumentalness_scores) -
                        min(instrumentalness_scores)) * instrumentalness_scaling_factor))

            return instrumentalness_similarity
        
        else:
            return 1-np.std(instrumentalness_scores)

    def calculate_liveness_similarity(self):
        """ Calculates the similarity score for the liveness feature. """
        liveness_scaling_factor = 4 
        liveness_scores = []
        for song in self.songs:
            liveness_scores.append(song.features.liveness)

        if ((max(liveness_scores)-min(liveness_scores)) * 
                            liveness_scaling_factor) > 1:
            return 0

        liveness_similarity = (1-(max(liveness_scores)-min(liveness_scores) 
                                                * liveness_scaling_factor))
        
        return liveness_similarity

    def calculate_valence_similarity(self):
        """ Calculates the similarity score for the valence feature. """
        valence_scaling_factor = 1
        valence_scores = []
        for song in self.songs:
            valence_scores.append(song.features.valence)

        valence_similarity = (1-(max(valence_scores)-min(valence_scores) 
                                            * valence_scaling_factor))
                                    
        return valence_similarity

    def calculate_time_signature_similarity(self):
        """ Calculates the similarity score for the time_signature feature. """ 
        return 0


