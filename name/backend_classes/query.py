import operator

from name.backend_classes.spotify_api_manager import SpotifyAPIManager
from name.backend_classes.song_similarity import SongSimilarity


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

    def search_single_song(self, song, offset=0):
        """ Searches for a single song.
        song: name or formatted query to search for.
        offset: offest of the song results to return. Default is
        0, which returns the first page of results.
        returns: a list of song objects(from the Song class)
        """
        spotify_api_manager = SpotifyAPIManager()
        search_result = spotify_api_manager.search_songs(song_list=[song], offset=offset)
        return search_result["found songs"]

    def get_song_info(self, song):
        """ Get song details for only the specified filters
        in the filter list.
        song = song object
        return: dictionary of song details for the filters
        """
        song_details = song.audio_features
        filter_mappings = {
                           "duration_ms": song_details.duration,
                           "key": song_details.key,
                           "tempo": song_details.tempo,
                           "danceability": song_details.danceability,
                           "energy": song_details.energy,
                           "loudness": song_details.loudness,
                           "mode": song_details.mode,
                           "speechiness": song_details.speechiness,
                           "acousticness": song_details.acousticness,
                           "instrumentalness": song_details.instrumentalness,
                           "liveness": song_details.liveness,
                           "valence": song_details.valence,
                           "time_signature": song_details.time_signature
                           }
        # store only the specified filters and corresponding filter values
        # into a dictionary
        filtered_song_details = {}
        for filter in self.filter_list:
            filtered_song_details[filter] = filter_mappings[filter]
        return filtered_song_details

    def get_similarity_score(self, songs):
        """ Gets a similarity score for the given songs.
        Only considers features from the filter list.
        songs: a list of song objects
        returns: a similarity score value (float)
        """
        song_similarity_calculator = SongSimilarity(songs, self.filter_list)
        result = song_similarity_calculator.compare_all()
        return result

    def get_top_genres(self, songs, limit):
        """ Gets a list of the top genres for the given songs.
        songs: a list of song objects
        limit: the limit for the number of genres to be returned
        returns: a list of genres (strings)
        """
        spotify_api_manager = SpotifyAPIManager()
        genres = {}
        for song in songs:
            genre_lst = spotify_api_manager.get_song_genres(song)
            for genre in genre_lst:
                if genre not in genres:
                    genres[genre] = 1
                else:
                    genres[genre] += 1
        # get top 5 genres, or less if fewer are returned
        limit = min(5, len(genres.keys()))
        top_genres = dict(sorted(genres.items(), key=operator.itemgetter(1), reverse=True)[:limit])
        return top_genres
