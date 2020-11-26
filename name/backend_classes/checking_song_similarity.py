import string
import random
from name.backend_classes.query import Query
from name.backend_classes.song_similarity import SongSimilarity

class CheckingSongSimilarity:

    def __init__(self, features):
        self.features = features

    def random_search(self, original_song):
        """ A function to search for 25 similar songs
        to a song the user searches for
        original_song: the song the user is searching for
        returns: a list of 25 songs
        """
        new_query = Query(self.features)
        similar_songs = []
        while len(similar_songs) < 26:
            lowercase_letters = string.ascii_lowercase
            random_string = "".join(random.choice(lowercase_letters) for i in range(5))
            random_string += "%"
            found_songs = new_query.search_single_song(random_string)
            for song in found_songs:
                original_song.append(song)
                song_similarity = SongSimilarity(original_song, self.features)
                similarity = song_similarity.compare_all()
                if similarity >= 0.8:
                    similar_songs.append(song)
                original_song.remove(song)
            
        return similar_songs

    def get_songs_similarity_score(self, songs):
        song_similarity = SongSimilarity(songs, self.features)
        similarity = song_similarity.compare_all()
        return similarity * 100
