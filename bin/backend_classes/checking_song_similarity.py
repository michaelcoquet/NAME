"""CMPT 370 Group 5 Project: NAME (Nearly Analogous Music Engine)
    Credits: Michael Coquet
             Elizabeth Reid
             Ben Camplin
             Laurence Craig Garcia
             Sean Warren
"""
import string
import random
import operator
from name.backend_classes.query import Query
from name.backend_classes.song_similarity import SongSimilarity
from name.backend_classes.spotify_api_manager import SpotifyAPIManager

class CheckingSongSimilarity:
    """ A helper class which handles several aspects of checking
        song similarity
    """

    def __init__(self, features):
        self.features = features

    def random_search(self, songs):
        """ A function to search for 25 similar songs
            to a song the user searches for
            songs: the song the user is searching for
            returns: a list of 25 songs
        """
        # get a list of the top five genres for the entered songs
        top_genres = list(self.get_top_genres(songs, 5).keys())
        new_query = Query(self.features)
        similar_songs = []
        while len(similar_songs) < 25:
            # get a random string. % is a wildcard character
            lowercase_letters = string.ascii_lowercase
            random_letter1 = random.choice(lowercase_letters)
            random_string = random_letter1 + "%"
            # pick a random genre from the top genres list to add to the query
            if top_genres != []:
                random_genre = random.choice(top_genres)
                random_string += " " + "genre:\"" + random_genre + "\""
            # max offset for spotify is 2000, but keeping this
            # at 100 is faster
            random_offset = random.randint(0, 2000)
            # in some cases the random offset may be too large,
            # and in that case default to 0
            try:
                found_songs = new_query.search_single_song(random_string, offset=random_offset)
            except:
                found_songs = new_query.search_single_song(random_string)
            # Look at all the found songs and see if any are similar enough
            # to be included
            for song in found_songs:
                # current song names
                similar_song_names = [sim_song.song_name for sim_song in similar_songs]
                if song.song_name not in similar_song_names:
                    songs.append(song)
                    song_similarity = SongSimilarity(songs, self.features)
                    similarity = song_similarity.compare_all()
                    if similarity >= 0.80:
                        similar_songs.append(song)
                        # run a new search after this
                        songs.remove(song)
                        break
                    else:
                        songs.remove(song)
        return similar_songs

    def get_songs_similarity_score(self, songs):
        song_similarity = SongSimilarity(songs, self.features)
        similarity = song_similarity.compare_all()
        return similarity * 100

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
        # get top limit of genres, or less if fewer are returned
        limit = min(limit, len(genres.keys()))
        top_genres = dict(sorted(genres.items(), key=operator.itemgetter(1), reverse=True)[:limit])
        return top_genres
