from spotify_api_manager import SpotifyAPIManager


class Query:

    def __init__(self, filter_list):
        """ Instantiation function. 
        filter_list: A list of filter names to search for
        """
        self.filter_list = filter_list

    def update_filter_list(self, filter_list):
        """ Updates the filter list. 
        filter_list: updated filter list
        """
        self.filter_list = filter_list


    def search_single_song(self, song):
        """ Searches for a single song.
        returns: a list of song objects(from the Song class) 
        """
        spotify_api_manager = SpotifyAPIManager()
        search_result = spotify_api_manager.search_songs([song])
        return search_result["found songs"]

    def get_song_info(self, song):
        """ Get song details for only the specified filters
        in the filter list.
        song = song object
        return: dictionary of song details for the filters
        """
        song_details = song.features
        filter_mappings = {
                           "duration_ms": self.duration,
                           "key": self.key,
                           "tempo": self.tempo,
                           "danceability": self.danceability,
                           "energy": self.energy,
                           "loudness": self.loudness,
                           "mode": self.mode,
                           "speechiness": self.speechiness,
                           "acousticness": self.acousticness,
                           "instrument": self.instrument,
                           "liveness": self.liveness,
                           "valence": self.valence,
                           "time_signature": self.time_signature 
                           }
        # store only the specified filters and corresponding filter values
        # into a dictionary
        filtered_song_details = {}
        for filter in self.filter_list:
            filtered_song_details[filter] = filter_mappings[filter]
        return filtered_song_details

    def get_similarity_score(self,songs):
        """ Gets a similarity score for the given songs. 
        Only considers features from the filter list.
        songs: a list of song objects
        returns: a similarity score value (float)
        """
        song_similarity_calculator = SongSimilarity(songs,self.filter_list)
        result = song_similarity_calculator.compare_all()
        return result

