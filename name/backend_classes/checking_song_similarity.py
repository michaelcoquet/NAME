import string
import random
from name.backend_classes.query import Query
from name.backend_classes.song_similarity import SongSimilarity

class CheckingSongSimilarity:

    def __init__(self, features):
        self.features = features

    def random_search(self, songs):
        """ A function to search for 25 similar songs
        to a song the user searches for
        songs: the song the user is searching for
        returns: a list of 25 songs
        """
        new_query = Query(self.features)
        similar_songs = []
        while len(similar_songs) < 26:
            # get a random string. % is a wildcard character
            lowercase_letters = string.ascii_lowercase
            random_letter1 = random.choice(lowercase_letters)
            random_string = random_letter1 + "%"
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
