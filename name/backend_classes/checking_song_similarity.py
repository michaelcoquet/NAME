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
            lowercase_letters = string.ascii_lowercase
            random_string = "".join(random.choice(lowercase_letters) for i in range(5))
            random_string += "%"
            found_songs = new_query.search_single_song(random_string)
            songs.append(found_songs[0])
            song_similarity = SongSimilarity(songs, self.features)
            similarity = song_similarity.compare_all()
            if similarity >= 0.8:
                similar_songs.append(found_songs[0])
            songs.remove(found_songs[0])
            
        return similar_songs

    def get_songs_similarity_score(self, songs):
        song_similarity = SongSimilarity(songs, self.features)
        similarity = song_similarity.compare_all()
        return similarity * 100
