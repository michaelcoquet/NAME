import string
import random
from name.backend_classes.query import Query
from name.backend_classes.song_similarity import SongSimilarity

class CheckingSongSimilarity:

    def __init__(self, songs, features):
        self.songs = songs
        self.features = features

    def random_search(self, original_song, filter_list):
        new_query = Query(filter_list)
        similar_songs = []
        while len(similar_songs) < 26:
            lowercase_letters = string.ascii_lowercase
            random_string = "".join(random.choice(lowercase_letters) for i in range(5))
            random_string += "%"
            found_songs = new_query.search_single_song(random_string)
            for song in found_songs:
                song_similarity = SongSimilarity([song, original_song], filter_list)
                similarity = song_similarity.compare_all()
                if similarity >= 0.8:
                    similar_songs.append(song)
            
        return similar_songs

    def get_songs_similarity_score(self, songs, filter_list):
        song_similarity = SongSimilarity(songs, filter_list)
        similarity = song_similarity.compare_all()
        return similarity * 100
