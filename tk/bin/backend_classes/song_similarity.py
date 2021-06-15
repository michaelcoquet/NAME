"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import numpy as np
# from bin.backend_classes.song import Song
# from bin.backend_classes.song import SongDetails


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
        # each weight is based on features that we thought were most recognizable
        # these weights are subject to change as we develop the algorithm
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

        return similarity

    def calculate_duration_ms_similarity(self):
        """ Calculates the similarity score for the duration_ms
        feature.
        """
        duration_values = []
        for song in self.songs:
            duration_values.append(song.audio_features.duration)

        # if all the values are the same, the range is 0
        # so we return 1
        if np.ptp(duration_values) == 0:
            return 1

        # normalize the values between 0 and 1
        normalized_values = ((duration_values - np.min(duration_values))
                                    /np.ptp(duration_values))

        # if it is two items, we return 1 - the difference
        if len(normalized_values) <= 2:

            return 1-np.max(normalized_values)-np.min(normalized_values)

        # otherwise the 1 - the standard deviation
        return 1-np.std(normalized_values)

    def calculate_key_similarity(self):
        """ Calculates the similarity score for the key feature. """
        song_keys = []
        for song in self.songs:
            song_keys.append(song.audio_features.key)

        def get_circle_of_fifths_clockwise(original_key, goal_key):
            """ A way to calculate how similar two keys are by going
            around the circle of fifths clockwise.
            """
            # we recursively go through the circle of fifths
            # each number is a key 0 = C, 1 = C#, and so on
            circle_of_fifths_mapping = {0 : 7,
                                        7 : 2,
                                        2 : 9,
                                        9 : 4,
                                        4 : 11,
                                        11 : 6,
                                        6 : 1,
                                        1 : 8,
                                        8 : 3,
                                        3 : 10,
                                        10 : 5,
                                        5 : 0}

            if original_key == goal_key:
                return 0

            # each step away from the original key we add one
            return 1 + get_circle_of_fifths_clockwise(
                    circle_of_fifths_mapping[original_key], goal_key)

        def get_circle_of_fifths_counterclockwise(original_key, goal_key):
            """ A way to calculate how similar two keys are by going
            around the circle of fifths counterclockwise.
            """
            # same thing as the previous function just
            # counterclockwise
            circle_of_fifths_mapping = {0 : 5,
                                        5 : 10,
                                        10 : 3,
                                        3 : 8,
                                        8 : 1,
                                        1 : 6,
                                        6 : 11,
                                        11 : 4,
                                        4 : 9,
                                        9 : 2,
                                        2 : 7,
                                        7 : 0}

            if original_key == goal_key:
                return 0

            return 1 + get_circle_of_fifths_counterclockwise(
                    circle_of_fifths_mapping[original_key], goal_key)


        keys_distance = []
        # now we check each key in the list of keys against each other
        for i in range(len(song_keys)):
            for j in range(i + 1, len(song_keys)):
                keys_distance.append(min(get_circle_of_fifths_clockwise(
                    song_keys[i], song_keys[j]), get_circle_of_fifths_counterclockwise(
                        song_keys[i], song_keys[j])))


        if np.ptp(keys_distance) == 0:
            return 1

        # normalize the values, and return the difference or
        # the standard deviation
        normalized_values = ((keys_distance - np.min(keys_distance))
                                    /np.ptp(keys_distance))

        if len(normalized_values) <= 2:
            return 1-np.max(normalized_values)-np.min(normalized_values)

        return 1-np.std(normalized_values)

    def calculate_tempo_similarity(self):
        """ Calculates the similarity score for the tempo feature. """
        tempo_values = []
        for song in self.songs:
            tempo_values.append(song.audio_features.tempo)

        if np.ptp(tempo_values) == 0:
            return 1

        normalized_values = ((tempo_values - np.min(tempo_values))
                                    /np.ptp(tempo_values))


        if len(normalized_values) <= 2:

            return 1-np.max(normalized_values)-np.min(normalized_values)

        return 1-np.std(normalized_values)

    def calculate_danceability_similarity(self):
        """ Calculates the similarity score for the danceability
            feature.
        """
        # each scaling factor is based on the distribution of scores across
        # all songs in spotify. The tighter the distribution, the higher the
        # scaling factor
        danceability_scaling_factor = 3
        danceability_scores = []
        for song in self.songs:
            danceability_scores.append(song.audio_features.danceability)

        if len(danceability_scores) <= 2:

            if ((max(danceability_scores)-min(danceability_scores)) *
                                    danceability_scaling_factor) > 1:
                return 0

            danceability_similarity = (1-((max(danceability_scores)-min(danceability_scores))
                                                            * danceability_scaling_factor))

            return danceability_similarity

        return 1-np.std(danceability_scores)

    def calculate_energy_similarity(self):
        """ Calculates the similarity score for the energy feature. """
        energy_scaling_factor = 2
        energy_scores = []
        for song in self.songs:
            energy_scores.append(song.audio_features.energy)

        if len(energy_scores) <= 2:

            if ((max(energy_scores)-min(energy_scores)) *
                            energy_scaling_factor) > 1:
                return 0

            energy_similarity = (1-(max(energy_scores)-min(energy_scores) *
                                                    energy_scaling_factor))

            return energy_similarity

        return 1-np.std(energy_scores)

    def calculate_loudness_similarity(self):
        """ Calculates the similarity score for the loudness
            feature.
        """
        loudness_scaling_factor = 4
        loudness_scores = []
        for song in self.songs:
            loudness_scores.append(song.audio_features.loudness)

        if np.ptp(loudness_scores) == 0:
            return 1

        normalized_scores = ((loudness_scores - np.min(loudness_scores))
                                        /np.ptp(loudness_scores))

        if len(normalized_scores) <= 2:

            if (abs(max(normalized_scores)-min(normalized_scores)) *
                                    loudness_scaling_factor) > 1:
                return 0

            loudness_similarity = (1-abs(max(normalized_scores)-min(normalized_scores)) *
                                                            loudness_scaling_factor)

            return loudness_similarity

        return 1-np.std(normalized_scores)

    def calculate_mode_similarity(self):
        """ Calculates the similarity score for the mode feature. """
        mode_scores = []
        for song in self.songs:
            mode_scores.append(song.audio_features.mode)

        return abs(sum(mode_scores)/len(mode_scores)-0.5) / 0.5

    def calculate_speechiness_similarity(self):
        """ Calculates the similarity score for the speechiness
            feature.
        """
        speechiness_scaling_factor = 6
        speechiness_scores = []
        for song in self.songs:
            speechiness_scores.append(song.audio_features.speechiness)

        if len(speechiness_scores) <= 2:

            if ((max(speechiness_scores)-min(speechiness_scores)) *
                                    speechiness_scaling_factor) > 1:
                return 0

            speechiness_similarity = (1-(max(speechiness_scores)-min(speechiness_scores) *
                                                            speechiness_scaling_factor))

            return speechiness_similarity

        return 1-np.std(speechiness_scores)

    def calculate_acousticness_similarity(self):
        """ Calculates the similarity score for the acoustincness
            feature.
        """
        acousticness_scaling_factor = 5
        acousticness_scores = []
        for song in self.songs:
            acousticness_scores.append(song.audio_features.acousticness)

        if len(acousticness_scores) <= 2:

            if ((max(acousticness_scores)-min(acousticness_scores)) *
                                    acousticness_scaling_factor) > 1:
                return 0

            acousticness_similarity = (1-(max(acousticness_scores)-min(acousticness_scores) *
                                        acousticness_scaling_factor))

            return acousticness_similarity

        return 1-np.std(acousticness_scores)

    def calculate_instrumentalness_similarity(self):
        """ Calculates the similarity score for the instrumentalness
            feature.
        """
        instrumentalness_scaling_factor = 6
        instrumentalness_scores = []
        for song in self.songs:
            instrumentalness_scores.append(song.audio_features.instrumentalness)

        if len(instrumentalness_scores) <= 2:

            if ((max(instrumentalness_scores)-min(instrumentalness_scores)) *
                                        instrumentalness_scaling_factor) > 1:
                return 0

            instrumentalness_similarity = (1-((max(instrumentalness_scores) -
                        min(instrumentalness_scores)) * instrumentalness_scaling_factor))

            return instrumentalness_similarity

        return 1-np.std(instrumentalness_scores)

    def calculate_liveness_similarity(self):
        """ Calculates the similarity score for the liveness
            feature.
        """
        liveness_scaling_factor = 4
        liveness_scores = []
        for song in self.songs:
            liveness_scores.append(song.audio_features.liveness)

        if len(liveness_scores) <= 2:

            if ((max(liveness_scores)-min(liveness_scores)) *
                                liveness_scaling_factor) > 1:
                return 0

            liveness_similarity = (1-(max(liveness_scores)-min(liveness_scores)
                                                    * liveness_scaling_factor))

            return liveness_similarity

        return 1-np.std(liveness_scores)

    def calculate_valence_similarity(self):
        """ Calculates the similarity score for the valence
            feature.
        """
        valence_scaling_factor = 1
        valence_scores = []
        for song in self.songs:
            valence_scores.append(song.audio_features.valence)

        if len(valence_scores) <= 2:

            valence_similarity = (1-(max(valence_scores)-min(valence_scores)
                                                * valence_scaling_factor))

            return valence_similarity

        return 1-np.std(valence_scores)

    def calculate_time_signature_similarity(self):
        """ Calculates the similarity score for the time_signature
            feature.
        """
        time_signatures = []
        for song in self.songs:
            time_signatures.append(song.audio_features.time_signature)

        time_signature_relations = []
        for i in range(len(time_signatures)):
            for j in range(i, len(time_signatures)):
                relation = 0
                if time_signatures[i] == time_signatures[j]:
                    relation = 1
                elif time_signatures[i] % 2 == time_signatures[j] % 2:
                    relation = 0.5
                elif (max(time_signatures[i], time_signatures[j]) %
                                        min(time_signatures[i], time_signatures[j])) == 0:
                    relation = 0.25
                time_signature_relations.append(relation)

        if len(time_signature_relations) <= 2:
            return 1-max(time_signature_relations)-min(time_signature_relations)

        return 1-np.std(time_signature_relations)

